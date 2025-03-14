import json
import os
import sys
import re

def traversal_folder(folder_path):
    file_path = []
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前文件夹下的所有文件
        for file_name in files:
            file_path.append(os.path.join(root, file_name))
    return file_path


if __name__ == '__main__':
    files = traversal_folder('.\\record')
    for file_name in files:
        if file_name[-4:] != 'json':
            continue
        try:
            game_code = re.search('[0-9]*_[0-9]*', file_name).group()
            sys.stdout = open(f'.\\record\\{game_code}.txt', 'w', encoding='utf-8')

            # 打开并读取 JSON 文件
            with open(file_name, "r", encoding="utf-8") as file:
                # 将 JSON 文件内容解析为字典
                data : dict = json.load(file)

                print(f'游戏编号: {game_code}\n')

                names = data['names']

                print(f'本局游戏共有{len(names)}名玩家，他们分别是:', end=' ')
                for n in names:
                    print(n, end=', ')
                print('\n')
                
            
                rounds = data['rounds']

                for r in rounds:
                    alive_players = [p['name'] for p in r['alivePlayers']]
                    print('-'*50, '\n')
                    print(f'第{r['round No.']}轮:\n\n场上玩家有:')
                    for p in r['alivePlayers']:
                        print(f'{p["name"]}，他本轮的色子是{p['dies']}，他此时还有{p['cups']}杯酒。')
                    print()

                    for opinions in r['opinions']:
                        current_player = list(opinions.keys())[0]
                        if not current_player in alive_players:
                            continue
                        opinion = opinions[current_player]
                        for othrt_player in opinion.keys():
                            if not othrt_player in alive_players:
                                continue
                            print(f'{current_player}对{othrt_player}的印象是: {opinion[othrt_player]}')
                        print()
                    print()
                    
                    print('本轮游戏开始：\n')
                    for event in r['Events']:
                        if event["Event Type"] == "Call":
                            print(f'{event['Actor']}认为：{event['Reason']}')
                            print(f'这时他{event['Action']}\n')
                            print(f'{event['Actor']}叫数{event['Detial']['num']}个{event['Detial']['point']}{'斋' if event['Detial']['state'] else '飞'}。')
                        elif event["Event Type"] == "Challenge":
                            print(f'{event['Actor']}认为：{event['Reason']}')
                            print(f'这时他{event['Action']}\n')
                            print(f'{event['Actor']}选择{'' if event["Decision"] else '不'}质疑{event["Impugant"]}')
                            if event["Decision"]:
                                print()
                                print(f'{event['Actor']}质疑{'成功' if event['Detial']['suc'] else '失败'}，{event['Detial']["drinker"]}喝了一杯酒')
                        print()
                    if r['loser'] == None:
                        print('本轮中没有玩家喝醉。')
                    else:
                        print(f'{r['loser']}在本轮中喝醉了。')
                    print('本轮游戏结束。')
                    print('\n')

                losers = data['losers']
                print('本局游戏中淘汰的玩家为（按先后顺序）：',end='')
                for loser in losers:
                    print(loser, ',', end=' ')
                print()

                winner = data['winner']
                print(f'本局游戏的赢家是：{winner}')

                #break
        except json.JSONDecodeError as e:
            print(f"错误: 文件 {file_name} 不是有效的 JSON 文件。错误信息: {e}")
        except FileNotFoundError:
            print(f"错误: 文件 {file_name} 不存在。")
        except Exception as e:
            print(f"错误: 读取文件 {file_name} 时发生错误。错误信息: {e}")