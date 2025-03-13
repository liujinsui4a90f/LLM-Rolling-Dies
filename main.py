from game import Game
import argparse

if __name__ == "__main__":
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加参数
    parser.add_argument(
        "-n", "--number",  # 参数名称
        type=int,         # 参数类型为整数
        default=1,        # 默认值为 1
        help="输入一个整数（默认为 1）"
    )

    # 解析参数
    args = parser.parse_args()

    configs = [
        {'name' : 'Qwen',     'model' : 'qwen-plus-latest'},
        {'name' : 'DeepSeek', 'model' : 'deepseek-v3-aliyun'},
        {'name' : 'Doubao',   'model' : 'Doubao-1.5-pro-32k'},
        {'name' : 'GLM',      'model' : 'GLM-4-Air'}
    ]
    for i in range(args.number):
        print(f"第{i+1}局游戏\n")
        game = Game(configs)
        game.start_game()