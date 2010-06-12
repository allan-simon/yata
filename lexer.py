import sys
from optparse import OptionParser
from dictionnaryParser import DictionnaryParser
from graph.base import Graph


class Lexer:
    @staticmethod
    def run():

        usage = "usage: %prog --word ";
        parser = OptionParser(usage);

        #input mode
        parser.add_option(
            '--word',
            dest="flexion",
            help="the word to decompose",
            metavar="WORD"
        );

        (options, args) = parser.parse_args();

        dictParser = DictionnaryParser("fra");
        dictParser.generate_graph();
        flexion = options.flexion;

        print(Lexer.analyse_word(flexion, dictParser.graph));

    @staticmethod
    def analyse_word(flexion, graph):
        flexionNode = graph[flexion];
        possibleDecompositions = [];
        for edge in flexionNode.outgoing:
            otherEndNode = edge.other_end(flexionNode);
            if otherEndNode.node_type is "lemme":
                word = otherEndNode.node_word ;
                decomposedWord = {
                    "lemme" : word.lemme,
                    "kind"  : word.kind,
                    "tags"  : edge.tags
                };
                possibleDecompositions.append(decomposedWord);
        return possibleDecompositions;


if __name__ == "__main__" :

    Lexer.run();

