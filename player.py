from random import randint
from utils import isValidAction

class Player:
    def __init__(self, name):
        self.name = name
        self.cups = 5
        self.dies = [0]*5

    def DiesReset(self):
        self.dies = [randint(1,6) for i in range(5)]

    def GerenateAction(self, last_action, playerNum):
        for i in range(5):
            #TODO: 将此过程转换为LLM生成
            num, point, state = input("请输入一个动作（以“数量,点数,True(斋)/False(飞)”的格式）：").split(',')
            num = int(num)
            point = int(point)
            state = bool(state)

            action = {
                'num' : num,
                'point' : point,
                'state' : state
            }

            #判断该行动是否符合规则
            if not isValidAction(last_action, action, playerNum):
                print("该行动无效或不符合规则，请重试")
                continue
            return action
        raise "有人砸场子，这破酒不喝也罢！"

    def CountDies(self, point : int, isZhai : bool) -> int:
        if point < 1 or point > 6:
            raise "Invaild point of dies, beyond 1 to 6" 
        
        #判断是不是豹子
        BaoZi = True
        for i in range(5):
            #当玩家叫“斋”时
            if self.dies[i] != point and isZhai:
                BaoZi = False
            #当玩家叫“飞”时
            if (self.dies[i] != point or self.dies[i] != 1) and not isZhai:
                BaoZi = False
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
        