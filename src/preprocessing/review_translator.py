from googletrans import Translator


class ReviewTranslatorMixin:
    def translate(self, src, dest):
        self.text = Translator().translate(self.text, src, dest).text
