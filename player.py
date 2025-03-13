"""
player.py - 摇色子游戏模拟器的玩家类

该文件实现了一个多人摇色子游戏的玩家的模拟。
主要类：
- Player：玩家类，执行游戏逻辑以及与大模型交互

作者：Jinsui
版本：1.0
最后更新：2025-03-11
"""
import json
import re
from random import randint
from llmClient import LLMClient

def isValidAction(last_action : dict[int, int, bool], action : dict[int, int, bool], playerNum) -> tuple[bool, str]:
        # 当游戏中第一个玩家叫数时
        if last_action["num"] == 0 and last_action['point'] == 0:
            # 1点必须n-1个起叫
            if action['num'] < playerNum - 1 and action['point'] == 1:
                return False, "你刚刚叫的数不符合规则，因为开局叫1点时，所叫点数必须大于等于场上玩家数减一"
            # 斋必须n个起叫
            if action['num'] < playerNum and action['state'] == True:
                return False, "你刚刚叫的数不符合规则，因为开局叫斋时，所叫点数必须大于等于场上玩家数"
            # 飞必须n+1起叫
            if action['num'] < playerNum + 1 and action['state'] == False:
                return False, "你刚刚叫的数不符合规则，因为开局叫飞时，所叫点数必须大于等于场上玩家数加一"
        
        # 叫1的时候不能叫飞
        elif action['point'] == 1 and action['state'] == False:
            return False, "你刚刚叫的数不符合规则，因为叫1的时候不能叫飞"
                    
        # 飞换斋时, 所叫色子数量最多比上家数量少一个
        elif action['state'] and not last_action['state']:
            if action['num'] < last_action['num'] - 1:
                return False, "你刚刚叫的数不符合规则，因为飞换斋时, 所叫色子数量最多比上家数量少一个"
        
        # 斋换飞时，需将所叫数量较上家所含数量翻倍
        elif not action['state'] and last_action['state']:
            if action['num'] < last_action['num'] * 2:
                return False, "你刚刚叫的数不符合规则，因为斋换飞时，需将所叫数量较上家所叫数量翻倍"

        # 一般情况下
        else:
            # 玩家所叫点数和个数须至少一个大于上家所叫
            if action['num'] < last_action['num'] and action['point'] < last_action['point']:
                return False, "你刚刚叫的数不符合规则，因为玩家所叫点数和个数须至少一个大于上家所叫"
        
        return True, ''


