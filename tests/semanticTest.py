import unittest

if __name__ == '__main__':
    import sys
    import io
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from src.parser import *
    from src.lexer import *
    from src.my_ast import *

def parseCode(code):
	stream = io.StringIO(code)
	lexer = Lexer(stream)
	parser = Parser(lexer, Semantic(True))
	return parser.parseProgram()

class TestSemantic(unittest.TestCase):
	#TEST DECLARATIONS
	def test_simple_declare(self):
		code = 'int x;'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_simple_declare_with_assignment(self):
		code = 'int x = 2;'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_many_declares(self):
		code = 'int x;char y = \'a\'; double k;'
		result =  parseCode(code)
		self.assertTrue(result)


	def test_declare_class(self):
		code = 'class X{};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_object_without_class(self):
		code = 'X x;'
		with self.assertRaises(NotDeclaredTypeError):
			parseCode(code)

	def test_declare_object(self):
		code = 'class X{}; X x;'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_function(self):
		code = 'int main(){}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_coliding_declares(self):
		code = 'int x; char x;'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_coliding_classes(self):
		code = 'class X{}; class X{};'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_coliding_functions(self):
		code = 'int fun(){} char fun(){}'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_coliding_fun_var(self):
		code = 'int fun(){} int fun;'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_coliding_fun_class(self):
		code = 'class X{}; fun X(){}'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_coliding_class_var(self):
		code = 'int X; class X{};'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_colliding_var_in_different_scope(self):
		code = 'int x; int main(){int x;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_var_fun_in_different_scopes(self):
		code = 'int fun(){} int main(){int fun;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_objects_in_different_scopes(self):
		code = 'class X{}; X x; int fun(){X x;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_many_colliding_in_many_scopes(self):
		code = 'int x; int fun(){float x; if(true){char x;if(false){double x;}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_in_same_scope(self):
		code = 'int fun(){float x; int x;}'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_fun_with_params(self):
		code = 'int fun(int a, char b){}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_object_params(self):
		code = 'class X{}; class Y{}; int fun(Y a, X b){}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_colliding_param_var(self):
		code = 'int a; int fun(int a){}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_colliding_params(self):
		code = 'int fun(int a, char a){}'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	"""def test_declare_fun_with_colliding_arg_var_inside_scope(self):
					code = 'int fun(int a){char a;}'
					with self.assertRaises(AlreadyDeclaredError):
						parseCode(code)"""


	def test_declare_class_with_members(self):
		code = 'class X{int k; int fun(){}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_class_with_colliding_members(self):
		code = 'class X{int k; int k(){}};'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_class_with_other_object(self):
		code = 'class X{}; class Y{X x;};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_class_with_even_deeper_nested_objects(self):
		code = 'class X{}; class Y{X x;}; class Z{Y y;};'
		result =  parseCode(code)
		self.assertTrue(result)


	def test_declare_colliding_var_in_different_scope_in_class(self):
		code = 'class X{int x; int main(){int x;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_var_fun_in_different_scopes_in_class(self):
		code = 'class X{int fun(){} int main(){int fun;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_objects_in_different_scopes_in_class(self):
		code = 'class X{}; class Y{X x; int fun(){X x;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_many_colliding_in_many_scopes_in_class(self):
		code = 'class X{int x; int fun(){float x; if(true){char x;if(false){double x;}}}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_in_same_scope_in_class(self):
		code = 'class X{int fun(){float x; int x;}};'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_fun_with_params_in_class(self):
		code = 'class X{int fun(int a, char b){}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_object_params_in_class(self):
		code = 'class X{}; class Y{}; class Z{int fun(Y a, X b){}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_colliding_param_var_in_class(self):
		code = 'class X{int a; int fun(int a){}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_fun_with_colliding_params_in_class(self):
		code = 'class X{int fun(int a, char a){}};'
		with self.assertRaises(AlreadyDeclaredError):
			parseCode(code)

	def test_declare_colliding_funs_out_and_in_class(self):
		code = 'int fun(int a){} class X{int fun(int a){}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_declare_colliding_vars_out_and_in_class(self):
		code = 'int x; class X{int x;};'
		result =  parseCode(code)
		self.assertTrue(result)




	#FUNCALLS
	def test_simple_fun_call(self):
		code = 'int fun(){} int main(){fun();}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_args(self):
		code = 'class X{}; int fun(int a, X b){} int main(){int x; X y; fun(x, y);}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_literal_args(self):
		code = 'int fun(int a, char b){} int main(){fun(2, \'a\');}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_too_small_number_of_args(self):
		code = 'int fun(int a){} int main(){fun();}'
		with self.assertRaises(WrongNumberOfArgsError):
			parseCode(code)

	def test_fun_call_fun_with_too_large_number_of_args(self):
		code = 'int fun(int a){} int main(){int x; int y; fun(x, y);}'
		with self.assertRaises(WrongNumberOfArgsError):
			parseCode(code)

	def test_fun_call_fun_with_wrong_args_v1(self):
		code = 'class X{}; int fun(int a, X b){} int main(){X y; fun(2, 2);}'
		with self.assertRaises(InvalidArgError):
			parseCode(code)

	def test_fun_call_fun_with_wrong_args_v2(self):
		code = 'class X{}; int fun(int a, X b){} int main(){X y; fun(y, y);}'
		with self.assertRaises(InvalidArgError):
			parseCode(code)

	def test_call_variable(self):
		code = 'int main(){int x; x();}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_variable_with_args(self):
		code = 'int main(){int x; x(2);}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_class(self):
		code = 'class X{}; int main(){X();}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_class_with_args(self):
		code = 'class X{}; int main(){X(a);}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_from_deeper_nested_level(self):
		code = 'int fun(){} int main(){if(true){if(false){fun();}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_call_with_override_function(self):
		code = 'int fun(){} int main(){int fun; fun();}'
		with self.assertRaises(NotCallableError):
			parseCode(code)


	def test_simple_fun_call_in_nested_objects(self):
		code = 'class A{int fun(){}}; class B{A a;}; class C{B b;}; \
			int main(){C c; c.b.a.fun();}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_args_in_nested_objects(self):
		code = 'class X{}; class A{int fun(int a, X b){}}; class B{A a;}; class C{B b;}; \
			int main(){int x; X y; C c; c.b.a.fun(x, y);}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_literal_args_in_nested_objects(self):
		code = 'class A{int fun(int a, char b){}}; class B{A a;}; class C{B b;}; \
			int main(){C c; c.b.a.fun(2, \'a\');}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_fun_call_with_too_small_number_of_args_in_nested_objects(self):
		code = 'class A{int fun(int a){}}; class B{A a;}; class C{B b;}; \
			int main(){C c; c.b.a.fun();}'
		with self.assertRaises(WrongNumberOfArgsError):
			parseCode(code)

	def test_fun_call_fun_with_too_large_number_of_args_in_nested_objects(self):
		code = 'class A{int fun(int a){}}; class B{A a;}; class C{B b;}; \
			int main(){int x; int y; C c; c.b.a.fun(x, y);}'
		with self.assertRaises(WrongNumberOfArgsError):
			parseCode(code)

	def test_fun_call_fun_with_wrong_args_v1_in_nested_objects(self):
		code = 'class X{}; class A{int fun(int a, X b){}}; class B{A a;}; class C{B b;}; \
			int main(){X y; C c; c.b.a.fun(2, 2);}'
		with self.assertRaises(InvalidArgError):
			parseCode(code)

	def test_fun_call_fun_with_wrong_args_v2_in_nested_objects(self):
		code = 'class X{}; class A{int fun(int a, X b){}}; class B{A a;}; class C{B b;}; \
			int main(){X y; C c; c.b.a.fun(y, y);}'
		with self.assertRaises(InvalidArgError):
			parseCode(code)

	def test_call_variable_in_nested_objects(self):
		code = 'int main(){int x; x();}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_variable_with_args_in_nested_objects(self):
		code = 'class A{int x;}; class B{A a;}; class C{B b;}; \
			int main(){int x; x(2);}'
		with self.assertRaises(NotCallableError):
			parseCode(code)

	def test_call_from_deeper_nested_level_in_nested_objects(self):
		code = 'class A{int fun(){}}; class B{A a;}; class C{B b;}; C c;\
			int main(){if(true){if(false){c.b.a.fun();}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_call_with_override_function_in_nested_objects(self):
		code = 'class A{int fun(){}}; class B{A a;}; class C{B b;}; C c;\
			int main(){int fun; if(false){if(true){c.b.a.fun();}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_call_not_class_member(self):
		code = 'class A{}; int main(){A a; a.fun();}'
		with self.assertRaises(NotAClassMemberError):
			parseCode(code)

	def test_call_not_class_member_in_nested_objects(self):
		code = 'class A{}; class B{A a;}; class C{B b;}; C c;\
			int main(){C c; c.b.a.fun();}'
		with self.assertRaises(NotAClassMemberError):
			parseCode(code)


	#TEST AEXP
	def test_simple_aexp(self):
		code = 'int main(){2+3;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_aexp_with_variable(self):
		code = 'int main(){int a; 2+a;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_aexp_with_nested_variable(self):
		code = 'class A{int var;}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2+c.b.a.var;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_aexp_with_fun(self):
		code = 'int fun(){} int main(){2+fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_aexp_with_class(self):
		code = 'class X{}; int main(){2+X;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_aexp_with_member_fun(self):
		code = 'class A{int fun(){}}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2+c.b.a.fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_aexp_with_object(self):
		code = 'class C{}; int main(){C c; 2+c;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_aexp_with_nested_object(self):
		code = 'class A{}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2+c.b.a;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_aexp_with_not_declared_var(self):
		code = 'int main(){2+var;}'
		with self.assertRaises(NotDeclaredVariableError):
			parseCode(code)

	def test_aexp_with_not_a_member(self):
		code = 'class A{}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2+c.b.a.var;}'
		with self.assertRaises(NotAClassMemberError):
			parseCode(code)


	#TEST BEXP
	def test_simple_bexp(self):
		code = 'int main(){true || false;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_bexp_with_variable(self):
		code = 'int main(){int a; a < 2;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_bexp_with_nested_variable(self):
		code = 'class A{int var;}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2 < c.b.a.var;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_bexp_with_fun(self):
		code = 'int fun(){} int main(){2 < fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_bexp_with_class(self):
		code = 'class X{}; int main(){2 < X;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_bexp_with_member_fun(self):
		code = 'class A{int fun(){}}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2 < c.b.a.fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_bexp_with_object(self):
		code = 'class C{}; int main(){C c; 2 < c;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_bexp_with_nested_object(self):
		code = 'class A{}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2 < c.b.a;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_bexp_with_not_declared_var(self):
		code = 'int main(){2 < var;}'
		with self.assertRaises(NotDeclaredVariableError):
			parseCode(code)

	def test_bexp_with_not_a_member(self):
		code = 'class A{}; class B{A a;}; class C{B b;}; \
			int main(){C c; 2 < c.b.a.var;}'
		with self.assertRaises(NotAClassMemberError):
			parseCode(code)



	#ASSIGNMENT TESTS
	def test_simple_assign(self):
		code = 'int main(){int x; x = 2;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_variable(self):
		code = 'int main(){int x; int y; x = y;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_object(self):
		code = 'class X{}; int main(){X x; X y; x = y;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_to_nested_object(self):
		code = 'class X{}; class Y{X x;}; int main(){Y y; X x; y.x = x;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_nested_object(self):
		code = 'class Z{}; class Y{Z z;}; class X{Y y;}; \
			int main(){X x; Z z; z = x.y.z;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_nested_var(self):
		code = 'class Y{int var;}; class X{Y y;}; int main(){X x; int var; var = x.y.var;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_to_nested_var(self):
		code = 'class Y{int var;}; class X{Y y;}; int main(){X x; x.y.var = 2;}'
		result =  parseCode(code)
		self.assertTrue(result)	

	def test_assign_not_declared_var(self):
		code = 'int main(){int x; x = y;}'
		with self.assertRaises(NotDeclaredVariableError):
			parseCode(code)

	def test_assign_fun(self):
		code = 'int fun(){} int main(){int x; x = fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_assign_to_fun(self):
		code = 'int fun(){} int main(){int x; fun = x;}'
		with self.assertRaises(LValueNotAVariableError):
			parseCode(code)

	def test_assign_to_class(self):
		code = 'class X{}; int main(){X x; X = x;}'
		with self.assertRaises(LValueNotAVariableError):
			parseCode(code)

	def test_assign_to_object_invalid_type(self):
		code = 'class Y{}; int main(){Y y; y = 2;}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)

	def test_assign_to_nested_object_invalid_type(self):
		code = 'class X{}; class Y{X x;}; int main(){Y y; y.x = 2;}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)

	def test_assign_nested_fun(self):
		code = 'class X{int fun(){}}; int main(){X x; int y; y = x.fun;}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_assign_to_nested_fun(self):
		code = 'class X{int fun(){}}; int main(){X x; int y; x.fun = y;}'
		with self.assertRaises(LValueNotAVariableError):
			parseCode(code)





	def test_assign_funcall(self):
		code = 'int fun(){} int main(){int x; x = fun();}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_funcall_wih_args(self):
		code = 'int fun(int a){}  int main(){int x; x=fun(2);}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_nested_funcall(self):
		code = 'class X{int fun(){}}; class Y{X x;}; \
			int main(){Y y; int a; a =y.x.fun();}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_nested_funcall_with_args(self):
		code = 'class X{int fun(int a){}}; class Y{X x;}; \
			int main(){Y y; int a; a = y.x.fun(2);}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_to_nested_var_funcall(self):
		code = 'class X{int var;}; class Y{X x;}; int fun(){}\
			int main(){Y y; y.x.var = fun();}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_to_nested_var_funcall_wih_args(self):
		code = 'class X{int var;}; class Y{X x;}; int fun(int a){}\
			int main(){Y y; y.x.var = fun(2);}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_not_declared_fun_call(self):
		code = 'int main(){int x; x = fun();}'
		with self.assertRaises(NotDeclaredVariableError):
			parseCode(code)

	def test_assign_to_fun_fun_call(self):
		code = 'int fun(){} int main(){int x; fun = fun();}'
		with self.assertRaises(LValueNotAVariableError):
			parseCode(code)

	def test_assign_to_class_fun_call(self):
		code = 'class X{}; X fun(){} int main(){X x; X = fun();}'
		with self.assertRaises(LValueNotAVariableError):
			parseCode(code)

	def test_assign_to_object_invalid_type_fun_call(self):
		code = 'class Y{}; int fun(){} int main(){Y y; y = fun();}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)

	def test_assign_to_nested_object_invalid_type_fun_call(self):
		code = 'class X{}; class Y{X x;}; int fun(){} int main(){Y y; y.x = fun();}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)


	#TEST ASSIGN AEXP
	def test_assign_aexp(self):
		code = 'int main(){int x; x = 2 + 3;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_aexp_with_id(self):
		code = 'int main(){int x; char y; x = 2 + y;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_wrong_aexp(self):
		code = 'class Y{}; int main(){int x; Y y; x = 2 + y;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_assign_aexp_to_object(self):
		code = 'class X{}; int main(){X x; x = 2 + 3;}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)

	def test_assign_aexp_to_bool(self):
		code = 'class X{}; int main(){bool x; x = 2 + 3;}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)


	#TEST ASSIGN BEXP
	def test_assign_bexp(self):
		code = 'int main(){bool x; x = 2 > 3;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_bexp_with_id(self):
		code = 'int main(){bool x; char y; x = 2 > y;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_assign_wrong_bexp(self):
		code = 'class Y{}; int main(){bool x; Y y; x = 2 < y;}'
		with self.assertRaises(NotCompatibileTypeInExpressionError):
			parseCode(code)

	def test_assign_bexp_to_object(self):
		code = 'class X{}; int main(){X x; x = 2 + 3;}'
		with self.assertRaises(AssignMismatchTypeError):
			parseCode(code)



	#TEST FOR LOOPS
	def test_simple_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_for_loop_with_id_in_init(self):
		code = 'int main(){int k; for(int i=k; i<2; i=i+1){}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_for_loop_with_fun_in_init(self):
		code = 'int fun(){} int main(){for(int i=fun; i<2; i=i+1){}}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_for_loop_with_class_in_init(self):
		code = 'class X{}; int main(){for(int i=X; i<2; i=i+1){}}'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_for_loop_with_already_declared_var(self):
		code = 'int main(){int x; for(int x=0; x<2; x=x+1){}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_for_loop_with_other_var_in_cond(self):
		code = 'int main(){int x; for(int i=0; x<2; i=i+1){}}'
		with self.assertRaises(InvalidForConditionError):
			parseCode(code)

	def test_for_loop_with_other_var_in_increment(self):
		code = 'int main(){int x; for(int i=0; i<2; x=i+1){}}'
		with self.assertRaises(InvalidForIncrementError):
			parseCode(code)

	def test_for_loop_with_other_var_in_increment_v2(self):
		code = 'int main(){int x; for(int i=0; i<2; i=x+1){}}'
		with self.assertRaises(InvalidForIncrementError):
			parseCode(code)	


	#TEST BREAK, CONTINUE
	def test_continue_without_loop(self):
		code = ' int main(){continue;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_break_without_loop(self):
		code = ' int main(){break;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)


	def test_simple_break_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){break;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_break_nested_for_loops(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){for(int j=0; j<2; j=j+1){break;}break;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_multiple_breaks_in_one_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){if(2<1)break;else{break;}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_break_before_for_loop(self):
		code = 'int main(){break; for(int i=0; i<2; i=i+1){}}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_break_after_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){} break;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_simple_continue_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){continue;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_continue_nested_for_loops(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){for(int j=0; j<2; j=j+1){continue;}continue;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_multiple_continues_in_one_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){if(2<1)continue;else{continue;}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_continue_before_for_loop(self):
		code = 'int main(){continue; for(int i=0; i<2; i=i+1){}}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_continue_after_for_loop(self):
		code = 'int main(){for(int i=0; i<2; i=i+1){} continue;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)



	def test_simple_break_while_loop(self):
		code = 'int main(){while(1<2){break;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_break_nested_while_loops(self):
		code = 'int main(){while(1<2){while(1<2){break;}break;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_multiple_breaks_in_one_while_loop(self):
		code = 'int main(){while(1<2){if(2<1)break;else{break;}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_break_bewhilee_while_loop(self):
		code = 'int main(){break; while(1<2){}}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_break_after_while_loop(self):
		code = 'int main(){while(1<2){} break;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_simple_continue_while_loop(self):
		code = 'int main(){while(1<2){continue;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_continue_nested_while_loops(self):
		code = 'int main(){while(1<2){while(1<2){continue;}continue;}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_multiple_continues_in_one_while_loop(self):
		code = 'int main(){while(1<2){if(2<1)continue;else{continue;}}}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_continue_bewhilee_while_loop(self):
		code = 'int main(){continue; while(1<2){}}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)

	def test_continue_after_while_loop(self):
		code = 'int main(){while(1<2){} continue;}'
		with self.assertRaises(JumpStmtOutsideLoopError):
			parseCode(code)


	#TEST RETURN
	def test_simple_return(self):
		code = 'int main(){return 1;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_return_id(self):
		code = 'int main(){int x; return x;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_return_object(self):
		code = 'class X{}; X fun(){X x; return x;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_return_void(self):
		code = 'void fun(){return;}'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_simple_member_return(self):
		code = 'class X{int fun(){return 1;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_member_return_id(self):
		code = 'class Y{int main(){int x; return x;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_member_return_object(self):
		code = 'class X{}; class Y{X fun(){X x; return x;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_member_return_void(self):
		code = 'class Y{void fun(){return;}};'
		result =  parseCode(code)
		self.assertTrue(result)

	def test_return_class(self):
		code = 'class X{}; X fun(){return X;};'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_return_fun(self):
		code = 'int fun2(){} int fun(){return fun2;};'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_member_return_class(self):
		code = 'class X{}; class Y{X fun(){return X;}};'
		with self.assertRaises(NotAVariableError):
			parseCode(code)

	def test_member_return_fun(self):
		code = 'int fun2(){} class Y{int fun(){return fun2;}};'
		with self.assertRaises(NotAVariableError):
			parseCode(code)



if __name__ == '__main__':
	unittest.main()
	#code = 'int fun(int a, char b){} int main(){fun(2, \'a\');}'
	#result =  parseCode(code)