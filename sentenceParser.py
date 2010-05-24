
class SentenceParser:

    def __init__ (self, lang, text):
        self._lang = lang;
        self._original_text = text;


    @property
    def lang(self):
        return self._lang;

    @lang.setter
    def lang(self, lang):
        self._lang = lang;

    @property
    def original_text(self):
        return self._original_text;

    @original_text.setter
    def original_text(self, original_text):
        self._original_text = original_text;

