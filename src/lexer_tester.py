from lexer import imp_lex
import sys

def generate(tokens):
	for token in tokens: 
		yield token


def test(filename):
	global gen
	file = open(filename)
	characters = file.read()
	file.close()
	tokens = imp_lex(characters)
	gen = generate(tokens)
	return gen

gen = None

def printNext(gen):
	token = next(gen)
	print(token[0], "\t-->\t", token[1].name)