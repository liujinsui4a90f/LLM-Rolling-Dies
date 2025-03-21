# LLM-Rolling-Dies
简体中文 | [English](./README-EN.md)

本项目是一个由LLM驱动的摇色子模拟程序。

## 配置

1. 使用conda或其他环境管理工具，安装相应依赖：
```
pip install openai
```

2. 在[MindCraft](https://www.mindcraft.com.cn/)创建账号，并生成API Key。
3. 在项目根目录创建`API-KEY`文件，并将生成的API key粘贴到里面。
4. 本项目将`deepseek-chat`、`qwen-max-latest`、`Doubao-1.5-pro-256k`和`GLM-4-Flash`四个模型设为默认玩家。若用户想使用其他模型，请参考MindCraft[文档](https://apifox.com/apidoc/shared-0fd7ea54-919e-4c93-b673-c60219bc82e0/api-199055738)中支持的模型。


## 使用
### 运行游戏
运行`main.py`进行一局游戏。
```sh
python main.py
```
执行
```python
python main.py -n x
```
以运行多局游戏，`x`为局数。

### 记录转换
执行
```python
python record_convert.py
```
以将游戏记录由json格式转换为易读的文本格式。

### 游戏统计
执行
```python
python analyse.py
```
以统计游戏结果。`analyse.py`在被执行时，会自动读取`./record`目录下的所有json文件，并进行统计。


## 已知问题
- 当LLM的叫数不符合规则时，会在prompt中加入上次叫数违反的具体规则，并重新生成叫数，会在一定程度上会干扰AI的判断。用户可以选择优化prompt来增强AI的推理能力 (也有可能会削弱)。
- 在python 3.10下运行时，会出现奇怪的f-string报错，使用python 3.12无此问题。

## 鸣谢

本项目受[LYiHub](https://github.com/LYiHub/)的[Liars Bar LLM](https://github.com/LYiHub/liars-bar-llm)项目启发。在此向[LYiHub](https://github.com/LYiHub/)鸣谢。

本项目使用[MindCraft](https://www.mindcraft.com.cn/)配置了统一的API调用接口。在此向[MindCraft](https://www.mindcraft.com.cn/)鸣谢。


