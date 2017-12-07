from googletrans import Translator


def translate(data, target_lang='bg'):
    translated_data = Translator().translate(data, dest=target_lang)
    return translated_data.text