class Player:
    def __init__(self, name : str, model : str):
        #玩家名
        self.name = name
        self.client = LLMClient(model)

        #游戏基本数据
        self.cups = 3
        self.dies = [0]*5

        self.opinions = {}

        # 读取游戏规则，用于后续生成prompt
        with open("./prompt/rule", 'r', encoding='UTF-8') as r:
            self.rule = r.read()
        self.rule = self.rule.format(name=self.name)

    def DiesReset(self):

        #五个色子如果点数各不一样则需要重摇
        while True:
            dies = [randint(1,6) for _ in range(5)]
            if len(set(dies)) != 5:
                break
        self.dies = dies
    
    def opinion_init(self, Players : list[str]):
        """初始化对其他玩家的看法"""
        self.opinions = {
            p : '还不了解这名玩家'
            for p in Players if p != self.name
        }
    
    def generate_opinion(self, Players : list[str], roundInfo):
        """每轮游戏过后更新对其他玩家的看法"""
        
        for player in self.opinions.keys():
            # 跳过自己
            if player == self.name:
                continue

            # 跳过已经淘汰的玩家
            if not player in Players:
                continue
            with open("./prompt/impression_prompt", 'r', encoding='UTF-8') as c:
                impression_prompt = c.read()
            impression_prompt = impression_prompt.format(rule=self.rule,
                                         round_info=roundInfo,
                                         player=player,
                                         previous_opinion=self.opinions[player])
            for i in range(5):
                try:
                    self.opinions[player] = self.client.ask(impression_prompt)
                    break
                except Exception as e:
                    print(e)
                    print(f"第{i}次尝试失败，即将进行下一次尝试")
                    


    def GenerateChallenge(self, roundInfo) -> dict:
        with open("./prompt/challenge_prompt", 'r', encoding='UTF-8') as c:
            challenge_prompt = c.read()
            challenge_prompt = challenge_prompt.format(rule=self.rule,
                                         round_info=roundInfo,
                                         dies=self.dies,
                                         understanding=json.dumps(self.opinions, ensure_ascii=False),
                                         cups=self.cups)
        
        for i in range(5):
            try:
                # 向llm发起询问
                response = self.client.ask(challenge_prompt)
                # 提取json
                response = re.search(r'({[\s\S]*})', response)
                if response:
                    response = response.group()
                    response = json.loads(response)

                    # 如果没获得指定的键
                    if not all(key in response for key in ['choice','reason','action']):
                        raise Exception("质疑生成失败")
                else:
                    # 如果没有匹配到json结构
                    raise Exception("质疑生成失败")

                return response
            except Exception as e:
                print(e)
                print(f"第{i+1}次尝试，质疑生成失败或不符合规则")
        print("有人砸场子，这破酒不喝也罢！")
        raise Exception("有玩家连续五次没有生成正确的行动，游戏结束")
    
    def text2call(self, text : str) -> dict:
        """
        从文本中提取call结构体

        @INPUT
        - text : str 一段对玩家行动的描述

        @OUTPUT
        call : dict 一个字典，包含`num`,`point`,`state`三个键

        例：
        input: "轻轻敲击桌面，目光坚定地扫过其他玩家，语气平稳但略带自信地说道：‘6个4斋。’随后微微挑眉，等待下家的反应。"
        output: {'num' : 6, 'point' : 4, 'state' : True}
        
        """
        match_rule = r'[0-9]*个[0-9][斋|飞]'
        call = {'num' : None, 'point' : None, 'state' : None}
        result = re.search(match_rule, text)
        if result != None:
            result = result.group()
        else:
            return call
        call['state'] = True if result[-1] == '斋' else False
        call['point'] = int(result[-2])
        call['num'] = int(result[:-3])
        return call

    def GerenateCall(self, last_call : dict, playerNum : int, roundInfo : str):

        with open("./prompt/call_prompt", 'r', encoding='UTF-8') as c:
            call_prompt = c.read()
        call_prompt = call_prompt.format(rule=self.rule,
                                         round_info=roundInfo,
                                         dies=self.dies,
                                         understanding=json.dumps(self.opinions, ensure_ascii=False),
                                         cups=self.cups)
        instruction = None
        for i in range(5):
            try:
                # 如上次叫数失败或不符合规则
                if i > 0 and instruction != None:
                    call_prompt = call_prompt + f'\n你刚刚叫了{call['num']}个{call['point']}{'斋' if call['state'] else '飞'}\n'
                    call_prompt = call_prompt + instruction
                    call_prompt = call_prompt + '\n请重新叫数'
                # 向llm发起询问
                response = self.client.ask(call_prompt)
                # 提取json
                response = re.search(r'({[\s\S]*})', response)
                if response:
                    response = response.group()
                    response = json.loads(response)

                    # 如果没获得指定的键
                    if not all(key in response for key in ['num','point','state','reason','action']):
                        raise Exception("叫数生成失败")
                else:
                    # 如果没有匹配到json结构
                    raise Exception("叫数生成失败")

                if response['point'] < 1 or response['point'] > 6:
                    raise ValueError("Point out of Boundary (1-6)")
                if response['num'] > playerNum * 5:
                    raise ValueError("The Player called too many dies")
                call = {
                    'num' : response['num'],
                    'point' : response['point'],
                    'state' : response['state']
                }
                call_in_action = self.text2call(response['action'])
                if call != call_in_action:
                    instruction = "action中的叫数与结构体中的\"num\",\"point\",\"state\"不一致,请重试"
                    raise Exception("action中的叫数与结构体中的\"num\",\"point\",\"state\"不一致")
                elif call_in_action['num'] == None:
                    instruction = "请务必将你的叫数在json结构体的\"action\"中明确体现，以使其他玩家你的确切的了解你的行动"
                    raise Exception("叫数未置于`action`键中")

                #判断该行动是否符合规则
                vaildcall, instruction = isValidAction(last_call, call, playerNum)
                if not vaildcall:
                    raise ValueError("The call doesn't match rules, please retry.")
                
                output = {'call' : call,
                          'reason' : response['reason'],
                          'action' : response['action']}
                return output
            
            except Exception as e:
                print(f"ERROR: {e}")
                print(f"第{i+1}次尝试，叫数生成失败或不符合规则")
            
            
        print("有人砸场子，这破酒不喝也罢！")
        raise Exception("有玩家连续五次没有生成正确的行动，游戏结束")

    def CountDies(self, point : int, isZhai : bool) -> int:
        if point < 1 or point > 6:
            raise ValueError("Invaild point of dies, beyond 1 to 6")
        
        #判断是不是豹子
        BaoZi = True
        for i in range(5):
            #当玩家叫“斋”时
            if self.dies[i] != point and isZhai:
                BaoZi = False
                break
            #当玩家叫“飞”时
            if (self.dies[i] != point or self.dies[i] != 1) and not isZhai:
                BaoZi = False
                break
        if BaoZi:
            return 6
        
        #正常计数
        counter = 0
        for i in range(5):
            #当玩家叫“斋”时
            if self.dies[i] == point and isZhai:
                counter += 1
            #当玩家叫“飞”时
            if (self.dies[i] == point or self.dies[i] == 1) and not isZhai:
                counter += 1
        return counter
        