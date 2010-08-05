import sys
from optparse import OptionParser
from dictionnaryParser import DictionnaryParser
from graph.base import Graph


class Generator:
    @staticmethod
    def run():

        usage = "usage: %prog --lemme LEMME [ --tags TAG1[,TAG2...]]";
        parser = OptionParser(usage);

        #input mode
        parser.add_option(
            '--lemme',
            dest="lemme",
            help="the lemme to inflect",
            metavar="LEMME"
        );

        parser.add_option(
            '--tags',
            dest="tagsArg",
            help="the tags, separated by comma",
            metavar="TAG"
        );



        (options, args) = parser.parse_args();


        dictParser = DictionnaryParser("fra");
        dictParser.generate_graph();

        lemme = options.lemme;
        tags = set(options.tagsArg.split(','));
        print(Generator.generate_word(lemme, tags, dictParser.graph));

    @staticmethod
    def generate_word(lemme, tags, graph):
        possibleFlexions = [];
        for lemmeNode in graph.search_nodes(node_type = "lemme", node_lemme = lemme):
            word = lemmeNode.node_word
            for edge in lemmeNode.outgoing:
                edgeTagsSet = set(edge.tags);
                tagsSet = set(tags)
                #if all the tags asked are include in the edge tags
                #then we add this flexion to the list of possible 
                #flexion
                if tagsSet - edgeTagsSet == set():
                    flexionNode = edge.other_end(lemmeNode);
                    inflectedWord = {
                        'flexion' : flexionNode.name,
                        'tags' : edgeTagsSet
                    }
                    possibleFlexions.append(inflectedWord)
        return possibleFlexions

if __name__ == "__main__" :
    Generator.run();

