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

	#gets identifier and returns entity if declared, else None
	def check_if_declared_variable(self, identifier):
		if not self.check_syntax:
			return
		return self.current_env.find(identifier.name)

	#gets identifier and class name and returns entity if variable is member of class, else None
	def check_if_part_of_class(self, var, class_name):
		class_ = self.global_env.find_local(class_name)
		class_env = class_.struct.env
		if class_env:
			return class_env.find_local(var)


	@staticmethod
	def get_var_class_name(variable):
		#TAKES ENTITY AND RETURNS VARIABLE CLASS
		if not isinstance(variable, Entity) or variable.type_ != EntityType.Var:
			raise NotAVariableError
		if not isinstance(variable.struct.type_, Identifier):
			raise NotAnObjectError
		return variable.struct.type_.name

	#gets id or identifier and returns entity if exist
	#raises NotAVariable, NotAnObject, NotDeclaredVariable, NotAClassMember
	def check_if_valid_id(self, id_):
		if not self.check_syntax:
			return
		if isinstance(id_, Id):
			variable_to_check = id_.parent
			variable_entity = self.check_if_declared_variable(variable_to_check)
			while(isinstance(id_, Id)):
				variable_class = Semantic.get_var_class_name(variable_entity)
				variable_to_check = id_ = id_.child
				if isinstance(id_, Id):
					variable_to_check = id_.parent
				variable_entity = self.check_if_part_of_class(variable_to_check.name, variable_class)
				if not variable_entity:
					raise NotAClassMemberError(variable_to_check.to_name(), variable_class)
			return variable_entity
		else:
			variable_entity = self.check_if_declared_variable(id_)
			if not variable_entity:
				raise NotDeclaredVariableError(id_.name)
			return variable_entity
	
	#CAN MERGE THESE 2
	def check_if_id_is_variable(self, id_):
		var_entity = self.check_if_valid_id(id_)
		if not isinstance(var_entity, Entity):
			raise Exception('Not an entity')
		if var_entity.type_ != EntityType.Var:
			raise NotCallableError(id_) #TO NAME
		return var_entity

	def check_if_id_is_function(self, id_):
		fun_entity = self.check_if_valid_id(id_)
		if not isinstance(fun_entity, Entity):
			raise Exception('Not an entity')
		if fun_entity.type_ != EntityType.Fun:
			raise NotCallableError(id_) #TO NAME
		return fun_entity

	@staticmethod
	#return dict {param:entity}
	def get_function_parameters(fun_entity, *, check=True):
		if check:
			if not isinstance(fun_entity, Entity):
				raise Exception('Not an entity')
			if entity.type_ != EntityType.Fun:
				raise NotCallableError(id_) #TO NAME
			return fun_entity
		return fun_entity.struct.env.dict

	@staticmethod
	def get_entity_return_type(entity, *, check=True):
		if check:
			if not isinstance(entity, Entity):
				raise Exception("Not an Entity")
			if entity.type_ == EntityType.Class:
				raise Exception("Class doesn't have return type")
		return entity.struct.type_

	@staticmethod
	def adjust_type(arg):
		return 'Literal' if isinstance(arg, Literal) else str(type(arg).__name__)
	

	@staticmethod # VOIDS?
	def check_two_types_compatibility(first, second):
		first_name = Semantic.adjust_type(first)
		second_name = Semantic.adjust_type(second)
		type_dict = {
			('TypeSpec', 'TypeSpec') : lambda x,y: True,
			('Literal', 'TypeSpec') : lambda x,y: True,
			('Identifier', 'TypeSpec') : lambda x,y : False,
			('Identifier', 'Identifier') : lambda x,y: x==y,
			('Literal', 'Literal') : lambda x,y: True,
			('Identifier', 'Literal') : lambda x,y: False,
		}
		if (first_name, second_name) in type_dict:
			compare = type_dict[(first_name, second_name)]
			return compare(first, second)
		if (second_name, first_name) in type_dict:
			compare = type_dict[(second_name, first_name)]
			return compare(second, first)
		raise Exception("Not known types")

	@staticmethod #MAYBE ADDITIONAL CHECK LATER && VOIDS?
	def throw_invalid_arg_error(id_, param_type, arg_type):
		param_name, arg_name = Semantic.adjust_type(param_type), Semantic.adjust_type(arg_type)
		type_dict = {
			('Identifier', 'TypeSpec') : lambda x,y : (x.to_name(), str(y.value)),
			('Identifier', 'Identifier') : lambda x,y: (x.to_name(), y.to_name()),
			('Identifier', 'Literal') : lambda x,y: (x.to_name(), str(y.value)),
			('TypeSpec', 'Identifier') : lambda x,y : (str(x.value), y.to_name()),
		}
		fun_name = id_.to_name()
		gen_types_str = type_dict[(param_name, arg_name)]
		param, arg = gen_types_str(param_type, arg_type)
		raise InvalidArgError(fun_name, param, arg)


	def check_if_funcall_arguments_are_valid(self, fun_entity, funcall):
		id_, args = funcall.name, funcall.args
		params = Semantic.get_function_parameters(fun_entity, check=False)
		if len(params) != len(args):
			raise WrongNumberOfArgsError(id_, len(params), len(args))
		for arg, param_entity in zip(args, params.values()):
			param_type = Semantic.get_entity_return_type(param_entity, check=False)
			if isinstance(arg, Identifier) or isinstance(arg, Id): #fun(x)
				arg_entity = self.check_if_id_is_variable(arg)
				arg_type = Semantic.get_entity_return_type(arg_entity, check=False)
				if not Semantic.check_two_types_compatibility(arg_type, param_type):
					Semantic.throw_invalid_arg_error(id_, param_type, arg_type)
			else: #fun(2)
				if not Semantic.check_two_types_compatibility(arg, param_type):
					Semantic.throw_invalid_arg_error(id_, param_type, arg)

	#used by parser, gets funcall
	#raises ...
	def check_if_valid_funcall(self, funcall):
		if not self.check_syntax:
			return
		fun_id = funcall.name
		fun_entity = self.check_if_id_is_function(fun_id)
		self.check_if_funcall_arguments_are_valid(fun_entity, funcall)
	










	def check_if_simple_type(self, var):
		if not self.check_syntax:
			return
		if var.type_ != EntityType.Var:
			raise NotAVariableError('name')# TODO CATCH IN PARSER OR SPLIT AEXP
		#CHECK IF VAR NOT FUN OR CLASS TODOOO
		type_ = var.struct.type_
		if isinstance(type_, Identifier):
			raise NotCompatibileTypeInExpressionError('name')	# TODO

	def check_assignment(self, assign):
		if not self.check_syntax:
			return
		id_, value = assign.name, assign.value
		var = self.check_if_valid_id(id_)
		if var.type_ != EntityType.Var:
			#raise LValueNotAVariableError(id_)
			raise LValueNotAVariableError(id_.to_name())
		l_type = var.struct.type_
		r_type = self.get_r_value_type(value)
		self.compare_types(l_type, r_type)

	def check_for_condition(self, cond, decl):
		if not self.check_syntax:
			return
		id_ = cond.left
		id_2 = decl.parameter.name
		if id_ != id_2:
			raise InvalidForConditionError(id_.to_name(), id_2.to_name())

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
			var = self.check_if_valid_id(value)
			if var.type_ != EntityType.Var:
				raise NotAVariableError
			type_ = var.struct.type_
			return type_
		if isinstance(value, FunCall):
			name = value.name
			fun = self.check_if_valid_id(name)
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

		#OBJECT
		if isinstance(type_spec, Identifier):
			#INIT PROHIBITED
			#check if class exist
			if not self.global_env.find_local(type_spec.name):
				raise NotDeclaredTypeError(type_spec.name)

			if value:
				raise InitializingObjectError(name)

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
		self.name_env(id_)

	def name_env(self, id_):
		if not self.check_syntax:
			return
		self.current_env.name = id_.name

	def check_identifier(self, id_):
		if not self.check_syntax:
			return
		if self.check_if_declared_variable(id_):
			raise AlreadyDeclaredError(id_.name)

	def check_fun_identifier(self, id_):
		if not self.check_syntax:
			return
		env = self.current_env
		if env.parent:
			env = env.parent
		if env.find_local(id_.name):
			raise AlreadyDeclaredError(id_.name)

	def check_parameter(self, param):
		if not self.check_syntax:
			return
		type_spec, name = param.type, param.name.name
		if self.current_env.find_local(name):
			raise AlreadyDeclaredError(name)
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
					return_var = self.check_if_valid_id(return_var)
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
