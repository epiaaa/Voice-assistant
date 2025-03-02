import pyttsx3


def text_to_speech(text, voice='zh', save=False):
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()
    if save:
        engine.save_to_file(text, 'test.mp3')
        engine.runAndWait()


if __name__ == '__main__':
    text = ('我个人认为，这个意大利面就应该拌42号混凝土，因为这个螺丝钉的长度，'
            '它很容易会直接影响到挖掘机的扭矩你知道吧。你往里砸的时候，一瞬间它'
            '就会产生大量的高能蛋白，俗称ufo，会严重影响经济的发展，甚至对整个太'
            '平洋以及充电器都会造成一定的核污染。你知道啊？再者说，根据这个勾股'
            '定理，你可以很容易地推断出人工饲养的东条英机，它是可以捕获野生的三'
            '角函数的，所以说这个秦始皇的切面是否具有放射性啊。特朗普的N次方是否'
            '含有沉淀物，都不影响这个沃尔玛跟维尔康在南极会合。')
    text_to_speech(text)
