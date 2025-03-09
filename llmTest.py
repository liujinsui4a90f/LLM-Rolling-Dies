from openai import OpenAI

client = OpenAI(api_key='sk-2533999e15524324b8854136ee786886', base_url='https://api.deepseek.com')

response = client.chat.completions.create(
    model='deepseek-chat',
    messages=[
        {'role' : 'system', 'content' : 'You are a helpful teacher'},
        {'role' : 'user', 'content' : 'can you tell me how to learn math'}
    ]
)

print(response.choices[0].message.content)