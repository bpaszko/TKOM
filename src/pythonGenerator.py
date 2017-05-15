if __name__ == '__main__':
	from my_ast import *
	from my_env import *
elif __package__:
	from .my_ast import *
	from .my_env import *
else:
	from my_ast import *
	from my_env import *

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

	def create_class(self, id_, env = None):
		code = self.tabs * '\t' + 'class ' + id_.to_python(env) + ':\n'
		self.code += code
		self.tabs += 1

	def create_function(self, id_, params, env):
		code = self.tabs * '\t' + 'def ' + id_.to_python(None) + '('
		if env.parent.env_type == EnvType.Class:
			code += 'self'
			if params: 
				code += ', '

		for i, param in enumerate(params):
			code += param.to_python(None)
			if i < len(params) - 1:
				code += ', '
		code += '):\n'
		self.code += code
		self.tabs += 1 

	def create_while_loop(self, bexp, env):
		code = '\t' * self.tabs + 'while ' + bexp.to_python(env) + ':\n'
		self.code += code
		self.tabs += 1

	def create_for_loop(self, init, cond, increment, env):
		var = init.parameter.name.to_python(env)
		var_value = init.value.to_python(env)
		cond_var = cond.right.to_python(env)
		inc_var = increment.value.right.to_python(env)
		code = '\t' * self.tabs + 'for ' + var + ' in range(' + var_value + \
			 ',' + cond_var + ',' + inc_var + '):\n'
		self.code += code
		self.tabs += 1

	def create_if_stmt(self, bexp, env):
		code = '\t' * self.tabs + 'if ' + bexp.to_python(env) + ':\n'
		self.code += code
		self.tabs += 1

	def create_else_stmt(self):
		code = '\t' * self.tabs + 'else:\n'
		self.code += code
		self.tabs += 1

	def create_jump_stmt(self, jump_stmt, env):
		code = '\t' * self.tabs + jump_stmt.to_python(env) + '\n'
		self.code += code

	def create_pass(self):
		self.code += '\t' * self.tabs + 'pass' + '\n'

	"""
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
	"""
	
	def create_id(self, id_, env = None):
		code = '\t' * self.tabs + id_.to_python(env) + '\n'
		self.code += code

	def create_literal(self, literal, env = None):
		code = '\t' * self.tabs + literal.to_python(env) + '\n'
		self.code += code

	def create_funcall(self, funcall, env):
		code = '\t' * self.tabs + funcall.to_python(env) + '\n'
		self.code += code

	def create_aexp(self, aexp, env):
		code = '\t' * self.tabs + aexp.to_python(env) + '\n'
		self.code += code

	def create_bexp(self, bexp, env):
		code = '\t' * self.tabs + bexp.to_python(env) + '\n'
		self.code += code

	def create_declaration(self, decl, env):
		code = '\t' * self.tabs + decl.to_python(env) + '\n'
		self.code += code

	def create_assignment(self, assignment, env):
		code = '\t' * self.tabs + assignment.to_python(env) + '\n'
		self.code += code

	def create_main_call(self):
		self.code += 'print(main())'