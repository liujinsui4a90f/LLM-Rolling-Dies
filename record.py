import json
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

    def to_dict(self):
        return {
                'type' : 'Call',
                'actor' : self.actor,
                'detial' : { 'num' : self.num, 'point' : self.point, 'state' : '斋' if self.state else '飞'}
                }

@dataclass
class ChallengeRecorder(ActionRecorder):
    impugant : str
    decision : bool
    suc : bool | None = None
    drinker : str | None = None

    def to_dict(self) -> dict:
        return {
                'type' : 'Challenge',
                'actor' : self.actor,
                'impugant' : self.impugant,
                'decision' : self.decision,
                'detial' : {'suc' : self.suc, 'drinker': self.drinker} if self.decision else None
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



if __name__ == '__main__':
    r = RoundRecorder(alivePlayers=[{'name' : 'A', 'dies' : [3,4,5,5,1], 'cups' : 3},
                                    {'name' : 'B', 'dies' : [3,4,5,5,1], 'cups' : 3},
                                    {'name' : 'C', 'dies' : [3,4,5,5,1], 'cups' : 3}],
                      roundNum=1,
                      PlayerEvents=list(),
                      loser=None)
    r.PlayerEvents.append(CallRecorder('A', 5,3,False))
    r.PlayerEvents.append(ChallengeRecorder('B', 'A', False))
    print(r)
    print(json.dumps(r.to_dict(), indent=4, ensure_ascii=False))

