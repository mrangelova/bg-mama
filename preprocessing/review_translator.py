from googletrans import Translator


class ReviewTranslatorMixin:
    def translate(self):
        self.text = Translator().translate(self.text).text
