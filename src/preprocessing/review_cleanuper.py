import re


class ReviewCleanuperMixin:
    SPECIAL_CHARACTERS = [
        ",", ":", "\"", "=", "&", ";", "%", "$", "@", "%", "^", "*", "(", ")", "{", "}",
        "[", "]", "|", "/", "\\", ">", "<", "-", "!", "?", ".", "'", "--", "---", "#"
    ]
    URL_REGEX = r'http.?://[^\s]+[\s]?'
    NUMBERS_REGEX = r'\s?[0-9]+\.?[0-9]*'

    def cleanup(self):
        self.remove_urls()
        self.remove_special_characters()
        self.remove_numbers()

    def remove_urls(self):
        self.text = re.sub(ReviewCleanuperMixin.URL_REGEX, '', self.text)

    def remove_special_characters(self):
        for character in ReviewCleanuperMixin.SPECIAL_CHARACTERS:
            self.text = re.sub(re.escape(character), '', self.text)

    def remove_numbers(self):
        self.text = re.sub(ReviewCleanuperMixin.NUMBERS_REGEX, '', self.text)
