import json
import os
import sys
import re

def traversal_folder(folder_path):
    """遍历指定文件夹，返回所有文件的路径列表
    
    Args:
        folder_path (str): 要遍历的文件夹路径
        
    Returns:
        list: 包含所有文件路径的列表
    """
    file_path = []  # 初始化一个空列表用于存储文件路径
    for root, dirs, files in os.walk(folder_path):  # 使用os.walk遍历文件夹
        # 遍历当前文件夹下的所有文件
        for file_name in files:
            file_path.append(os.path.join(root, file_name))  # 将文件的完整路径添加到列表中
    return file_path  # 返回包含所有文件路径的列表


if __name__ == '__main__':
    """主程序入口：将游戏记录从JSON格式转换为易读的文本格式"""
    
    # 获取record文件夹下所有文件路径
    files = traversal_folder('.\\record')
    for file_name in files:  # 遍历每个文件路径
        if file_name[-4:] != 'json':  # 检查文件扩展名是否为.json
            continue  # 如果不是.json文件，则跳过本次循环
        try:
            # 使用正则表达式从文件名中提取游戏编号
            game_code = re.search('[0-9]*_[0-9]*', file_name).group()
            # 将标准输出重定向到指定的文本文件，用于保存转换后的游戏记录
            sys.stdout = open(f'.\\record\\{game_code}.txt', 'w', encoding='utf-8')

            # 打开并读取 JSON 文件
            with open(file_name, "r", encoding="utf-8") as file:
                # 将 JSON 文件内容解析为字典
                data: dict = json.load(file)
                
                # 从文件名中提取游戏编号（这行代码是多余的，因为在前面已经提取过了）
                game_code = re.search('[0-9]*_[0-9]*', file_name).group()

                # 打印游戏编号
                print(f'游戏编号: {game_code}\n')

                # 获取并打印玩家信息
                names = data['names']

                print(f'本局游戏共有{len(names)}名玩家，他们分别是:', end=' ')
                for n in names:
                    print(n, end=', ')  # 打印每个玩家的名字，用逗号分隔
                print('\n')  # 打印换行符
                
            
                # 处理每一轮游戏数据
                rounds = data['rounds']

                for r in rounds:  # 遍历每一轮游戏数据
                    # 获取当前轮次存活的玩家
                    alive_players = [p['name'] for p in r['alivePlayers']]
                    print('-'*50, '\n')  # 打印分隔线
                    print(f'第{r["round No."]}轮:\n\n场上玩家有:')  # 打印当前轮次的序号
                    for p in r['alivePlayers']:
                        # 打印每个存活的玩家的名字、他本轮的色子情况以及他还有的酒杯数
                        print(f'{p["name"]}，他本轮的色子是{p["dies"]}，他此时还有{p["cups"]}杯酒。')
                    print()  # 打印换行符

                    # 处理玩家之间的印象
                    for opinions in r['opinions']:
                        current_player = list(opinions.keys())[0]  # 获取当前处理的玩家名称
                        if current_player not in alive_players:  # 检查当前玩家是否存活
                            continue  # 如果当前玩家不在存活玩家列表中，则跳过本次循环
                        opinion = opinions[current_player]  # 获取当前玩家对其他玩家的意见
                        for other_player in opinion.keys():  # 遍历当前玩家对其他玩家的意见
                            if other_player not in alive_players:  # 检查被提到的其他玩家是否存活
                                continue  # 如果被提到的其他玩家不在存活玩家列表中，则跳过本次循环
                            # 打印当前玩家对其他玩家的印象
                            print(f'{current_player}对{other_player}的印象是: {opinion[other_player]}')
                        print()  # 打印换行符
                    print()  # 打印换行符
                    
                    print('本轮游戏开始：\n')  # 打印本轮游戏开始提示
                    # 处理每个游戏事件（叫数、质疑等）
                    for event in r['Events']:
                        if event["Event Type"] == "Call":  # 如果事件类型是叫数
                            # 打印叫数事件的详细信息
                            print(f'{event["Actor"]}认为：{event["Reason"]}')
                            print(f'这时他{event["Action"]}\n')
                            # 打印叫数的具体内容
                            print(f'{event["Actor"]}叫数{event["Detial"]["num"]}个{event["Detial"]["point"]}{"斋" if event["Detial"]["state"] else "飞"}.')
                        elif event["Event Type"] == "Challenge":  # 如果事件类型是质疑
                            # 打印质疑事件的详细信息
                            print(f'{event["Actor"]}认为：{event["Reason"]}')
                            print(f'这时他{event["Action"]}\n')
                            # 打印质疑的具体内容
                            print(f'{event["Actor"]}选择{"" if event["Decision"] else "不"}质疑{event["Impugant"]}')
                            if event["Decision"]:  # 如果玩家决定质疑
                                print()  # 打印换行符
                                # 打印质疑的结果以及喝酒的玩家
                                print(f'{event["Actor"]}质疑{"成功" if event["Detial"]["suc"] else "失败"}，{event["Detial"]["drinker"]}喝了一杯酒')
                        print()  # 打印换行符
                    # 打印本轮中是否有玩家喝醉
                    if r['loser'] is None:
                        print('本轮中没有玩家喝醉。')
                    else:
                        print(f'{r["loser"]}在本轮中喝醉了。')
                    print('本轮游戏结束。')  # 打印本轮游戏结束提示
                    print('\n')  # 打印换行符

                # 打印本局游戏中淘汰的所有玩家
                losers = data['losers']
                print('本局游戏中淘汰的玩家为（按先后顺序）：', end='')
                for loser in losers:
                    print(loser, ',', end=' ')  # 打印每个被淘汰的玩家名字，用逗号分隔
                print()  # 打印换行符

                # 打印本局游戏的赢家
                winner = data['winner']
                print(f'本局游戏的赢家是：{winner}')

        except json.JSONDecodeError as e:
            # 打印JSON解码错误信息
            print(f"错误: 文件 {file_name} 不是有效的 JSON 文件。错误信息: {e}")
        except FileNotFoundError:
            # 打印文件未找到错误信息
            print(f"错误: 文件 {file_name} 不存在。")
        except Exception as e:
            # 打印其他异常错误信息
            print(f"错误: 读取文件 {file_name} 时发生错误。错误信息: {e}")

