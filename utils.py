

def isValidAction(last_action : dict[int, int, bool], action : dict[int, int, bool], playerNum) -> bool:
        # 当游戏中第一个玩家叫数时
        if last_action["num"] == 0 and last_action['point'] == 0:
            # 叫1不能叫飞
            if action['point'] == 1 and action['state'] == False:
                return False
            # 1点必须n-1个起叫
            if action['num'] < playerNum - 1 and action['point'] == 1:
                return False
            # 斋必须n个起叫
            if action['num'] < playerNum and action['state'] == True:
                return False
            # 飞必须n+1起叫
            if action['num'] < playerNum + 1 and action['state'] == False:
                return False
                    
        # 飞换斋时, 所叫色子数量最多比上家数量少一个
        elif action['state'] and not last_action['state']:
            if action['num'] < last_action['num'] - 1:
                return False
        
        # 斋换飞时，需将所叫数量较上家所含数量翻倍
        elif not action['state'] and last_action['state']:
            if action['num'] < action['num'] * 2:
                return False

        # 一般情况下
        else:
            # 玩家所叫点数和个数须至少一个大于上家所叫
            if action['num'] < last_action['num'] and action['point'] < last_action['point']:
                return False
        
        return True