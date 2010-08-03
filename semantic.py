###
### In research phase by Biptaste
###

from sentenceParser import SentenceParser

class Semantic:

	def __init__ (self):
		return;

	def semantic(self):
		source_parser = SentenceParser('fra', 'pomme est un nom');
		source_parser.parse();
		
		if source_parser.decomposedWords[1][0] == 'est' and source_parser.decomposedWords[2][0] == 'un':

			print(source_parser.decomposedWords[0][0], ' : ',source_parser.decomposedWords[3][0]);

