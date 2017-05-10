import unittest

if __name__ == '__main__':
    import sys
    import io
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from src.pythonGenerator import *
    from src.my_ast import *

class PythonGeneratorTest(unittest.TestCase):
	def setUp(self):
		self.pygen = PythonGenerator()

	def test_class_header(self):
		self.pygen.create_class(Identifier('MyClass'))
		result = self.pygen.get_code()
		expected = 'class MyClass:'
		self.assertEqual(result, expected)

	def test_no_arg_function_header(self):
		self.pygen.create_function(Identifier('my_fun'), list())
		result = self.pygen.get_code()
		expected = 'def my_fun():'
		self.assertEqual(result, expected)

	def test_function_header_with_args(self):
		param1 = Param(TypeSpec('int'), Identifier('p1')) 
		param2 = Param(Identifier('X'), Identifier('p2')) 
		param3 = Param(TypeSpec('char'), Identifier('p3')) 
		param4 = Param(TypeSpec('double'), Identifier('p4')) 
		param5 = Param(TypeSpec('float'), Identifier('p5'))
		params = [param1, param2, param3, param4, param5] 
		self.pygen.create_function(Identifier('my_fun'), params)
		result = self.pygen.get_code()
		expected = 'def my_fun(p1, p2, p3, p4, p5):'
		self.assertEqual(result, expected)

if __name__ == '__main__':
	unittest.main()