import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("请开始说话...")
        audio = r.listen(source, phrase_time_limit=10)

    print("停止说话...")
    try:
        print("识别中...")
        text = r.recognize_google(audio, language='zh-CN')

        print(f"识别结果：{text}")
        return text
    except sr.UnknownValueError:
        return "无法识别音频"
    except sr.RequestError:
        return "服务不可用"


def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='zh-cn')
        tts.save("response.mp3")

        # 播放音频
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        os.remove("response.mp3")
    except Exception as e:
        print(f"语音合成失败：{str(e)}")


if __name__ == "__main__":
    print("This is gtts_speech.py")
    text = speech_to_text()
    print(text)
