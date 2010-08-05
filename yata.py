import sys
from optparse import OptionParser
from sentenceParser import SentenceParser

class Yata:
    @staticmethod
    def run():

        usage = "usage: %prog --mode MODENAME --from LANG --to LANG --from-sentence SENTENCE --to-sentence SENTENCE ";
        parser = OptionParser(usage);

        #input mode
        parser.add_option(
            '--mode',
            dest="input_mode",
            choices=['true','false','question'],
            help="define the input mode",
            metavar="MODENAME"
        );

        # languages
        parser.add_option(
            '--from',
            dest="source_language",
            choices=['fra','eng'],
            help="define source language",
            metavar="LANG"
        );


        parser.add_option(
            '--to',
            dest="target_language",
            choices=['fra','eng'],
            help="define target language",
            metavar="LANG"
        );

        #sentences

        parser.add_option(
            '--from-sentence',
            dest="source_sentence",
            help="define source sentence",
            metavar="SENTENCE"
        );


        parser.add_option(
            '--to-sentence',
            dest="target_sentence",
            help="define target sentence",
            metavar="SENTENCE"
        );


        (options, args) = parser.parse_args();

        #check all mandatory options are here
        mandatories = [
            'target_language',
            'source_language',
            'input_mode',
            'target_sentence',
            'source_sentence'
        ];

        for m in mandatories:
            if not options.__dict__[m]:
                print("mandatory ", m, " option is missing\n");
                parser.print_help();
                exit(-1);

        source_parser = SentenceParser(options.source_language, options.source_sentence);
        source_parser.parse();
##

if __name__ == "__main__" :

    Yata.run();
