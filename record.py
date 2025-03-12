import json
from datetime import datetime
from dataclasses import dataclass
from player import Player


@dataclass
class ActionRecorder:
    actor : str

    def to_dict(self) -> dict:
        pass

@dataclass
class CallRecorder(ActionRecorder):
    num : int
    point : int
    state : bool
    reason : str
    action : str

    def to_dict(self):
        return {
                'Event Type' : 'Call',
                'Actor' : self.actor,
                'Detial' : { 'num' : self.num, 'point' : self.point, 'state' : '斋' if self.state else '飞'},
                'Reason' : self.reason,
                'Action' : self.action
                }

@dataclass
class ChallengeRecorder(ActionRecorder):
    impugant : str
    decision : bool
    reason : str
    action : str
    suc : bool | None = None
    drinker : str | None = None
    

    def to_dict(self) -> dict:
        return {
                'Event Type' : 'Challenge',
                'Actor' : self.actor,
                'Impugant' : self.impugant,
                'Decision' : self.decision,
                'Detial' : {'suc' : self.suc, 'drinker': self.drinker} if self.decision else None,
                'Reason' : self.reason,
                'Action' : self.action
                }


@dataclass
class RoundRecorder:
    alivePlayers : list[dict]
    roundNum : int
    PlayerEvents : list[ActionRecorder]
    loser : Player | None = None

    def to_dict(self) -> dict:
        return {
            'round No.' : self.roundNum,
            'alivePlayers' : [p for p in self.alivePlayers],
            'Events' : [e.to_dict() for e in self.PlayerEvents],
            'loser' : None if self.loser == None else self.loser.name
        }
    
    def round_info(self, currentPlayer : str) -> str:
        """生成本轮游戏的基本信息"""

        # 玩家人数
        info = [f'本轮游戏中，场上共有{len(self.alivePlayers)}名玩家。除你之外']

        # 每个玩家的信息
        for p in self.alivePlayers:
            if p['name'] == currentPlayer:
                continue
            info.append(f"玩家{p['name']}目前还有{p['cups']}杯酒")
        info.append('\n')

        # 玩家过往叫数或质疑
        info.append('以下是这轮游戏中其他玩家的过往行为：')
        for event in self.PlayerEvents:
            if hasattr(event, "impugant"):
                if event.decision:
                    info.append(f"{"玩家"+event.actor if event.actor != currentPlayer else '你'}选择质疑{'玩家'+event.impugant if event.impugant != currentPlayer else '你'}，")
                else:
                    info.append(f"{"玩家"+event.actor if event.actor != currentPlayer else '你'}选择不质疑{'玩家'+event.impugant if event.impugant != currentPlayer else '你'}，")
                info.append(f'此时{'他' if event.actor != currentPlayer else '你'}' + event.action)
            else:
                info.append(f"{'玩家'+event.actor if event.actor != currentPlayer else '你'}叫数{event.num}个{event.point}{'斋' if event.state else '飞'}，")
                info.append(f'此时{'他' if event.actor != currentPlayer else '你'}' + event.action)

        return '\n'.join(info)
    
    def round_history(self, currentPlayer : str) -> str:
        info = [f'本轮游戏中，场上共有{len(self.alivePlayers)}名玩家。']

        info.append('以下是这轮游戏中其他玩家的过往行为：')
        for event in self.PlayerEvents:
            if hasattr(event, "impugant"):
                if event.decision:
                    info.append(f"{"玩家"+event.actor if event.actor != currentPlayer else '你'}选择质疑{'玩家'+event.impugant if event.impugant != currentPlayer else '你'}，")
                    info.append(f'此时{'他' if event.actor != currentPlayer else '你'}' + event.action)
                    info.append(f"{"玩家"+event.actor if event.actor != currentPlayer else '你'}质疑{"成功" if event.suc else '失败'}，{event.impugant if event.suc else event.actor}喝了一杯酒")
                else:
                    info.append(f"{"玩家"+event.actor if event.actor != currentPlayer else '你'}选择不质疑{'玩家'+event.impugant if event.impugant != currentPlayer else '你'}，")
                    info.append(f'此时{'他' if event.actor != currentPlayer else '你'}' + event.action)
            else:
                info.append(f"{'玩家'+event.actor if event.actor != currentPlayer else '你'}叫数{event.num}个{event.point}{'斋' if event.state else '飞'}，")
                info.append(f'此时{'他' if event.actor != currentPlayer else '你'}' + event.action)

        if self.loser == None:
            info.append('本局游戏中没有人醉倒')
        else:
            info.append(f'玩家{self.loser.name}在本局游戏中醉倒了。')


        return '\n'.join(info)


@dataclass()
class GameRecorder:
    names : list[str]
    losers : list[str]
    rounds : list[RoundRecorder]

    def to_dict(self) -> dict:
        return {
            'names' : self.names,
            'losers' : self.losers,
            'rounds' : [r.to_dict() for r in self.rounds]
        }
    def save(self):
        d = self.to_dict()
        j = json.dumps(d)
        datestrap = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'./record/{datestrap}.json', 'w', encoding='UTF-8') as f:
            f.write(j)


if __name__ == '__main__':
    r = RoundRecorder(alivePlayers=[{'name' : 'A', 'dies' : [3,4,5,5,1], 'cups' : 3},
                                    {'name' : 'B', 'dies' : [3,4,5,5,1], 'cups' : 3},
                                    {'name' : 'C', 'dies' : [3,4,5,5,1], 'cups' : 3}],
                      roundNum=1,
                      PlayerEvents=list(),
                      loser=None)
    r.PlayerEvents.append(CallRecorder('A', 5,3,False,'','冷静地摇动色盅，微微皱眉，似乎在思考，然后坚定地说出‘4个5斋’'))
    r.PlayerEvents.append(ChallengeRecorder('B', 'A', False,"","轻轻点头，目光在Alen和Cendy之间游移，似乎在思考，但没有立即做出反应，保持沉默。"))
    r.PlayerEvents.append(CallRecorder('B', 6,3,False,'','冷静地摇动色盅，微微皱眉，似乎在思考，然后坚定地说出‘4个5斋’'))
    r.PlayerEvents.append(ChallengeRecorder('C', 'B', False,'','轻轻点头，目光在Alen和Cendy之间游移，似乎在思考，但没有立即做出反应，保持沉默。'))
    r.PlayerEvents.append(CallRecorder('C', 8,5,False,'','冷静地摇动色盅，微微皱眉，似乎在思考，然后坚定地说出‘4个5斋’'))
    r.PlayerEvents.append(ChallengeRecorder('A', 'C', True, '', '高声大喊：开！',True, 'C'))
    print(r)
    print(r.round_history('A'))

