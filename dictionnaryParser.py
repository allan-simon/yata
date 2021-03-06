from xml.dom.minidom import parse
from inflecter import Inflecter
from word import Word
from itertools import count
from graph.base import Graph

import sys

class DictionnaryParser:

    def __init__ (self, lang):
        self._lang = lang;
        self._doml = parse(lang+"/dictionary.xml");
        self._inflectersDict = {};
        self._wordsDict = [];
        self._graph = Graph();
        self.parse_flections();
        self.parse_words();
    
    # Define language of the dictionnary
    @property
    def lang(self):
        return self._lang;

    @lang.setter
    def lang(self, lang):
        self._lang = lang;

    # In memory representation of the dictionnary.xml
    @property
    def doml(self):
        return self._doml;

    @doml.setter
    def doml(self, doml):
        self._doml = doml;

    # Python dict of inflecter's name : inflecter object
    @property
    def inflectersDict(self):
        return self._inflectersDict;


    # Python dict of words
    @property
    def wordsDict(self):
        return self._wordsDict;


    # Graph representation of the dictionnary
    @property
    def graph(self):
        return self._graph;

    def export_graph(self):
        from graph.extras import dot
        from subprocess import getstatusoutput

        # build the drawing tool
        drawer = dot.DotGenerator()

        # populate the output file
        with open('dot/dict.dot', 'w') as f:
            output = drawer.draw(self.graph, "dict_graph")
            f.write(output)

        getstatusoutput("circo -Tgif -o picture/dict/dict.gif -v dot/dict.dot")


    def generate_graph(self):
        i = 0;
        for word in self.wordsDict:
            # add the flexion
            self.graph.add_node(
                name=word.lemme_node_name(),
                node_type = "lemme",
                node_lemme = word.lemme,
                shape = "box",
                color = "red",
                node_word = word
            );

            if word.flection in self.inflectersDict:
                wordFlexions = self.inflectersDict[word.flection].inflecte(word);

                for tags, wordFlexion in wordFlexions.items():
                    if not wordFlexion in self.graph:
                        #if it's the first time we had this "form" we add the
                        #flexion node
                        self.graph.add_node(
                            name=wordFlexion,
                            node_type="flexion",
                            shape ="box",
                            color = "green",
                        );
                    edgeName = i;
                    
                    tempEdge = self.graph.add_edge(
                        wordFlexion,
                        word.lemme_node_name(),
                        name=edgeName,
                        tags=tags.split(" "),
                        is_directed=False
                    );

                    i = i + 1; 
        self.export_graph();
        #self.draw();

    def draw(self):
        dot = write(self.graph)
        #print(dot);

    def test(self):
        self.generate_graph();
        for word in self.wordsDict:
            if word.flection in self.inflectersDict:#.has_key(word.flection):
                self.inflectersDict[word.flection].inflecte(word);


    def parse_words(self):
        allWords = self.doml. getElementsByTagName("word");
        for wordNode in allWords:
            tempWord = self.generate_word(wordNode);
            self.wordsDict.append(tempWord);

    def parse_flections(self):
        allInflectionRules = self.doml. getElementsByTagName("flection_rule");
        for inflectionRule in allInflectionRules:
            name = inflectionRule.getAttribute('id');
            inflecter = self.generate_inflecter( inflectionRule);
            self.inflectersDict[name] = inflecter;

    def generate_word(self, wordNode):
        word = Word();
        kind = wordNode.attributes['type'].value;
        lemmeNode = wordNode.getElementsByTagName("lemme")[0]; 

        if lemmeNode.hasAttribute('flection'):
            word.flection = lemmeNode.getAttribute('flection')
        word.lemme = lemmeNode.childNodes[0].data;
        word.kind = kind;

        return word;

    # generate all flection from xml
    def generate_inflecter(self, inflecterNode):
        inflecter = Inflecter();
        for flection in inflecterNode.getElementsByTagName("flection"):
            tags = flection.getAttribute('type');
            # add all possible regexp
            for flection_regexp in flection.getElementsByTagName('flection_regexp'):
                #priority of the rule
                priority = int(flection_regexp.getAttribute('priority'));
                #matching regexp
                from_lemme = flection_regexp.getElementsByTagName('from_lemme')[0].childNodes[0].data;
                #resulting regexp
                to_flexion = flection_regexp.getElementsByTagName('to_flexion')[0].childNodes[0].data;
                inflecter.add_flection(tags, from_lemme, to_flexion, priority);
        return inflecter;

