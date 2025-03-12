from game import Game

if __name__ == "__main__":
    configs = [
        {'name' : 'Qwen',     'model' : 'qwen-max-latest'},
        {'name' : 'DeepSeek', 'model' : 'deepseek-chat'},
        {'name' : 'Doubao',   'model' : 'Doubao-1.5-pro-256k'},
        {'name' : 'GLM',      'model' : 'GLM-4-Flash'}
    ]
    game = Game(configs)
    game.start_game()