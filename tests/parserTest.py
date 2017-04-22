import unittest

if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from src.parser import *
    from src.lexer import *
    from src.my_ast import *


def createParser(code):
	lexer = Lexer()
	tokens = lexer.imp_lex(code)
	parser = Parser(tokens)
	return parser

class TestParser(unittest.TestCase):
	def test_simple_AEXP(self):
		code = '2+x'
		result = BinopAexp(IntNum('2'), '+', Identifier('x'))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_longer_AEXP(self):
		code = '2+4-x*2+5/5'
		result = BinopAexp(BinopAexp(BinopAexp(IntNum(2), '+', IntNum(4)), '-', \
			BinopAexp(Identifier('x'), '*', IntNum(2))), '+', BinopAexp(IntNum(5), '/', IntNum(5)))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_paranthesis_AEXP(self):
		code = '2+(2-x)'
		result = BinopAexp(IntNum('2'), '+', BinopAexp(IntNum(2), '-', Identifier('x')))

		parser = createParser(code)		
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_paranthesis_and_order_AEXP(self):
		code = '2*(2-x)'
		result = BinopAexp(IntNum(2), '*', BinopAexp(IntNum(2), '-', Identifier('x')))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_paranthesis_and_order_v2_AEXP(self):
		code = '(2-3)*x'
		result = BinopAexp(BinopAexp(IntNum(2), '-', IntNum(3)), '*', Identifier('x'))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_many_paranthesis_AEXP(self):
		code = '(2+5)-(1+2)*(2-2)'
		result = BinopAexp(BinopAexp(IntNum(2), '+', IntNum(5)), '-', BinopAexp(BinopAexp( \
			IntNum(1), '+', IntNum(2)), '*', BinopAexp(IntNum(2), '-', IntNum(2))))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	def test_nested_paranthesis(self):
		code = '1*(2*(3-1)/(4-2))'
		result = BinopAexp(IntNum(1), '*', BinopAexp(BinopAexp(IntNum(2), '*', BinopAexp(IntNum(3), \
			'-', IntNum(1))), '/', BinopAexp(IntNum(4), '-', IntNum(2))))

		parser = createParser(code)
		ast = parser.aexp()

		self.assertEqual(ast, result)

	"""
	def test_error_AEXP(self):
		code = '1+2*'		
		parser = createParser(code)
		ast = parser.aexp()"""



	def test_simple_BEXP(self):
		code = 'false || true'
		result = OrBexp(BoolLit('false'), BoolLit('true'))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_long_BEXP(self):
		code = 'true || false && true && true'
		result = OrBexp(BoolLit('true'), AndBexp(AndBexp(BoolLit('false'), BoolLit('true')), BoolLit('true')))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_conditions_BEXP(self):
		code = 'x < 2'
		result = RelopBexp(Identifier('x'), '<', IntNum(2))


		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_paranthesis_BEXP(self):
		code = '(false || true)'
		result = OrBexp(BoolLit('false'), BoolLit('true'))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_paranthesis_and_order_BEXP(self):
		code = 'true && (false || true)'
		result = AndBexp(BoolLit('true'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_paranthesis_and_order_v2_BEXP(self):
		code = '(false || true) && true'
		result = AndBexp(OrBexp(BoolLit('false'), BoolLit('true')), BoolLit('true'))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_many_paranthesis_BEXP(self):
		code = '(false || true) && (false || true && true)'
		result = AndBexp(OrBexp(BoolLit('false'), BoolLit('true')), OrBexp(BoolLit('false'), \
		 	AndBexp(BoolLit('true'), BoolLit('true'))))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_nested_paranthesis_BEXP(self):
		code = '(true || (x<2 && y>3 || (true && false)))'
		result = OrBexp(BoolLit('true'), OrBexp(AndBexp(RelopBexp(Identifier('x'), '<', IntNum(2)), \
			RelopBexp(Identifier('y'), '>', IntNum(3))), AndBexp(BoolLit('true'), BoolLit('false'))))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_simple_negation_BEXP(self):
		code = '!false'
		result = NotBexp(BoolLit('false'))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_negation_condition_BEXP(self):
		code = '!(x < 2)'
		result = NotBexp(RelopBexp(Identifier('x'), '<', IntNum(2)))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)

	def test_complex_BEXP(self):
		code = '!(true || !(x<2 && y>3 || (true && x==4))) || (y <= 2)'
		result = OrBexp(NotBexp(OrBexp(BoolLit('true'), NotBexp(OrBexp(AndBexp(RelopBexp( \
			Identifier('x'), '<', IntNum(2)), RelopBexp(Identifier('y'), '>', IntNum(3))), \
			AndBexp(BoolLit('true'), RelopBexp(Identifier('x'), '==', IntNum(4))))))), RelopBexp(\
			Identifier('y'), '<=', IntNum(2)))

		parser = createParser(code)
		ast = parser.bexp()

		self.assertEqual(ast, result)




	#TESTING ASSIGNMENT
	def test_assign_literal(self):
		code = 'x = 5'
		result = AssignExp(Identifier('x'), IntNum(5))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)

	def test_assign_identifier(self):
		code = 'x = y'
		result = AssignExp(Identifier('x'), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)

	def test_assign_aexp(self):
		code = 'x = 2 + 4'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)

	def test_assign_aexp_paranthesis(self):
		code = 'x = (2 + 4)'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)

	def test_assign_bexp(self):
		code = 'x = false || true'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)

	def test_assign_bexp_paranthesis(self):
		code = 'x = (false && true)'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseExp()

		self.assertEqual(ast, result)




	#TESTING DECLARATIONS
	def test_declare_without_assignment(self):
		code = 'int x'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), None)

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)


	def test_declare_with_literal(self):
		code = 'int x = 5'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(5))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_declare_with_identifier(self):
		code = 'int x = y'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_declare_with_aexp(self):
		code = 'int x = 2 + 4'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_declare_with_aexp_paranthesis(self):
		code = 'int x = (2 + 4)'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_declare_with_bexp(self):
		code = 'int x = false || true'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_declare_with_bexp_paranthesis(self):
		code = 'int x = (false && true)'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)




	#TESTING ASSIGN STATEMENTS
	def test_stmt_assign_literal(self):
		code = 'x = 5;'
		result = AssignExp(Identifier('x'), IntNum(5))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_stmt_assign_identifier(self):
		code = 'x = y;'
		result = AssignExp(Identifier('x'), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_stmt_assign_aexp(self):
		code = 'x = 2 + 4;'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_stmt_assign_aexp_paranthesis(self):
		code = 'x = (2 + 4);'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_stmt_assign_bexp(self):
		code = 'x = false || true;'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_stmt_assign_bexp_paranthesis(self):
		code = 'x = (false && true);'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)




	#TEST DECLARATION STATEMENT
	def test_stmt_declare_without_assignment(self):
		code = 'int x;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), None)

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)


	def test_stmt_declare_with_literal(self):
		code = 'int x = 5;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(5))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_stmt_declare_with_identifier(self):
		code = 'int x = y;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_stmt_declare_with_aexp(self):
		code = 'int x = 2 + 4;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_stmt_declare_with_aexp_paranthesis(self):
		code = 'int x = (2 + 4);'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_stmt_declare_with_bexp(self):
		code = 'int x = false || true;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)

	def test_stmt_declare_with_bexp_paranthesis(self):
		code = 'int x = (false && true);'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseDecl()

		self.assertEqual(ast, result)


	#TEST WHILE LOOP
	def test_single_line_while_loop(self):
		code = 'while(x<5)1+1;'
		result = WhileStmt(RelopBexp(Identifier('x'), '<', IntNum(5)), BinopAexp(IntNum(1), '+', IntNum(1)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_while_loop_boolean_paranthesis(self):
		code = 'while(((x<5)&&(x!=2)))1+1;'
		result = WhileStmt(AndBexp(RelopBexp(Identifier('x'), '<', IntNum(5)), RelopBexp(Identifier('x'), \
			'!=', IntNum(2))), BinopAexp(IntNum(1), '+', IntNum(1)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_while_loop(self):
		code = 'while(x<2){int k=2;2+2;true&&false;}'
		result = WhileStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), CompoundStmt([Decl( \
			Param(TypeSpec('int'), Identifier('k')), IntNum(2)), BinopAexp(IntNum(2), '+', \
			IntNum(2)), AndBexp(BoolLit('true'), BoolLit('false'))]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_nested_while_loop(self):
		code = 'while(true)while(x<2)2+2;'
		result = WhileStmt(BoolLit('true'), WhileStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), \
			BinopAexp(IntNum(2), '+', IntNum(2))))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_while_loop_with_if_else(self):
		code = 'while(true)if(true)1;else 2;'
		result = WhileStmt(BoolLit('true'), IfStmt(BoolLit('true'), IntNum(1), IntNum(2)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)


	def test_while_loop_with_continue(self):
		pass

	def test_while_loop_with_break(self):
		pass



	#TEST COMPOUND STMT
	def test_simple_compound_stmt(self):
		code = '{2+2;}'
		result = CompoundStmt([BinopAexp(IntNum(2), '+', IntNum(2))])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_stmt_with_while(self):
		code = '{while(true)1;}'
		result = CompoundStmt([WhileStmt(BoolLit('true'), IntNum(1))])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_stmt_with_if(self):
		code = '{if(true)1;}'
		result = CompoundStmt([IfStmt(BoolLit('true'), IntNum(1), None)])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_stmt_with_if_else(self):
		code = '{if(true)1;else 2;}'
		result = CompoundStmt([IfStmt(BoolLit('true'), IntNum(1), IntNum(2))])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)



	#TEST SELECTION STATEMENT
	def test_single_line_if_stmt(self):
		code = 'if(x<5)1+1;'
		result = IfStmt(RelopBexp(Identifier('x'), '<', IntNum(5)), BinopAexp(IntNum(1), '+', IntNum(1)), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_if_stmt_boolean_paranthesis(self):
		code = 'if(((x<5)&&(x!=2)))1+1;'
		result = IfStmt(AndBexp(RelopBexp(Identifier('x'), '<', IntNum(5)), RelopBexp(Identifier('x'), \
			'!=', IntNum(2))), BinopAexp(IntNum(1), '+', IntNum(1)), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_if_stmt(self):
		code = 'if(x<2){int k=2;2+2;true&&false;}'
		result = IfStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), CompoundStmt([Decl(Param(TypeSpec('int'), \
		 	Identifier('k')), IntNum(2)), BinopAexp(IntNum(2), '+', IntNum(2)), AndBexp(BoolLit('true'), \
			BoolLit('false'))]), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_nested_if_stmt(self):
		code = 'if(true)if(x<2)2+2;'
		result = IfStmt(BoolLit('true'), IfStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), BinopAexp( \
			IntNum(2), '+', IntNum(2)), None), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_if_stmt_with_while_loop(self):
		code = 'if(true)while(true)1;'
		result = IfStmt(BoolLit('true'), WhileStmt(BoolLit('true'), IntNum(1)), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)



	#TEST IF ELSE STATEMENT
	def test_single_line_if_else_stmt(self):
		code = 'if(x<5)1+1;else 2;'
		result = IfStmt(RelopBexp(Identifier('x'), '<', IntNum(5)), BinopAexp(IntNum(1), '+', IntNum(1)), \
			IntNum(2))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_if_else_stmt_boolean_paranthesis(self):
		code = 'if(((x<5)&&(x!=2)))1+1;else 2;'
		result = IfStmt(AndBexp(RelopBexp(Identifier('x'), '<', IntNum(5)), RelopBexp(Identifier('x'), '!=', \
			IntNum(2))), BinopAexp(IntNum(1), '+', IntNum(1)), IntNum(2))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_if_else_stmt(self):
		code = 'if(x<2){int k=2;2+2;true&&false;}else{int k=2;2+2;true&&false;}'
		result = IfStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), CompoundStmt([Decl(Param(TypeSpec('int'), \
		 	Identifier('k')), IntNum(2)), BinopAexp(IntNum(2), '+', IntNum(2)), AndBexp(BoolLit('true'), \
			BoolLit('false'))]), CompoundStmt([Decl(Param(TypeSpec('int'), Identifier('k')), IntNum(2)), \
			BinopAexp(IntNum(2), '+', IntNum(2)), AndBexp(BoolLit('true'), BoolLit('false'))]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_nested_if_else_stmt(self):
		code = 'if(true)if(x<2)2+2;else 2;else false;'
		result = IfStmt(BoolLit('true'), IfStmt(RelopBexp(Identifier('x'), '<', IntNum(2)), BinopAexp( \
			IntNum(2), '+', IntNum(2)), IntNum(2)), BoolLit('false'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_if_else_stmt_with_while_loop(self):
		code = 'if(true)while(true)1;else while(false)2;'
		result = IfStmt(BoolLit('true'), WhileStmt(BoolLit('true'), IntNum(1)), WhileStmt(BoolLit('false'),\
		 IntNum(2)))


		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)


if __name__ == '__main__':
	unittest.main()