if __name__ == '__main__':
    from my_ast import *
elif __package__:
    from .my_ast import *
else:
	from my_ast import *

from enum import Enum, auto

class NotDeclaredError(Exception):
	pass

class AlreadyDeclaredError(Exception):
	pass


class EntityType(Enum):
	Fun = auto()
	Var = auto()
	Class = auto()


class Entity:
	def __init__(self, type_, struct):
		self.type_ = type_
		self.struct = struct

	def __repr__(self):
		return '%s, [%s]' % (self.type_.name, self.struct)

class VariableStruct:
	def __init__(self, type_, class_):
		self.type_ = type_
		self.class_ = class_

	def __repr__(self):	
		return '%s, %s' % (self.type_, self.class_) if self.class_ \
			else '%s' % self.type_

class FunctionStruct:
	def __init__(self, type_, class_, env):
		self.type_ = type_
		self.class_ = class_
		self.env = env #USED TO CHECK ARGS

	def __repr__(self):
		return '%s, %s, %s' % (self.type_, self.class_, self.env) if self.class_ \
			else '%s, %s' % (self.type_, self.env)

class ClassStruct:
	def __init__(self, env):
		self.env = env

	def __repr__(self):
		return ''

class Env:
	def __init__(self, parent=None, name=None,):
		self.name = name
		self.parent = parent
		self.dict = {}
		self.childs = list()

	def find_local(self, name):
		if name in self.dict.keys():
			return self.dict[name]

	def find(self, name):
		var = self.find_local(name)
		if var:
			return var
		if self.parent:
			return self.parent.find(name)

	def __repr__(self):
		return 'env %s: %s' % (self.name, self.dict) if self.name else \
			'env: %s' % self.dict

    
type_specifiers = ['bool', 'char', 'int', 'long', 'float', 'double', 'void']

