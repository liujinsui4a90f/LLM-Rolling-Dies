from random import randint
from utils import isValidAction

class Player:
    def __init__(self, name):
        self.name = name
        self.cups = 1
        self.dies = [0]*5

    def DiesReset(self):
        self.dies = [randint(1,6) for i in range(5)]

    def ChooseToChallenge(self):
        #TODO: 将此过程转换为LLM生成
        return bool(int(input(f"玩家“{self.name}“是否质疑上家 (输入Ture/False):")))

    def GerenateCall(self, last_call, playerNum):
        for i in range(5):
            try:
                #TODO: 将此过程转换为LLM生成
                num, point, state = input("请输入一个动作（以“数量,点数,1(斋)/0(飞)”的格式）：").split(',')
                num = int(num)
                point = int(point)
                state = bool(int(state))

                if point < 1 or point > 6:
                    raise ValueError("Point out of Boundary (1-6)")
                if point > playerNum * 5:
                    raise ValueError("The Player called too many dies")

                call = {
                    'num' : num,
                    'point' : point,
                    'state' : state
                }

                #判断该行动是否符合规则
                if not isValidAction(last_call, call, playerNum):
                    raise ValueError("The call doesn't match rules, please retry.")
                return call
            
            except ValueError as e:
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
        