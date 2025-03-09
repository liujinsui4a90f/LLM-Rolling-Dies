from openai import OpenAI

client = OpenAI(api_key='MC-7A9D14B972BE45EE8445E0BFAF4A1D52', base_url='https://api.mindcraft.com.cn/v1')

response = client.chat.completions.create(
    model='deepseek-chat',
    messages=[
        {'role' : 'user', 'content' : 'Hello!'}
    ]
)

print(response.choices[0].message.content)