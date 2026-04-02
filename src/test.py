from ollama import chat

response = chat(
    model='qwen3.5',
    messages=[{'role': 'user', 'content': '안녕?'}],
)
print(response.message.content)