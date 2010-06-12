from dictionnaryParser import DictionnaryParser
from lexer import Lexer

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


    def parse(self):
        dictParser = DictionnaryParser(self.lang);
        dictParser.generate_graph();
        words = self.original_text.split(" ");

        decomposedWords = [];
        for word in words:
            try :
                dictParser.graph[word];
            except KeyError:
                #if we face an unknown word we mark it 
                decomposedWords.append((word,"unknown"));
                continue;
            decompositions = Lexer.analyse_word(word, dictParser.graph)
            decomposedWords.append((word,decompositions))
        print( decomposedWords);

