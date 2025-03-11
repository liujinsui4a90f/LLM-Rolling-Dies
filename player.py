import json
from random import randint
from utils import isValidAction
from llmClient import LLMClient


class Player:
    def __init__(self, name : str, model : str):
        #玩家名
        self.name = name
        self.client = LLMClient(model)

        #游戏基本数据
        self.cups = 1
        self.dies = [0]*5

        self.opinions = {}

        # 读取游戏规则，用于后续生成prompt
        with open("./prompt/rule", 'r', encoding='UTF-8') as r:
            self.rule = r.read()
        self.rule = self.rule.format(name='Player C')

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
            if player == self.name:
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
                except Exception as e:
                    print(e)
                    print(f"第{i}次尝试失败，即将进行下一次尝试")
                    


    def ChooseToChallenge(self, roundInfo) -> dict:
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
                response = response[7:-3]
                response = json.loads(response)

                return response
            except Exception as e:
                print(e)
                print(f"第{i}次尝试，叫数生成失败或不符合规则")
        print("有人砸场子，这破酒不喝也罢！")
        raise Exception("有玩家连续五次没有生成正确的行动，游戏结束")

    def GerenateCall(self, last_call : dict, playerNum : int, roundInfo : str):

        with open("./prompt/call_prompt", 'r', encoding='UTF-8') as c:
            call_prompt = c.read()
        call_prompt = call_prompt.format(rule=self.rule,
                                         round_info=roundInfo,
                                         dies=self.dies,
                                         understanding=json.dumps(self.opinions, ensure_ascii=False),
                                         cups=self.cups)
        for i in range(5):
            try:
                # 向llm发起询问
                response = self.client.ask(call_prompt)
                # 提取json
                response = response[7:-3]
                response = json.loads(response)

                if response['point'] < 1 or response['point'] > 6:
                    raise ValueError("Point out of Boundary (1-6)")
                if response['num'] > playerNum * 5:
                    raise ValueError("The Player called too many dies")
                call = {
                    'num' : response['num'],
                    'point' : response['point'],
                    'state' : response['state']
                }

                #判断该行动是否符合规则
                if not isValidAction(last_call, call, playerNum):
                    raise ValueError("The call doesn't match rules, please retry.")
                
                output = {'call' : call,
                          'reason' : response['reason'],
                          'action' : response['action']}
                return output
            
            except Exception as e:
                print(f"ERROR: {e}")
                print(f"第{i}次尝试，叫数生成失败或不符合规则")
            
            
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
        