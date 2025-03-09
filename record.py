from dataclasses import dataclass
from player import Player

ZHAI = True
FEI = False

@dataclass
class ActionRecorder:
    actor : str

@dataclass
class CallRecorder(ActionRecorder):
    num : int
    point : int
    state : bool

    def to_dict(self):
        return {'actor' : self.actor, 'num' : self.num, 'point' : self.point, 'state' : self.state}

@dataclass
class ChallengeRecorder(ActionRecorder):
    impugant : str
    suc : bool
    drinker : str

    def to_dict(self):
        return {'actor' : self.actor, 'impugant' : self.impugant, 'suc' : self.suc, 'drinker': self.drinker}


@dataclass
class RoundRecorder:
    alivePlayers : list[Player]
    roundNum : int
    callEvents : list[CallRecorder]
    challengeEvent : ChallengeRecorder | None
    loser : Player | None

    def to_dict(self):
        return {
            'round' : self.roundNum,
            'alivePlayers' : [{
                'name' : p.name,
                'dies' : p.dies,
                #'remaining cups' : p.cups
            } for p in self.alivePlayers],
            'calls' : [c.to_dict() for c in self.callEvents],
            'challenge' : self.challengeEvent.to_dict(),
            'loser' : None if self.loser == None else self.loser.name
        }

@dataclass()
class GameRecorder:
    names : list[str]
    losers : list[str]
    rounds : list[RoundRecorder]

    def to_dict(self):
        return {
            'names' : self.names,
            'losers' : self.losers,
            'rounds' : [r.to_dict() for r in self.rounds]
        }




    




    