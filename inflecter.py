import re
from word import Word

class Inflecter:

    def __init__(self):

        self._flections = {};

    @property
    def flections(self):
        return self._flections


    def add_flection(self, tags, from_lemme, to_flexion, priority):
        if not  tags in self.flections: #.has_key(tags):
            self.flections[tags] = [];
        self.flections[tags].insert(priority, (from_lemme, to_flexion));

    def inflecte (self, word):
        lemme = word.lemme;
        wordFlexionsDict = {}
        for tags, flection_regexps in self.flections.items():
            for from_regexp, to_regexp in flection_regexps:
                if not re.match(from_regexp, lemme):
                    break;
                stemme = re.sub(from_regexp, to_regexp, lemme);
            wordFlexionsDict[tags] = stemme;
        return wordFlexionsDict;



