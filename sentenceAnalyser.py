from sentenceParser import SentenceParser
from grammarParser import GrammarParser
from grammarTagger import GrammarTagger


class SentenceAnalyser:
	"""This class is the proccess to analyse a sentence """

	@staticmethod
	def run(options):
		sourceParser = SentenceParser(options.source_language, options.source_sentence)
		sourceParser.parse()
		
		grammarParser = GrammarParser(options.source_language)
		grammarParser.parse_doml()

		grammarTagger = GrammarTagger(grammarParser.graph)
		grammarTagger.tag(['nom_propre','verbe','determinant','nom_commun','determinant','groupe_nominal'])


