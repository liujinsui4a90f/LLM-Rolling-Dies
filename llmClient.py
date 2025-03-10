from openai import OpenAI

try:
    with open('API-KEY', 'r') as f:
        APIKEY = f.readline()
except FileNotFoundError as e:
    print("API key cannot found!")
    print("Please put your API key in file \"API-KEY\" under the same path as \"game.py\". ")
    exit()

class LLMClient:
    def __init__(self, model : str):
        self.model = model
        self.client = OpenAI(api_key=APIKEY, base_url='https://api.mindcraft.com.cn/v1')

    def response(self, prompt : str) -> str:
        response = self.client.chat.completions.create(model='deepseek-chat',
                                            messages=[
                                                {'role' : 'user', 'content' : prompt}
                                            ])
        if response.status != 200:
            raise RuntimeError(f"Didn't get response from {self.model}.")
        return response.choices[0].message.content
        
