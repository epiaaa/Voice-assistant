from openai import OpenAI
import random
import re
import time


class Conversation:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def set_values(self, veichle_num, capacity):
        self.veichle_num = veichle_num
        self.capacity = capacity

    def get_weather(self):
        choice = ['heavy snowy', 'middle snowy', 'snowy with rain', 'sunny']
        value = [0.25, 0.5, 0.75, 0.99]
        index = random.randint(0, len(choice) - 1)
        weather_type = choice[index]
        weather_value = value[index]

        return weather_type, weather_value

    def get_response(self, messages, model='deepseek-chat', stream=False, print_content=False):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream
            )
        except Exception as e:
            print(f"请求错误: Conversation.get_response：{e}")
            exit()
        reasoning_content = ''
        content = ''

        if stream:
            for chunk in response:
                if model == 'deepseek-reasoner' and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                    if print_content:
                        print(chunk.choices[0].delta.reasoning_content, end='')
                elif chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    if print_content:
                        print(chunk.choices[0].delta.content, end='')
            print('\n')
        else:
            if model == 'deepseek-reasoner':
                reasoning_content = response.choices[0].message.reasoning_content
            content = response.choices[0].message.content
            if print_content:
                print(reasoning_content)
                print(content)
        # print(response)
        return reasoning_content, content

    def conversation(self, user_input, messages=None, model='deepseek-chat', stream=False, print_content=False):
        if messages is None:
            messages = [{'role': 'system', 'content': '你是一个乐于助人的助手。'}, {'role': 'user', 'content': user_input}]
        else:
            messages.append({'role': 'user', 'content': user_input})
        print('正在思考...')
        get_response = self.get_response(messages, model=model, stream=stream, print_content=print_content)
        return get_response[1], messages

    def conversations(self, messages=None, model='deepseek-chat', stream=False, print_content=False):
        pass


def check_string(string):
    pattern = r'^\d.*\..*$'
    if re.match(pattern, string):
        return True
    else:
        return False


def split_data(raw):
    # line_array = raw.replace("[", "").replace("]", "").split(",")
    record_value = re.findall(r'\[.*?: (\d+\.?\d*)\]', raw)
    # record_value = []
    # for i in range(len(line_array)):
    #     result = line_array[i].split(':')[1].strip()
    #
    #     if check_string(result):
    #         result = result[:-1]
    #         print('res', result)
    #     if result.startswith("{") and result.endswith("}"):
    #         result = result.replace("{", "").replace("}", "")
    #     result = float(result)
    #
    #     print(result)
    #     record_value.append(result)

    return record_value


# @lru_cache()
def save_prompt_data(data):
    formatter_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    path = f"./prompt_data/{formatter_time}.txt"
    with open(path, mode='a+') as save_e:
        save_e.write(data)
        save_e.write("\n")


# test = ('根据已知条件和题目要求，假设在heavy snowy天气下，每车道通行量为50，车辆数量为10的情况下，四个指标的假设值如下:\n'
#         '\n'
#         '- [平均加速: 0.4]\n'
#         '- [平均减速: 1.4]\n'
#         '- [平均紧急减速: 1.8]\n'
#         '- [平均时延: 0.6]\n'
#         '\n'
#         '这些值是基于标准值并根据车辆数量和积雪程度进行了适当调整的假设值。')
#
# split_data(test)

