import sys
import logging
from optparse import OptionParser
from sentenceAnalyser import SentenceAnalyser


class Yata:
	"""This class is the entry point for yata command line."""

	@staticmethod
	def run():

		usage = "usage: %prog --mode MODENAME --from LANG --to LANG --from-sentence SENTENCE --to-sentence SENTENCE "
		parser = OptionParser(usage)

		#input mode
		parser.add_option(
			'--mode',
			dest="input_mode",
			choices=['true','false','question'],
			help="define the input mode",
			metavar="MODENAME"
		)

		# languages
		parser.add_option(
			'--from',
			dest="source_language",
			choices=['fra','eng'],
			help="define source language",
			metavar="LANG"
		)


		parser.add_option(
			'--to',
			dest="target_language",
			choices=['fra','eng'],
			help="define target language",
			metavar="LANG"
		)

		#sentences

		parser.add_option(
			'--from-sentence',
			dest="source_sentence",
			help="define source sentence",
			metavar="SENTENCE"
		)


		parser.add_option(
			'--to-sentence',
			dest="target_sentence",
			help="define target sentence",
			metavar="SENTENCE"
		)

		# debug
		parser.add_option(
			'-d', '--debug',
			action='store_true',
			dest="debug",
			default=False,
			help="Display debug messages"
		)

		(options, args) = parser.parse_args()

		#check all mandatory options are here
		mandatories = [
			'target_language',
			'source_language',
			'input_mode',
			'target_sentence',
			'source_sentence'
		]

		for m in mandatories:
			if not options.__dict__[m]:
				print("mandatory ", m, " option is missing\n")
				parser.print_help()
				exit(-1)

		# logging
		ch = logging.StreamHandler()
		if options.debug:
			ch.setLevel(logging.DEBUG)
		else:
			ch.setLevel(logging.ERROR)

		formatter = logging.Formatter('%(levelname)s - %(name)s : %(message)s')
		ch.setFormatter(formatter)

		logger = logging.getLogger('yata')
		logger.setLevel(logging.DEBUG)
		logger.addHandler(ch)

		logger.debug('You run in debug mode.')

		# Launch the analyse of the sentence
		SentenceAnalyser.run(options)
##

if __name__ == "__main__" :

	Yata.run()

