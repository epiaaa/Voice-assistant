from speech.text2audio import text_to_audio, audio_to_text
from AI import *

DeepSeek_API_Key = 'sk-8735744e32f04635af0caa27e341a60d'
DeepSeek_base_url = 'https://api.deepseek.com'


def get_data(prompt_element, ai, model='deepseek-chat', stream=False, print_content=True):
    # vehicle_num, phase_value, weather_name
    capacity_num = str(50)
    vehicle_num, phase_value, weather_name = prompt_element

    vehicle_num = str(vehicle_num)
    weather_name = str(weather_name)

    # question = input('你好，有什么问题？\n')
    question = ('已知条件：在雪天期间，车辆的平均加速度为0.5米/秒平方，车辆的平均减速为1.5米/秒平方，车辆的平均紧急减速约为2米/秒平方，平均延迟为0.5秒。'
                '由于这些指标可能会根据车辆数量和积雪程度而变化，因此它们会根据标准值产生偏差。'
                '若某车道车辆为' + vehicle_num + '，通行量为' + capacity_num + '，且在' + weather_name + '天气下，每车道通行量为' + capacity_num +
                '，则将平均加速、平均减速、平均紧急减速、平均延误四个指标按(将{value}替换为假设值，只允许一个值)的格式进行假设: '
                '[平均加速: {value}], [平均减速: {value}], [平均紧急减速: {value}], [平均时延: {value}]'
                )
    messages = [{'role': 'system', 'content': '你是一个乐于助人的助手，请严格按照格式输出'}, {'role': 'user', 'content': question}]
    reasoning_content, content = ai.get_response(messages, model=model, stream=stream, print_content=print_content)
    spl = split_data(content)
    save_prompt_data(question + '\n\n' + '最终结果：' + ' '.join(spl))
    print('结果：', spl)


def conversations(ai, model='deepseek-chat', stream=False):
    question = input('你好，有什么问题？\n')

    # messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    messages = []
    while question != 'exit':
        messages.append({'role': 'user', 'content': question})
        reasoning_content, content = ai.get_response(
            model=model,
            messages=messages,
            stream=stream,
            print_content=True
        )
        messages.append({'role': 'assistant', 'content': content})
        # with open('conversations.txt', 'a') as f:
        #     f.write('问：' + messages + '\n')
        #     f.write('思考：' + reasoning_content + '\n')
        #     f.write('回答：' + content + '\n')
        question = input('\n')
    print('对话结束')


'''a849310ffc310f9b6a5c36636a828b47'''
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

