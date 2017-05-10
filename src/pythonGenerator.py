if __name__ == '__main__':
    from my_ast import *
elif __package__:
    from .my_ast import *


class PythonGenerator:
	def __init__(self, path='pycode.py'):
		self.tabs = 0
		self.code = ''
		self.file_path = path

	def get_code(self):
		return self.code

	def dump(self):
		with open(self.file_path, 'w') as f:
			f.write(self.code)

	def decrease(self):
		self.tabs -= 1

	def create_class(self, id_):
		code = self.tabs * '\t' + 'class ' + id_.to_python() + ':\n'
		self.code += code
		self.tabs += 1

	def create_function(self, id_, params):
		code = self.tabs * '\t' + 'def ' + id_.to_python() + '('
		for i, param in enumerate(params):
			code += param.to_python()
			if i < len(params) - 1:
				code += ', '
		code += '):\n'
		self.code += code
		self.tabs += 1 

	def create_while_loop(self, bexp):
		code = '\t' * self.tabs + 'while ' + bexp.to_python() + ':\n'
		self.code += code
		self.tabs += 1

	def create_for_loop(self, init, cond, increment):
		var = init.parameter.name.to_python()
		var_value = init.value.to_python()
		cond_var = cond.right.to_python()
		inc_var = increment.value.right.to_python()
		code = '\t' * self.tabs + 'for ' + var + ' in range(' + var_value + \
			 ',' + cond_var + ',' + inc_var + '):\n'
		self.code += code
		self.tabs += 1

	def create_if_stmt(self, bexp):
		code = '\t' * self.tabs + 'if ' + bexp.to_python() + ':\n'
		self.code += code
		self.tabs += 1

	def create_else_stmt(self):
		code = '\t' * self.tabs + 'else:\n'
		self.code += code
		self.tabs += 1

	def create_jump_stmt(self, jump_stmt):
		code = '\t' * self.tabs + jump_stmt.to_python() + '\n'
		self.code += code

	@staticmethod
	def get_type(value):
		if isinstance(value, Id) or isinstance(value, Idenifier):
			return 'Id'
		if isinstance(value, Literal):
			return 'Literal'
		if isinstance(value, Aexp):
			return 'Aexp'
		if isinstance(value, Bexp):
			return 'Bexp'
		if isinstance(value, FunCall):
			return 'Funcall'

	def create_id(self, id_):
		code = '\t' * self.tabs + id_.to_python() + '\n'
		self.code += code

	def create_literal(self, literal):
		code = '\t' * self.tabs + literal.to_python() + '\n'
		self.code += code

	def create_funcall(self, funcall):
		code = '\t' * self.tabs + funcall.to_python() + '\n'
		self.code += code

	def create_aexp(self, aexp):
		code = '\t' * self.tabs + aexp.to_python() + '\n'
		self.code += code

	def create_bexp(self, bexp):
		code = '\t' * self.tabs + bexp.to_python() + '\n'
		self.code += code

	def create_declaration(self, decl):
		code = '\t' * self.tabs + decl.to_python() + '\n'
		self.code += code

	def create_assignment(self, assignment):
		code = '\t' * self.tabs + assignment.to_python() + '\n'
		self.code += code