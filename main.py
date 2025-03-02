from speech.convert_text_and_speech import text_to_audio, audio_to_text
from AI import *

DeepSeek_API_Key = '' # 官网的API_Key
DeepSeek_base_url = 'https://api.deepseek.com'

# model = deepseek-chat / deepseek-reasoner
if __name__ == '__main__':
    my_ai = Conversation(DeepSeek_API_Key, DeepSeek_base_url)
    print("epi_，仅供娱乐")
    text_to_audio('你好，有什么需要帮忙的吗？')
    messages = None
    while True:
        text = audio_to_text('response.wav')
        if text not in ['无法识别音频', '服务不可用']:
            context, messages = my_ai.conversation(text, messages=messages)
            messages.append({'role': 'assistant', 'content': context})
        else:
            context = text
        text_to_audio(context)

