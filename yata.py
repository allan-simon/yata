import sys
from optparse import OptionParser

class Yata:
    @staticmethod
    def run():

        usage = "usage: %prog --mode MODENAME --from LANG --to LANG --from-sentences SENTENCE --to-sentence SENTENCE ";
        parser = OptionParser(usage);

        #input mode
        parser.add_option(
            '--mode',
            dest="inputMode",
            choices=['true','false','question'],
            help="define the input mode",
            metavar="MODENAME"
        );

        # languages
        parser.add_option(
            '--from',
            dest="sourceLanguage",
            choices=['fra','eng'],
            help="define source language",
            metavar="LANG"
        );


        parser.add_option(
            '--to',
            dest="targetLanguage",
            choices=['fra','eng'],
            help="define target language",
            metavar="LANG"
        );

        #sentences

        parser.add_option(
            '--from-sentence',
            dest="sourceSentence",
            help="define source sentence",
            metavar="SENTENCE"
        );


        parser.add_option(
            '--to-sentence',
            dest="targetSentence",
            help="define target sentence",
            metavar="SENTENCE"
        );


        (options, args) = parser.parse_args();

        #check all mandatory options are here
        mandatories = [
            'targetLanguage',
            'sourceLanguage',
            'inputMode',
            'targetSentence',
            'sourceSentence'
        ];

        for m in mandatories:
            if not options.__dict__[m]:
                print "mandatory option is missing\n";
                parser.print_help();
                exit(-1);

        print options.sourceSentence;
        print options.targetSentence;

##

if __name__ == "__main__" :

    Yata.run();