class Syntax:
	def __init__(self, check=False):
		self.check_syntax = check
		self.global_env = Env(None, '-global-')
		self.current_env = self.global_env

	def set_new_env(self):
		env = Env(self.current_env)
		self.current_env.childs.append(env)
		self.current_env = env

	def previous_env(self):
		self.current_env = self.current_env.parent

	def check_if_declared_variable(self, identifier):
		return self.current_env.find(identifier.name)

	def check_if_part_of_class(self, var, class_name):
		class_ = self.global_env.find_local(class_name)
		class_env = class_.struct.env
		if class_env:
			return class_env.find_local(var)

	#c.b.a
	def check_id(self, id_):
		if not self.check_syntax:
			return
		#GOT ID
		if isinstance(id_, Id):
			parent, child = id_.parent, id_.child
			#CHECK IF OBJECT VISIBLE
			var = self.check_if_declared_variable(parent)
			while isinstance(id_, Id):
				to_check = id_ = id_.child
				#STILL NESTED ID
				if isinstance(id_, Id):
					to_check = id_.parent
				to_check = to_check.name
				var_class = var.struct.type_.name
				#CHECK IF MEMBER
				var = self.check_if_part_of_class(to_check, var_class)
				if not var:
					raise Exception
			return var
		#GOT IDENTIFIER
		else:
			var = self.check_if_declared_variable(id_)
			if not var:
				raise NotDeclaredError
			return var

	def check_funcall(self, funcall):
		if not self.check_syntax:
			return
		id_, args = funcall.name, funcall.args
		fun_def = self.check_id(id_)
		if fun_def.type_ != EntityType.Fun:
			raise Exception('Not callable')
		params = fun_def.struct.env.dict
		if len(params) != len(args):
			raise Exception('Wrong number of args')
		for arg, param in zip(args, params.values()):
			#BOTH IDENTIFIERS
			if isinstance(arg, Identifier) or isinstance(arg, Id):
				arg_decl = self.check_id(arg)
				#CHECK IF NOT FUN OR CLASS
				if arg_decl.type_ != EntityType.Var:
					raise Exception('Non-variable argument')
				arg_type = arg_decl.struct.type_
				param_type = param.struct.type_
				if not isinstance(param_type, Identifier) \
				  or (isinstance(arg_type, Identifier) and arg_type != param_type):
					raise Exception('Invalid argument')
			#ARG IS LITERAL
			else:
				if isinstance(param.struct.type_, Identifier):
					raise Exception('Invalid argument')	

	def check_if_simple_type(self, var):
		if not self.check_syntax:
			return
		if var.type_ != EntityType.Var:
			raise Exception('Variable required')
		#CHECK IF VAR NOT FUN OR CLASS TODOOO
		type_ = var.struct.type_
		if isinstance(type_, Identifier):
			raise Exception('Incompatibile types in aexp')

	def check_assignment(self, assign):
		if not self.check_syntax:
			return
		id_, value = assign.name, assign.value
		var = self.check_id(id_)
		if var.type_ != EntityType.Var:
			raise Exception('L-value in assignment must be variable')
		l_type = var.struct.type_
		r_type = self.get_r_value_type(value)
		self.compare_types(l_type, r_type)

	def get_r_value_type(self, value):
		if isinstance(value, Aexp):
			return TypeSpec('aexp') #TODO
		if isinstance(value, Bexp):
			return TypeSpec('bool')
		if type(value) in [Id, Identifier]:
			var = self.check_id(value)
			if var.type_ != EntityType.Var:
				raise Exception('Not a variable')
			type_ = var.struct.type_
			return type_
		if isinstance(value, FunCall):
			name = value.name
			fun = self.check_id(name)
			if fun.type_ != EntityType.Fun:
				raise Exception('Not callable')
			type_ = fun.struct.type_
			print(fun, type_)
			return type_
		raise Exception('Unknown Type')

	def compare_types(self, l_val, r_val):
		if isinstance(l_val, TypeSpec):
			if l_val == TypeSpec('bool'):
				if not isinstance(r_val, TypeSpec) or r_val != TypeSpec('bool'):
					raise Exception('Assign type mismatch')
			if not isinstance(r_val, TypeSpec):
				raise Exception('Assign type mismatch')
		else:
			if not isinstance(r_val, Identifier) or l_val != r_val:
				raise Exception('Assign type mismatch')		


	#AFTER LEAVING
	#L_VAL = IDENTIFIER!
	def add_declaration(self, decl, member=False):
		if not self.check_syntax:
			return
		parameter, value = decl.parameter, decl.value
		type_spec, id_ = parameter.type, parameter.name
		name = id_.name
		#type_spec id_ = value

		#OBJECT
		if isinstance(type_spec, Identifier):
			#INIT PROHIBITED
			#check if class exist
			if not self.global_env.find_local(type_spec.name):
				raise Exception()

			if value:
				raise Exception('Initializing object')

		#SIMPLE TYPE
		else:
			#CHECK IF PROPER TYPE ASSIGNED
			if value:
				l_type = type_spec
				r_type = self.get_r_value_type(value)
				self.compare_types(l_type, r_type)

		class_ = None	

		if member:
			class_ = self.current_env.name
		var = VariableStruct(type_spec, class_)
		self.current_env.dict[name] = Entity(EntityType.Var, var)

	#after leaving fun_env
	def add_function_definition(self, fun_def):
		if not self.check_syntax:
			return
		type_, id_= fun_def.type, fun_def.name
		class_ = None
		fun_env = self.current_env.childs[-1]
		fun_env.name = id_.name
		if self.current_env.parent:
			class_ = self.current_env.name
		fun = FunctionStruct(type_, class_, fun_env)
		self.current_env.dict[id_.name] = Entity(EntityType.Fun, fun)

	#pre leaving class_env
	def add_class(self, class_):
		if not self.check_syntax:
			return
		id_ = class_.name
		cl = ClassStruct(self.current_env)
		self.global_env.dict[id_.name] = Entity(EntityType.Class, cl)

	def name_env(self, id_):
		if not self.check_syntax:
			return
		self.current_env.name = id_.name

	def check_identifier(self, id_):
		if not self.check_syntax:
			return
		if self.check_if_declared_variable(id_):
			raise AlreadyDeclaredError

	def check_parameter(self, param):
		if not self.check_syntax:
			return
		type_spec, name = param.type, param.name.name
		if self.current_env.find_local(name):
			raise AlreadyDeclaredError()
		var = VariableStruct(type_spec, None)
		self.current_env.dict[name] = Entity(EntityType.Var, var)


