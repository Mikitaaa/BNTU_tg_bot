from google import genai
from Config_handler import load_config

config = load_config('config.txt')

client = genai.Client(api_key=config['api_key'])

def getTextResponse(user_message: str) -> str:
    prompt_message = config['prompt_message'].format(user_message=user_message)
    #messages = [{"role": "user", "content": prompt_message}]
    print(prompt_message)

    try:
        response = client.models.generate_content(
             model="gemini-2.5-flash", contents=prompt_message)
        
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Ошибка при запросе к модели: {e}")
        return "Хз что сказать"
