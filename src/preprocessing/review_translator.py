from googletrans import Translator


class ReviewTranslatorMixin:
    def translate(self, dest, src):
        self.text = Translator().translate(self.text, dest, src).text
