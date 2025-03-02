import time
import pyaudio
import wave
import requests
import numpy as np
import speech_recognition as sr


def text_get_wav(text):
    json = {
        "text": text,
        "text_language": "zh",
        "cut_punc": "， 。",
        "refer_wav_path": r"G:\Python\Tool\Conversations\ref_audio\克拉拉.wav",
        "prompt_language": "zh",
        "prompt_text": "娜塔莎姐姐说克拉拉也是医生呢，是机器伙伴的医生。"
    }
    url = 'http://localhost:9880'
    response = requests.get(url, params=json)
    # print(response.url)
    # print(response.status_code)
    # print(response.content)
    with open('./response.wav', 'wb') as f:
        f.write(response.content)


def play_wav(file_path):
    # 打开WAV文件
    wf = wave.open(file_path, 'rb')

    # 初始化PyAudio
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 读取数据
    data = wf.readframes(1024)

    # 播放音频
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # 停止和关闭流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()


def text_to_audio(text):
    text_get_wav(text)
    print(text)
    play_wav('./response.wav')


def record_wav(filename, silence_threshold=500, silence_duration=1.5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print('开始录音...')
    time.sleep(0.5)
    frames = []
    silence_counter = 0
    chunk_samples = CHUNK // 2
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # 将字节数据转换为整数数组
        samples = np.frombuffer(data, dtype=np.int16)

        # 计算当前音频块的能量
        current_rms = np.sqrt(np.mean(samples ** 2))

        if current_rms < silence_threshold:
            silence_counter += 1
            if silence_counter > (RATE / CHUNK * silence_duration):
                break
        else:
            silence_counter = 0
    print('录音结束...')
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as f:
        f.setnchannels(CHANNELS)
        f.setsampwidth(p.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(b''.join(frames))


def recognize_wav(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
    try:
        print("识别中...")
        text = r.recognize_google(audio_data, language='zh-CN')
        print(f"识别结果：{text}")
        return text
    except sr.UnknownValueError:
        return "无法识别音频"
    except sr.RequestError:
        return "服务不可用"


def audio_to_text(filename):
    record_wav(filename)
    return recognize_wav(filename)


if __name__ == '__main__':
    audio_to_text('test.wav')
