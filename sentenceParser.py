from dictionnaryParser import DictionnaryParser
from lexer import Lexer

"""This class decompose sentence in a list of tagged word."""

class SentenceParser:

	def __init__ (self, lang, text):
		self._lang = lang
		self._original_text = text
		self._decomposedWords = []


	@property
	def lang(self):
		return self._lang

	@lang.setter
	def lang(self, lang):
		self._lang = lang

	@property
	def original_text(self):
		return self._original_text

	@original_text.setter
	def original_text(self, original_text):
		self._original_text = original_text

	@property
	def decomposedWords(self):
		return self._decomposedWords 


	def parse(self):
		"""Decompose the sentence."""

		dictParser = DictionnaryParser(self.lang)
		dictParser.generate_graph()
		words = self.original_text.split(" ")

		#decomposedWords = []
		for word in words:
			try :
				dictParser.graph[word]
			except KeyError:
				#if we face an unknown word we mark it 
				self._decomposedWords.append((word,"unknown"))
				continue
			decompositions = Lexer.analyse_word(word, dictParser.graph)
			self._decomposedWords.append((word,decompositions))

		# debug message
		print( self._decomposedWords)


