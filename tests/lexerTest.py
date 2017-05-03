import unittest

if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from src.lexer import *


def run_lexer(code):
	lexer = Lexer()
	return lexer.cpp_lex(code)

class TestLexer(unittest.TestCase):
	def test_keyword_int(self):
		code = 'int'
		tokens = [Token(TokenType.Int, 'int')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_long(self):
		code = 'long'
		tokens = [Token(TokenType.Long, 'long')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_float(self):
		code = 'float'
		tokens = [Token(TokenType.Float, 'float')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_double(self):
		code = 'double'
		tokens = [Token(TokenType.Double, 'double')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_char(self):
		code = 'char'
		tokens = [Token(TokenType.Char, 'char')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_bool(self):
		code = 'bool'
		tokens = [Token(TokenType.Bool, 'bool')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_break(self):
		code = 'break'
		tokens = [Token(TokenType.Break, 'break')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_class(self):
		code = 'class'
		tokens = [Token(TokenType.Class, 'class')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_continue(self):
		code = 'continue'
		tokens = [Token(TokenType.Continue, 'continue')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_else(self):
		code = 'else'
		tokens = [Token(TokenType.Else, 'else')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_false(self):
		code = 'false'
		tokens = [Token(TokenType.False_, 'false')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_for(self):
		code = 'for'
		tokens = [Token(TokenType.For, 'for')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_if(self):
		code = 'if'
		tokens = [Token(TokenType.If, 'if')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_private(self):	
		code = 'private'
		tokens = [Token(TokenType.Private, 'private')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_protected(self):
		code = 'protected'
		tokens = [Token(TokenType.Protected, 'protected')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_public(self):
		code = 'public'
		tokens = [Token(TokenType.Public, 'public')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_return(self):
		code = 'return'
		tokens = [Token(TokenType.Return, 'return')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_true(self):
		code = 'true'
		tokens = [Token(TokenType.True_, 'true')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_void(self):
		code = 'void'
		tokens = [Token(TokenType.Void, 'void')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_keyword_while(self):
		code = 'while'
		tokens = [Token(TokenType.While, 'while')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)





	def test_comma(self):
		code = ','
		tokens = [Token(TokenType.Comma, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)


	def test_left_bracket(self):
		code = '{'
		tokens = [Token(TokenType.LBracket, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_right_bracket(self):
		code = '}'
		tokens = [Token(TokenType.RBracket, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_dot(self):
		code = '.'
		tokens = [Token(TokenType.Dot, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_equals(self):
		code = '=='
		tokens = [Token(TokenType.Equals, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_assign(self):
		code = '='
		tokens = [Token(TokenType.Assign, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_open_paranthesis(self):
		code = '('
		tokens = [Token(TokenType.OpenParanthesis, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_close_paranthesis(self):
		code = ')'
		tokens = [Token(TokenType.CloseParanthesis, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_semicolon(self):
		code = ';'
		tokens = [Token(TokenType.SemiColon, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_colon(self):
		code = ':'
		tokens = [Token(TokenType.Colon, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_plus(self):
		code = '+'
		tokens = [Token(TokenType.Plus, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_minus(self):
		code = '-'
		tokens = [Token(TokenType.Minus, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_asterix(self):
		code = '*'
		tokens = [Token(TokenType.Asterix, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_slash(self):
		code = '/'
		tokens = [Token(TokenType.Slash, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_less_or_equal(self):
		code = '<='
		tokens = [Token(TokenType.LessOrEqual, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_greater_or_equal(self):
		code = '>='
		tokens = [Token(TokenType.GreaterOrEqual, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_less_than(self):
		code = '<'
		tokens = [Token(TokenType.LessThan, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_greater_than(self):
		code = '>'
		tokens = [Token(TokenType.GreaterThan, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_differs(self):
		code = '!='
		tokens = [Token(TokenType.Differs, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_or(self):
		code = '||'
		tokens = [Token(TokenType.Or, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_and(self):
		code = '&&'
		tokens = [Token(TokenType.And, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_not(self):
		code = '!'
		tokens = [Token(TokenType.Not, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)



	def test_float_typical(self):
		code = '124.02'
		tokens = [Token(TokenType.FloatNum, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_float_with_0_fraction(self):
		code = '124.0'
		tokens = [Token(TokenType.FloatNum, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_float_0(self):
		code = '0.0'
		tokens = [Token(TokenType.FloatNum, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)


	def test_int_typical(self):
		code = '125459'
		tokens = [Token(TokenType.IntNum, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_int_0(self):
		code = '0'
		tokens = [Token(TokenType.IntNum, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)


	def test_char_typical(self):
		code = "'a'"
		tokens = [Token(TokenType.Character, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_char_tab(self):
		code = "'\t'"
		tokens = [Token(TokenType.Character, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_char_two_letters_not_allowed(self):
		code = "'ab'"
		
		with self.assertRaises(LexError):
			run_lexer(code)

	def test_char_new_line_not_allowed(self):
		code = "'\n'"

		with self.assertRaises(LexError):
			run_lexer(code)



	def test_id_simple(self):
		code = "my_var"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_id_starting_with_keyword(self):
		code = "intx"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_id_containing_keyword(self):
		code = "xintx"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_id_ending_with_keyword(self):
		code = "xint"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)
	
	def test_id_starting_and_ending_with_underscore(self):
		code = "_myvar_"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)



	def test_invalid_sign_hash(self):
		code = "#"

		with self.assertRaises(LexError):
			run_lexer(code)

	def test_invalid_sign_backslash(self):
		code = "\\"
		
		with self.assertRaises(LexError):
			run_lexer(code)

	def test_invalid_quotation(self):
		code = '"h"'
		
		with self.assertRaises(LexError):
			run_lexer(code)

	"""
	def test_id_starting_and_ending_with_underscore(self):
		code = "_myvar_"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_id_starting_and_ending_with_underscore(self):
		code = "_myvar_"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)
	"""

	def test_id_followed_by_paranthesis_without_whitespaces(self):
		code = "x()"
		tokens = [Token(TokenType.Identifier, 'x'), Token(TokenType.OpenParanthesis, '('),
			Token(TokenType.CloseParanthesis, ')')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_ids_separated_by_comma(self):
		code = "x,y"
		tokens = [Token(TokenType.Identifier, 'x'), Token(TokenType.Comma, ','),
			Token(TokenType.Identifier, 'y')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_declaration_with_whitespaces(self):
		code = "int x 	=       5 ;"
		tokens = [Token(TokenType.Int, 'int'), Token(TokenType.Identifier, 'x'), \
			Token(TokenType.Assign, '='), Token(TokenType.IntNum, '5'), Token(TokenType.SemiColon, ';')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_declaration_without_whitespaces(self):
		code = "int x=5;"
		tokens = [Token(TokenType.Int, 'int'), Token(TokenType.Identifier, 'x'), \
			Token(TokenType.Assign, '='), Token(TokenType.IntNum, '5'), Token(TokenType.SemiColon, ';')]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

	def test_id_starting_and_ending_with_underscore(self):
		code = "_myvar_"
		tokens = [Token(TokenType.Identifier, code)]

		result = run_lexer(code)

		self.assertEqual(tokens, result)

if __name__ == '__main__':
	unittest.main()