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
	def test_float_literal(self):
		code = '12.44'
		result = FloatNum(12.44)

		parser = createParser(code)
		ast = parser.parseLiteral()

		self.assertEqual(ast, result)

	def test_int_literal(self):
		code = '10'
		result = IntNum(10)

		parser = createParser(code)
		ast = parser.parseLiteral()

		self.assertEqual(ast, result)

	def test_char_literal(self):
		code = "'a'"
		result = Character("'a'")

		parser = createParser(code)
		ast = parser.parseLiteral()

		self.assertEqual(ast, result)

	def test_simple_id(self):
		code = 'var'
		result = Identifier('var')

		parser = createParser(code)
		ast = parser.parseId()

		self.assertEqual(ast, result)

	def test_nested_ids(self):
		code = 'var.nest1.nest2'
		result = Id(Identifier('var'), Id(Identifier('nest1'), Identifier('nest2')))

		parser = createParser(code)
		ast = parser.parseId()

		self.assertEqual(ast, result)



	#test arithmetic expressions
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
		code = 'x = 5;'
		result = AssignExp(Identifier('x'), IntNum(5))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_identifier(self):
		code = 'x = y;'
		result = AssignExp(Identifier('x'), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_aexp(self):
		code = 'x = 2 + 4;'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_aexp_paranthesis(self):
		code = 'x = (2 + 4);'
		result = AssignExp(Identifier('x'), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_bexp(self):
		code = 'x = false || true;'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_bexp_paranthesis(self):
		code = 'x = (false && true);'
		result = AssignExp(Identifier('x'), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_funcall_without_args(self):
		code = 'x = fun();'
		result = AssignExp(Identifier('x'), FunCall(Identifier('fun'), []))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_id_funcall_without_args(self):
		code = 'x = var.fun();'
		result = AssignExp(Identifier('x'), FunCall(Id(Identifier('var'), Identifier('fun')), []))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_funcall_with_args(self):
		code = 'x = fun(a);'
		result = AssignExp(Identifier('x'), FunCall(Identifier('fun'), [Identifier('a')]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_assign_id_funcall_with_args(self):
		code = 'x = var.fun(2, 1);'
		result = AssignExp(Identifier('x'), FunCall(Id(Identifier('var'), Identifier('fun')), \
			[IntNum(2), IntNum(1)]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)



	#TEST FUNCTION CALL
	def test_function_call_without_params_from_identifier(self):
		code = 'fun();'
		result = FunCall(Identifier('fun'), [])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_function_call_without_params_from_id(self):
		code = 'var.var2.fun();'
		result = FunCall(Id(Identifier('var'), Id(Identifier('var2'), Identifier('fun'))), [])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_function_call_with_params_from_identifier(self):
		code = 'fun(k, 2);'
		result = FunCall(Identifier('fun'), [Identifier('k'), IntNum(2)])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_function_call_with_params_from_id(self):
		code = 'var.var2.fun(k, 2);'
		result = FunCall(Id(Identifier('var'), Id(Identifier('var2'), Identifier('fun'))), \
			[Identifier('k'), IntNum(2)])

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)



	#TESTING DECLARATIONS
	def test_declare_without_assignment(self):
		code = 'int x;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), None)

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)


	def test_declare_with_literal(self):
		code = 'int x = 5;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(5))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_identifier(self):
		code = 'int x = y;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), Identifier('y'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_aexp(self):
		code = 'int x = 2 + 4;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_aexp_paranthesis(self):
		code = 'int x = (2 + 4);'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), BinopAexp(IntNum(2), '+', IntNum(4)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_bexp(self):
		code = 'int x = false || true;'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_bexp_paranthesis(self):
		code = 'int x = (false && true);'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), OrBexp(BoolLit('false'), BoolLit('true')))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_with_funcall_without_args(self):
		code = 'int x = fun();'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), FunCall(Identifier('fun'), []))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)


	def test_declare_with_id_funcall_with_args(self):
		code = 'int x = var.fun(2, 1);'
		result = Decl(Param(TypeSpec('int'), Identifier('x')), FunCall(Id(Identifier('var'), \
			Identifier('fun')), [IntNum(2), IntNum(1)]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_declare_object(self):
		code = 'MyClass x;'
		result = Decl(Param(Identifier('MyClass'), Identifier('x')), None)

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
		code = 'while(true)continue;'
		result = WhileStmt(BoolLit('true'), JumpStmt('continue'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_while_loop_with_break(self):
		code = 'while(true)break;'
		result = WhileStmt(BoolLit('true'), JumpStmt('break'))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)



	#TEST FOR LOOP
	def test_single_line_for_loop(self):
		code = 'for(int x=0;x<5;x=x+2)1+1;'
		result = ForStmt(Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(0)), RelopBexp(Identifier('x'), \
			'<', IntNum(5)), AssignExp(Identifier('x'), BinopAexp(Identifier('x'), '+', IntNum(2))), \
			BinopAexp(IntNum(1), '+', IntNum(1)))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_compound_for_loop(self):
		code = 'for(int x=0;x<z;x=x+2){int k=2;2+2;true&&false;}'
		result = ForStmt(Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(0)), RelopBexp(Identifier('x'), \
			'<', Identifier('z')), AssignExp(Identifier('x'), BinopAexp(Identifier('x'), '+', IntNum(2))), \
			CompoundStmt([Decl(Param(TypeSpec('int'), Identifier('k')), IntNum(2)), BinopAexp(IntNum(2), '+', \
			IntNum(2)), AndBexp(BoolLit('true'), BoolLit('false'))]))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)

	def test_nested_for_loop(self):
		code = 'for(int x=0;x<5;x=x+2)for(int y=0;y<4;y=y+2)2+2;'
		result = ForStmt(Decl(Param(TypeSpec('int'), Identifier('x')), IntNum(0)), RelopBexp(\
			Identifier('x'), '<', IntNum(5)), AssignExp(Identifier('x'), BinopAexp(Identifier('x'), '+', \
			IntNum(2))), ForStmt(Decl(Param(TypeSpec('int'), Identifier('y')), IntNum(0)), \
			RelopBexp(Identifier('y'), '<',IntNum(4)), AssignExp(Identifier('y'), BinopAexp( \
			Identifier('y'), '+', IntNum(2))), BinopAexp(IntNum(2), '+', IntNum(2))))

		parser = createParser(code)
		ast = parser.parseStmt()

		self.assertEqual(ast, result)


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



	#FUNCTION DEFINITIONS TESTS
	def test_function_def_without_params_and_body(self):
		code = 'int fun(){}'
		result = FunDef(TypeSpec('int'), Identifier('fun'), [], CompoundStmt([]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	def test_function_def_without_params_with_body(self):
		code = 'int fun(){int a = 5;}'
		result = FunDef(TypeSpec('int'), Identifier('fun'), [], CompoundStmt([Decl(Param(TypeSpec('int'), \
			Identifier('a')), IntNum(5))]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	def test_function_def_with_params_without_body(self):
		code = 'char fun(int a, char b){}'
		result = FunDef(TypeSpec('char'), Identifier('fun'), [Param(TypeSpec('int'), Identifier('a')), \
			Param(TypeSpec('char'), Identifier('b'))], CompoundStmt([]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	def test_function_def_with_params_and_body(self):
		code = 'char fun(int a, char b, int k){ a = k + b; }'
		result = FunDef(TypeSpec('char'), Identifier('fun'), [Param(TypeSpec('int'), Identifier('a')), \
			Param(TypeSpec('char'), Identifier('b')), Param(TypeSpec('int'), Identifier('k'))], \
			CompoundStmt([AssignExp(Identifier('a'), BinopAexp(Identifier('k'), '+', Identifier('b')))]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	def test_function_def_with_void_return(self):
		code = 'void fun(){return;}'
		result = FunDef(TypeSpec('void'), Identifier('fun'), [], CompoundStmt([JumpStmt('return', None)]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	def test_function_def_with_return(self):
		code = 'int fun(int a){return a;}'
		result = FunDef(TypeSpec('int'), Identifier('fun'), [Param(TypeSpec('int'), Identifier('a'))], \
			CompoundStmt([JumpStmt('return', Identifier('a'))]))

		parser = createParser(code)
		ast = parser.parseFunctionDefinition()

		self.assertEqual(ast, result)

	#CLASS TESTS
	def test_empty_class(self):
		code = 'class X{};'
		result = Class(Identifier('X'), [])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_with_empty_access_specs(self):
		code = 'class X{public:private:protected:public:};'
		result = Class(Identifier('X'), [AccessMembers('public', []), AccessMembers('private', []), \
			AccessMembers('protected', []), AccessMembers('public', [])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_same_spec_member_declarations_decl(self):
		code = 'class X{public:int x = 5; int k;};'
		result = Class(Identifier('X'), [AccessMembers('public', [Decl(Param(TypeSpec('int'), \
			Identifier('x')), IntNum(5)), Decl(Param(TypeSpec('int'), Identifier('k')), None)])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_same_spec_member_declarations_fun(self):
		code = 'class X{public:int fun1(){} int fun2(int a){}};'
		result = Class(Identifier('X'), [AccessMembers('public', [FunDef(TypeSpec('int'), \
			Identifier('fun1'), [], CompoundStmt([])), FunDef(TypeSpec('int'), Identifier('fun2'), \
			[Param(TypeSpec('int'), Identifier('a'))], CompoundStmt([]))])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_same_spec_member_declarations_both(self):
		code = 'class X{public:int x = 2; int fun2(int a){}};'
		result = Class(Identifier('X'), [AccessMembers('public', [Decl(Param(TypeSpec('int'), \
			Identifier('x')), IntNum(2)), FunDef(TypeSpec('int'), Identifier('fun2'), [Param(TypeSpec('int'), \
			Identifier('a'))], CompoundStmt([]))])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_different_spec_member_declarations(self):
		code = 'class X{private:int k; public:int fun2(int a){}};'
		result = Class(Identifier('X'), [AccessMembers('private', [Decl(Param(TypeSpec('int'), \
			Identifier('k')), None)]), AccessMembers('public', [FunDef(TypeSpec('int'), \
			Identifier('fun2'), [Param(TypeSpec('int'), Identifier('a'))], CompoundStmt([]))])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)

	def test_class_members_without_access_spec(self):
		code = 'class X{int k;};'
		result = Class(Identifier('X'), [AccessMembers('private', [Decl(Param(TypeSpec('int'), \
			Identifier('k')), None)])])

		parser = createParser(code)
		ast = parser.parseClassSpecifier()

		self.assertEqual(ast, result)



	#TESTING WHOLE PROGRAMS 
	def test_whole_program(self):
		code = ' \
			class X { \
				public: \
					long x = 15;  \
					int f(int arg) { \
						f2(); \
						int y = x + arg; \
						return y; \
					} \
				private: \
					void f2() { \
						x = x + 5; \
					} \
				}; \
 					\
				int main() { \
					X obj; \
					int y = 0; \
					for(int i = 0; i < 5; i = i + 1) { \
						if (y < 10) { \
							y = obj.f(i); \
							continue; \
						} \
						else \
							break; \
					} \
					return y; \
				} '

		result = \
			Program( \
				[Class(Identifier('X'),  \
					[AccessMembers('public', [ \
						Decl(Param(TypeSpec('long'), Identifier('x')), IntNum(15)),  \
						FunDef(TypeSpec('int'), Identifier('f'), [Param(TypeSpec('int'), Identifier('arg'))],  \
							CompoundStmt([ \
								FunCall(Identifier('f2'), []),  \
								Decl(Param(TypeSpec('int'), Identifier('y')), BinopAexp(Identifier('x'), '+', Identifier('arg'))),  \
								JumpStmt('return', Identifier('y'))]))]),  \
					AccessMembers('private', [ \
						FunDef(TypeSpec('void'), Identifier('f2'), [],  \
							CompoundStmt([ \
								AssignExp(Identifier('x'), BinopAexp(Identifier('x'), '+', IntNum(5)))]))])]),  \
				 \
				FunDef(TypeSpec('int'), Identifier('main'), [],  \
					CompoundStmt([ \
						Decl(Param(Identifier('X'), Identifier('obj')), None),  \
						Decl(Param(TypeSpec('int'), Identifier('y')), IntNum(0)),  \
						ForStmt(Decl(Param(TypeSpec('int'), Identifier('i')), IntNum(0)), RelopBexp(Identifier('i'), '<', IntNum(5)), AssignExp(Identifier('i'), BinopAexp(Identifier('i'), '+', IntNum(1))),  \
							CompoundStmt([ \
								IfStmt(RelopBexp(Identifier('y'), '<', IntNum(10)),  \
									CompoundStmt([ \
										AssignExp(Identifier('y'), FunCall(Id(Identifier('obj'), Identifier('f')), [Identifier('i')])),  \
										JumpStmt('continue', None)]),  \
									JumpStmt('break', None))])),  \
						JumpStmt('return', Identifier('y'))]))]) 

		parser = createParser(code)
		ast = parser.parseProgram()

		self.assertEqual(ast, result)

if __name__ == '__main__':
	unittest.main()