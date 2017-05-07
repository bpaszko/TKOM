if __name__ == '__main__':
    from my_ast import *
elif __package__:
    from .my_ast import *
    from .my_env import *
    from .semantic_errors import *
else:
	from my_ast import *
	from my_env import *
	from semantic_errors import *


type_specifiers = ['bool', 'char', 'int', 'long', 'float', 'double', 'void']


class Semantic:
	def __init__(self, check=False):
		self.check_syntax = check
		self.global_env = Env(None, '-global-')
		self.current_env = self.global_env

	def set_new_env(self, name=None, env_type=None):
		env = Env(self.current_env, name, env_type)
		self.current_env.childs.append(env)
		self.current_env = env

	def previous_env(self):
		self.current_env = self.current_env.parent

	def check_if_declared_variable(self, identifier):
		if not self.check_syntax:
			return
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
					raise NotAClassMemberError
			return var
		#GOT IDENTIFIER
		else:
			var = self.check_if_declared_variable(id_)
			if not var:
				raise NotDeclaredVariableError
			return var

	def check_funcall(self, funcall):
		if not self.check_syntax:
			return
		id_, args = funcall.name, funcall.args
		fun_def = self.check_id(id_)
		if fun_def.type_ != EntityType.Fun:
			raise NotCallableError
		params = fun_def.struct.env.dict
		if len(params) != len(args):
			raise WrongNumberOfArgsError
		for arg, param in zip(args, params.values()):
			#BOTH IDENTIFIERS
			if isinstance(arg, Identifier) or isinstance(arg, Id):
				arg_decl = self.check_id(arg)
				#CHECK IF NOT FUN OR CLASS
				if arg_decl.type_ != EntityType.Var:
					raise NotAVariableError
				arg_type = arg_decl.struct.type_
				param_type = param.struct.type_
				#BOTH OBJECTS 
				if isinstance(param_type, Identifier) \
				  and isinstance(arg_type, Identifier) and arg_type != param_type:
					raise InvalidArgError
				if type(param_type) != type(arg_type):
					raise InvalidArgError
			#ARG IS LITERAL
			else:
				if isinstance(param.struct.type_, Identifier):
					raise InvalidArgError

	def check_if_simple_type(self, var):
		if not self.check_syntax:
			return
		if var.type_ != EntityType.Var:
			raise NotAVariableError
		#CHECK IF VAR NOT FUN OR CLASS TODOOO
		type_ = var.struct.type_
		if isinstance(type_, Identifier):
			raise NotCompatibileTypeInExpressionError

	def check_assignment(self, assign):
		if not self.check_syntax:
			return
		id_, value = assign.name, assign.value
		var = self.check_id(id_)
		if var.type_ != EntityType.Var:
			raise LValueNotAVariableError('L-value in assignment must be variable')
		l_type = var.struct.type_
		r_type = self.get_r_value_type(value)
		self.compare_types(l_type, r_type)

	def check_for_condition(self, cond, decl):
		if not self.check_syntax:
			return
		id_ = cond.left
		id_2 = decl.parameter.name
		if id_ != id_2:
			raise InvalidForConditionError

	def check_for_increment(self, assign, decl):
		if not self.check_syntax:
			return
		id_1, binop = assign.name, assign.value
		id_2, literal = binop.left, binop.right
		id_3 = decl.parameter.name
		if id_1 != id_3 or id_2 != id_3 or not isinstance(literal, IntNum):
			raise InvalidForIncrementError

	def get_r_value_type(self, value):
		if isinstance(value, Aexp):
			return TypeSpec('aexp') #TODO
		if isinstance(value, Bexp):
			return TypeSpec('bool')
		if type(value) in [Id, Identifier]:
			var = self.check_id(value)
			if var.type_ != EntityType.Var:
				raise NotAVariableError
			type_ = var.struct.type_
			return type_
		if isinstance(value, FunCall):
			name = value.name
			fun = self.check_id(name)
			if fun.type_ != EntityType.Fun:
				raise NotCallableError
			type_ = fun.struct.type_
			return type_
		raise UnknownTypeError

	def compare_types(self, l_val, r_val):
		if isinstance(l_val, TypeSpec):
			if l_val == TypeSpec('bool'):
				if not isinstance(r_val, TypeSpec) or r_val != TypeSpec('bool'):
					raise AssignMismatchTypeError
			if not isinstance(r_val, TypeSpec) and not isinstance(r_val, Literal):
				raise AssignMismatchTypeError
		else:
			if not isinstance(r_val, Identifier) or l_val != r_val:
				raise AssignMismatchTypeError	


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
				raise NotDeclaredTypeError

			if value:
				raise InitializingObjectError

		#SIMPLE TYPE
		else:
			#CHECK IF PROPER TYPE ASSIGNED
			if value:
				l_type = type_spec
				r_type = self.get_r_value_type(value)
				self.compare_types(l_type, r_type)

		var = VariableStruct(type_spec)
		self.current_env.dict[name] = Entity(EntityType.Var, var)

	#after leaving fun_env
	def add_function_definition(self, type_, id_):
		if not self.check_syntax:
			return
		name = id_.name
		self.current_env.name = name
		fun = FunctionStruct(type_, self.current_env)
		self.current_env.parent.dict[name] = Entity(EntityType.Fun, fun)

	#pre leaving class_env
	def add_class(self, id_):
		if not self.check_syntax:
			return
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

	def check_fun_identifier(self, id_):
		if not self.check_syntax:
			return
		env = self.current_env
		if env.parent:
			env = env.parent
		if env.find_local(id_.name):
			raise AlreadyDeclaredError

	def check_parameter(self, param):
		if not self.check_syntax:
			return
		type_spec, name = param.type, param.name.name
		if self.current_env.find_local(name):
			raise AlreadyDeclaredError()
		var = VariableStruct(type_spec)
		self.current_env.dict[name] = Entity(EntityType.Var, var)

	def check_return(self, jump):
		if not self.check_syntax:
			return
		env = self.current_env
		while env != self.global_env:
			if env.env_type == EnvType.Fun:
				fun_name = env.name
				return_var = jump.returnable
				if isinstance(return_var, Identifier) or isinstance(return_var, Id):
					return_var = self.check_id(return_var)
					if return_var.type_ != EntityType.Var:
						raise NotAVariableError
					return_var = return_var.struct.type_

				env = env.parent
				fun = env.find_local(fun_name)
				ret_type = fun.struct.type_
				if isinstance(ret_type, TypeSpec) and ret_type == TypeSpec('void'):
					if return_var:
						raise WrongTypeReturnError('Should return void')
					else:
						return
				try:
					self.compare_types(ret_type, return_var)
				except:
					raise WrongTypeReturnError('Wrong return type')
				return
			env = env.parent
		raise ReturnOutsideFunctionError('Return statement outside function')

	def check_if_inside_loop(self):
		if not self.check_syntax:
			return
		env = self.current_env
		while env != self.global_env:
			if env.env_type == EnvType.Loop:
				return
			env = env.parent
		raise JumpStmtOutsideLoopError('Continue or break outside loop')
