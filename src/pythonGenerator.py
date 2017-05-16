if __name__ == '__main__':
	from my_ast import *
	from my_env import *
elif __package__:
	from .my_ast import *
	from .my_env import *
else:
	from my_ast import *
	from my_env import *

pykeywords = ['and', 'del', 'from', 'not', 'as', 'elif', 'global', 'or', 'with',
	'assert', 'pass', 'yield', 'except', 'import', 'print', 'class',
	'exec', 'in', 'raise', 'finally', 'is', 'def', 'lambda', 'try']


class PythonGenerator:
	def __init__(self, path='pycode.py', check=True):
		self.tabs = 0
		self.code = ''
		self.file_path = path
		self.check = check

		self.py_vars = {i:i+'_' for i in pykeywords}

	def get_code(self):
		return self.code

	def dump(self):
		if not self.check:
			return
		with open(self.file_path, 'w') as f:
			f.write(self.code)

	def decrease(self):
		if not self.check:
			return
		self.tabs -= 1

	def create_class(self, id_, env = None):
		if not self.check:
			return
		code = self.tabs * '\t' + 'class ' + id_.to_python(env, self.py_vars) + ':\n'
		self.code += code
		self.tabs += 1

	def create_function(self, id_, params, env):
		if not self.check:
			return
		code = self.tabs * '\t' + 'def ' + id_.to_python(None, self.py_vars) + '('
		if env.parent.env_type == EnvType.Class:
			code += 'self'
			if params: 
				code += ', '

		for i, param in enumerate(params):
			code += param.to_python(None, self.py_vars)
			if i < len(params) - 1:
				code += ', '
		code += '):\n'
		self.code += code
		self.tabs += 1 

	def create_while_loop(self, bexp, env):
		if not self.check:
			return
		code = '\t' * self.tabs + 'while ' + bexp.to_python(env, self.py_vars) + ':\n'
		self.code += code
		self.tabs += 1

	def create_for_loop(self, init, cond, increment, env):
		if not self.check:
			return
		var = init.parameter.name.to_python(env, self.py_vars)
		var_value = init.value.to_python(env, self.py_vars)
		cond_var = cond.right.to_python(env, self.py_vars)
		inc_var = increment.value.right.to_python(env, self.py_vars)
		code = '\t' * self.tabs + 'for ' + var + ' in range(' + var_value + \
			 ',' + cond_var + ',' + inc_var + '):\n'
		self.code += code
		self.tabs += 1

	def create_if_stmt(self, bexp, env):
		if not self.check:
			return
		code = '\t' * self.tabs + 'if ' + bexp.to_python(env, self.py_vars) + ':\n'
		self.code += code
		self.tabs += 1

	def create_else_stmt(self):
		if not self.check:
			return
		code = '\t' * self.tabs + 'else:\n'
		self.code += code
		self.tabs += 1

	def create_jump_stmt(self, jump_stmt, env):
		if not self.check:
			return
		code = '\t' * self.tabs + jump_stmt.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_pass(self):
		if not self.check:
			return
		self.code += '\t' * self.tabs + 'pass' + '\n'

	
	def create_id(self, id_, env = None):
		if not self.check:
			return
		code = '\t' * self.tabs + id_.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_literal(self, literal, env = None):
		if not self.check:
			return
		code = '\t' * self.tabs + literal.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_funcall(self, funcall, env):
		if not self.check:
			return
		code = '\t' * self.tabs + funcall.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_aexp(self, aexp, env):
		if not self.check:
			return
		code = '\t' * self.tabs + aexp.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_bexp(self, bexp, env):
		if not self.check:
			return
		code = '\t' * self.tabs + bexp.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_declaration(self, decl, env):
		if not self.check:
			return
		code = '\t' * self.tabs + decl.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_assignment(self, assignment, env):
		if not self.check:
			return
		code = '\t' * self.tabs + assignment.to_python(env, self.py_vars) + '\n'
		self.code += code

	def create_main_call(self):
		if not self.check:
			return
		self.code += 'print(main())'

	def create_copy_import(self):
		if not self.check:
			return
		self.code += 'from copy import deepcopy\n\n'		