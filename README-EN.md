# LLM-Rolling-Dies
This project is a rolling dice simulation program driven by LLM (Large Language Model).

## Configuration

1. Use conda or other environment management tools to install the necessary dependencies:
```
pip install openai
```

2. Create an account on [MindCraft](https://www.mindcraft.com.cn/) and generate an API Key.
3. Create an `API-KEY` file in the root directory of the project and paste the generated API key into it.
4. The project sets four models, `deepseek-chat`, `qwen-max-latest`, `Doubao-1.5-pro-256k`, and `GLM-4-Flash`, as default players. If users want to use other models, please refer to the models supported in the MindCraft [documentation](https://apifox.com/apidoc/shared-0fd7ea54-919e-4c93-b673-c60219bc82e0/api-199055738).

## Usage
### Running the Game
Run `main.py` to start a game.
```sh
python main.py
```
Execute
```python
python main.py -n x
```
to run multiple games, where `x` is the number of games.

### Record Conversion
Execute
```python
python record_convert.py
```
to convert game records from JSON format to a more readable text format.

### Game Statistics
Execute
```python
python analyse.py
```
to analyze the game results. When `analyse.py` is run, it automatically reads all JSON files in the `./record` directory and performs the analysis.

## Known Issues
- If the LLM's call does not conform to the rules, the specific rule violated by the previous call will be added to the prompt, and the call will be regenerated, which may interfere to some extent with AI's judgment. Users can choose to optimize the prompt to enhance the AI's reasoning ability (it may also weaken it).
- When running under Python 3.10, there will be a strange f-string error. This issue does not occur when using Python 3.12.

## Acknowledgments
This project is inspired by the [Liars Bar LLM](https://github.com/LYiHub/liars-bar-llm) project by [LYiHub](https://github.com/LYiHub/). We would like to express our gratitude to [LYiHub](https://github.com/LYiHub/).

The project uses the unified API call interface configured by [MindCraft](https://www.mindcraft.com.cn/). We would like to express our gratitude to [MindCraft](https://www.mindcraft.com.cn/).