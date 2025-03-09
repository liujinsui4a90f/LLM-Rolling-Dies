"""
game.py - 摇色子游戏模拟器

该文件实现了一个多人摇色子游戏的模拟，包含游戏规则、玩家交互和游戏流程控制。
主要类：
- Game：游戏主类，负责游戏规则执行和流程控制

作者：Jinsui
版本：1.0
最后更新：2025-03-09
"""

from random import randint
from player import Player
from record import *

class Game:
    """
    ## 摇色子游戏规则

    - **参与人数**：2人以上。
    - **道具**：每人5个色子，一个色盅。
    - **获胜/失败条件**： 每个玩家有5杯酒，若5杯酒全部喝完就会“醉倒”，则游戏失败；最后一个喝完酒的玩家将会获得胜利
    - **规则**：
        1. 每人摇动色盅，看自己的点数并保密。
        2. 玩家依次叫数，猜测全场某种点数的总和（如“3个3”）。
        3. 下家需叫出更高的点数或色子个数（如“4个3”或“3个6”，也可以两个数字都比前一玩家大），或质疑上家的叫数。
        4. 若质疑正确，既全场该点数数量之和小于上家教的数字（例如上家叫“8个6”，但全场6点的数量不足8个），则被质疑者喝酒；反之，质疑者喝酒。
        5. 在叫数之时要在数字后面说明“斋”还是“飞”（例如“3个3斋”或“4个2飞”）
            - 当玩家叫“飞”时，1点被当作万能点数（质疑时须统计全场一点与其所叫点数数量之和）
            - 叫“斋”时则只需计算所叫点数的色子数量。
        6. 叫1点时不能叫“飞”，只能叫“斋”。
        7. 叫飞时，若某家的五个色子仅有1点和所叫点数，称为豹子，计算时将其记为6个对应点数的色子，而非5个。叫“斋”时，只能由5个相同点数的色子构成豹子。
        8. “斋”和“飞”的状态可以相互转换
            - “斋”转变为“飞”时，需将所叫数量较上家所含数量翻倍（例如上家叫“3个3斋”，则己方可叫“6个3飞”）；
            - 从“飞”转变为“斋”时，所叫色子数量最多比上家数量少一个（例如上家叫“6个5飞”，则己方可以叫“5个5斋”，**注意**：这是唯一一种己方所叫数量能少于上家的情况）
        9. 第一局游戏可以由任一名玩家首先叫数，在之后的游戏中，则由上一局游戏喝酒的玩家开始叫数。
        10. 对第一次叫数的限制，当场上有n名玩家时
            - 首先开始叫数的玩家叫1点时，所叫的数量不得少于n-1个；
            - 叫“斋”时，所叫的数量不得少于n；
            - 叫“飞”时，所叫数量不得少于n+1。
    """
    def __init__(self, names : list[str]):
        self.players = [Player(name) for name in names]
        self.playerNum = len(names)
        self.round = 0

        #记录一局游戏
        self.game_recorder = GameRecorder([p.name for p in self.players], [], [])
        self.game_recorder.names = [p.name for p in self.players]

        # 当前行动玩家编号
        self.ActionPlayerNo = randint(0, self.playerNum - 1) 

        # 最近一次喝酒玩家
        self.lastDrinker = 0 # range: [0,self.playerNum - 1]

        # 最近一次玩家叫数
        self.call = {
            "num" : 0,
            "point" : 0,
            "state" : True # "斋"为True，“飞”为False
        }

    def _ResetGame(self):
        # 当前行动玩家编号
        self.ActionPlayerNo = self.lastDrinker % self.playerNum 
        for p in self.players:
            p.dies = [randint(1,6) for i in range(5)]

        # 将上一次行动重置为初始状态
        self.call = {
            "num" : 0,
            "point" : 0,
            "state" : True # "斋"为True，“飞”为False
        }

        self.round += 1

    def _isSuccessfulChallenge(self) -> dict[bool, int]:
        """处理质疑逻辑"""

        pointCounter = 0
        for idx in range(self.playerNum):
            pointCounter += self.players[idx].CountDies(self.call['point'], self.call['state'])
        
        if pointCounter < self.call['num']:
            return {'suc' : True, 'num' : pointCounter}
        else:
            return {'suc' : False, 'num' : pointCounter}

    
    def start_game(self):
        while len(self.players) > 1:
            print(f"第{self.round + 1}局")
            self._ResetGame()
            roundRecorder = RoundRecorder(self.players.copy(), self.round, list(), None, None)  
            
            #无人质疑时，只更新玩家叫数
            challenge = False
            while True:
                
                if self.call['num'] != 0 and self.call['point'] != 0:
                    challenge = self.players[self.ActionPlayerNo].ChooseToChallenge()
                if challenge:
                    print(f"玩家“{self.players[self.ActionPlayerNo].name}”对上家提出质疑")
                    break
                self.call = self.players[self.ActionPlayerNo].GerenateCall(self.call, self.playerNum)

                # 记录这次叫数事件
                roundRecorder.callEvents.append(CallRecorder(
                    self.players[self.ActionPlayerNo].name,
                    self.call['num'],
                    self.call['point'],
                    self.call['state']
                    ))
                print(f"玩家“{self.players[self.ActionPlayerNo].name}”叫数{self.call['num']}个{self.call['point']}{"斋" if self.call['state'] else "飞"}")
                self.ActionPlayerNo = (self.ActionPlayerNo + 1) % self.playerNum
            
            # 当有人质疑时，处理质疑逻辑
            challengeInfo = self._isSuccessfulChallenge()
            if challengeInfo['suc']:
                print(f"玩家“{self.players[self.ActionPlayerNo].name}”质疑成功，上家喝酒")
                self.players[(self.ActionPlayerNo - 1) % self.playerNum].cups -= 1
                self.lastDrinker = (self.ActionPlayerNo - 1) % self.playerNum
            else:
                print(f"玩家“{self.players[self.ActionPlayerNo].name}”质疑失败，自己喝酒")
                self.players[self.ActionPlayerNo].cups -= 1
                self.lastDrinker = self.ActionPlayerNo

            # 记录这次质疑事件
            roundRecorder.challengeEvent = ChallengeRecorder(
                self.players[self.ActionPlayerNo].name,
                self.players[(self.ActionPlayerNo - 1) % self.playerNum].name,
                challengeInfo['suc'],
                self.players[(self.ActionPlayerNo - 1) % self.playerNum].name if challengeInfo['suc'] else self.players[self.ActionPlayerNo].name
            )

            # 将已经“醉倒”的玩家排除出游戏
            for i in range(self.playerNum):
                if self.players[i].cups == 0:
                    loser = self.players.pop(i)
                    self.playerNum -= 1
                    # 记录失败者
                    roundRecorder.loser = loser
                    break

            self.game_recorder.rounds.append(roundRecorder)
            if roundRecorder.loser != None:
                self.game_recorder.losers.append(loser.name)

        
        print(f"玩家{self.players[0].name}获得了本局游戏最终的胜利！")
        print(self.game_recorder.to_dict())

if __name__ == "__main__":
    names = ['A','B','C']
    game = Game(names)
    game.start_game()
