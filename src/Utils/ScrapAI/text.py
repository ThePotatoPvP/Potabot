import random
import poe

def generate_gpt4_response(prompt):
    response = "Pong"
    token = random.choice(open('./src/Utils/ScrapAI/poe_tokens.txt', 'r', encoding='utf-8').read().splitlines())
    client = poe.Client(token.split(':')[0])
    completion = client.send_message('beaver', prompt, with_chat_break=True)
    response = ''.join(token['text_new'] for token in completion)

    return response