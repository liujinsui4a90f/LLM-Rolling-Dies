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
    """主程序入口：统计过往游戏的记录并输出到文本文件"""
    # 重定向标准输出到指定的文本文件
    sys.stdout = open(f'.\\stat.md', 'w', encoding='utf-8')
    # 获取record文件夹下所有文件路径
    files = traversal_folder('.\\record')

    gameNum = 0
    players = []
    win_times = {}
    credits = {}
    pk = {}
    for file_name in files:  # 遍历每个文件路径
        if file_name[-4:] != 'json':  # 检查文件扩展名是否为.json
            continue  # 如果不是.json文件，则跳过本次循环

        try:
            # 打开并读取 JSON 文件
            with open(file_name, "r", encoding="utf-8") as file:
                # 将 JSON 文件内容解析为字典
                data: dict = json.load(file)
                # 统计游戏数量
                gameNum += 1
                # 更新参与者列表
                for p in data['names']:
                    if not p in players:
                        players.append(p)
                        win_times[p] = 0
                        credits[p] = 0
                        pk[p] = {}

                # 初始化PK统计字典
                for p in players:
                    for op in players:
                        if op != p and not op in pk[p]:
                            pk[p][op] = 0

                # 赢家统计及积分更新
                if data['winner'] in players:
                    win_times[data['winner']] += 1
                    credits[data['winner']] += len(data['names'])
                # 输家积分更新         
                for i, p in enumerate(data['losers']):
                    if p in players:
                        credits[p] += 3 - i

                # 更新PK统计字典
                for r in data['rounds']:
                    final_event = r['Events'][-1]
                    challenger = final_event['Actor']
                    drinker =  final_event['Detial']['drinker']
                    if challenger != drinker:
                        pk[challenger][drinker] += 1
                    else:
                        pk[final_event['Impugant']][drinker] += 1
                   
        except json.JSONDecodeError as e:
            # 打印JSON解码错误信息
            print(f"错误: 文件 {file_name} 不是有效的 JSON 文件。错误信息: {e}")
        except FileNotFoundError:
            # 打印文件未找到错误信息
            print(f"错误: 文件 {file_name} 不存在。")
        except Exception as e:
            # 打印其他异常错误信息
            print(f"错误: 读取文件 {file_name} 时发生错误。错误信息: {e}")
           
    # 输出统计结果
    print("# 过往游戏统计")
    print(f"目前共有 {gameNum} 场游戏记录。")
    print("## 参与者统计")
    print(f"共有 {len(players)} 位玩家参与过游戏。它们分别是：" + ", ".join(players))
    print("## 胜利次数统计")

    print("胜利次数：")
    print('| |','|'.join(players), '|')
    print('|---' * (len(players) + 1), '|')
    print('|获胜次数|','|'.join([str(win_times[p]) for p in players]), '|')
    print("## 总计积分统计")
    print("积分规则：每胜一局，玩家获得与玩家总数对应的积分；其余玩家按照淘汰顺序分别获得对应分数。\n")
    print("积分排名：")
    print('| |','|'.join(players), '|')
    print('|---' * (len(players) + 1), '|')
    print('|积分数量|','|'.join([str(credits[p]) for p in players]), '|')
    print("## PK统计")
    print("当玩家A选择质疑玩家B，如果玩家A喝酒，则记玩家B战胜玩家A一次，反之亦然。\n")
    print("PK统计：")
    print('| |','|'.join(pk.keys()), '|')
    print('|---' * (len(pk.keys()) + 1), '|')
    for p in pk.keys():
        print(f"|{p}", end='')
        for op in pk.keys():
            if op != p:
                print(f'|{pk[p][op]}', end='')
            else:
                print(f'| -', end='')
        print(f"|")

    print()
    print('上表中，横坐标表示喝酒的玩家；纵坐标是质疑成功，或者被质疑但对方质疑失败的玩家。')
