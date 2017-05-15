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

	def name_env(self, name):
		self.current_env.name = name

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
	def get_var_class_name(var_entity, var_id, *, check=True):
		#TAKES ENTITY AND RETURNS VARIABLE CLASS
		if check:
			if not isinstance(var_entity, Entity):
				raise Exception("Not an Entity")
		if not isinstance(var_entity.struct.type_, Identifier) or var_entity.type_ != EntityType.Var:
			raise NotAnObjectError(var_id.to_text())
		return var_entity.struct.type_.name

	#gets id or identifier and returns entity if exist
	#raises NotAVariable, NotAnObject, NotDeclaredVariable, NotAClassMember
	def check_if_valid_id(self, id_):
		if not self.check_syntax:
			return
		if isinstance(id_, Id):
			variable_to_check = id_.parent
			variable_entity = self.check_if_declared_variable(variable_to_check)
			while(isinstance(id_, Id)):
				variable_class = Semantic.get_var_class_name(variable_entity, variable_to_check)
				variable_to_check = id_ = id_.child
				if isinstance(id_, Id):
					variable_to_check = id_.parent
				variable_entity = self.check_if_part_of_class(variable_to_check.name, variable_class)
				if not variable_entity:
					raise NotAClassMemberError(variable_to_check.to_text(), variable_class)
				access = variable_entity.struct.access
				if access != 'public':
					raise AccessSpecifierError(variable_to_check.to_text(), variable_class, access)
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
			raise NotAVariableError(id_.to_text())
		return var_entity

	def check_if_id_is_function(self, id_):
		fun_entity = self.check_if_valid_id(id_)
		if not isinstance(fun_entity, Entity):
			raise Exception('Not an entity')
		if fun_entity.type_ != EntityType.Fun:
			raise NotCallableError(id_.to_text()) 
		return fun_entity

	@staticmethod
	#return dict {param:entity}
	def get_function_parameters(fun_entity, *, check=True):
		if check:
			if not isinstance(fun_entity, Entity):
				raise Exception('Not an entity')
			if entity.type_ != EntityType.Fun:
				raise NotCallableError(id_.to_text())
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
		if isinstance(arg, Literal):
			return 'Literal'
		if isinstance(arg, TypeSpec) and arg == TypeSpec('void'):
			return 'Void'
		return str(type(arg).__name__)

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
			('Void', 'TypeSpec') : lambda x,y: False, 
			('Void', 'Identifier') : lambda x,y: False, 
			('Void', 'Literal') : lambda x,y: False,
			('Void', 'Void') : lambda x,y: True, 
		}
		if (first_name, second_name) in type_dict:
			compare = type_dict[(first_name, second_name)]
			return compare(first, second)
		if (second_name, first_name) in type_dict:
			compare = type_dict[(second_name, first_name)]
			return compare(second, first)
		raise Exception("Unknown types")

	@staticmethod #MAYBE ADDITIONAL CHECK LATER && VOIDS?
	def throw_invalid_arg_error(id_, param_type, arg_type):
		param_name, arg_name = Semantic.adjust_type(param_type), Semantic.adjust_type(arg_type)
		type_dict = {
			('Identifier', 'TypeSpec') : lambda x,y : (x.to_text(), str(y.value)),
			('Identifier', 'Identifier') : lambda x,y: (x.to_text(), y.to_text()),
			('Identifier', 'Literal') : lambda x,y: (x.to_text(), str(y.value)),
			('TypeSpec', 'Identifier') : lambda x,y : (str(x.value), y.to_text()),
		}
		fun_name = id_.to_text()
		gen_types_str = type_dict[(param_name, arg_name)]
		param, arg = gen_types_str(param_type, arg_type)
		raise InvalidArgError(fun_name, param, arg)


	def check_if_funcall_arguments_are_valid(self, fun_entity, funcall):
		id_, args = funcall.name, funcall.args
		params = Semantic.get_function_parameters(fun_entity, check=False)
		if len(params) != len(args):
			raise WrongNumberOfArgsError(id_.to_text(), len(params), len(args))
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
	


	def check_if_id_is_simple_type_variable(self, id_):
		if not self.check_syntax:
			return
		var_entity = self.check_if_id_is_variable(id_)
		var_type = Semantic.get_entity_return_type(var_entity, check=False)
		if isinstance(var_type, Identifier):
			raise NotCompatibileTypeInExpressionError(id_.to_text())


	@staticmethod #MAYBE ADDITIONAL CHECK LATER && VOIDS?
	def throw_assign_mismatch_type_error(l_type, r_type):
		l_type_name, r_type_name = Semantic.adjust_type(l_type), Semantic.adjust_type(r_type)
		type_dict = {
			('Identifier', 'TypeSpec') : lambda x,y : (x.to_text(), str(y.value)),
			('Identifier', 'Identifier') : lambda x,y: (x.to_text(), y.to_text()),
			('Identifier', 'Literal') : lambda x,y: (x.to_text(), str(y.value)),
			('TypeSpec', 'Identifier') : lambda x,y : (str(x.value), y.to_text()),
		}
		gen_types_str = type_dict[(l_type_name, r_type_name)]
		l_type, r_type = gen_types_str(l_type, r_type)
		raise AssignMismatchTypeError(l_type, r_type)

	def get_r_value_type(self, value):
		if isinstance(value, Aexp):
			return TypeSpec('aexp') #TODO
		if isinstance(value, Bexp):
			return TypeSpec('bexp')
		if type(value) in [Id, Identifier]:
			var_entity = self.check_if_id_is_variable(value) #NEED?
			var_type = Semantic.get_entity_return_type(var_entity)
			return var_type
		if isinstance(value, FunCall):
			fun_id = value.name
			fun_entity = self.check_if_id_is_function(fun_id) #NEED?
			fun_type = Semantic.get_entity_return_type(fun_entity)
			return fun_type
		raise UnknownTypeError


	def check_if_valid_assignment(self, assign):
		if not self.check_syntax:
			return
		id_, value = assign.name, assign.value
		var_entity = self.check_if_id_is_variable(id_)
		l_type = Semantic.get_entity_return_type(var_entity)
		r_type = self.get_r_value_type(value)
		if not Semantic.check_two_types_compatibility(l_type, r_type):
			Semantic.throw_assign_mismatch_type_error(l_type, r_type)




	def check_for_condition(self, cond, decl):
		if not self.check_syntax:
			return
		id_ = cond.left
		id_2 = decl.parameter.name
		if id_ != id_2:
			raise InvalidForConditionError(id_.to_text(), id_2.to_text())

	def check_for_increment(self, assign, decl):
		if not self.check_syntax:
			return
		id_1, binop = assign.name, assign.value
		id_2, literal = binop.left, binop.right
		id_3 = decl.parameter.name
		if id_1 != id_3 or id_2 != id_3 or not isinstance(literal, IntNum):
			raise InvalidForIncrementError #TODO


	def check_if_declared_class(self, name):
		class_entity = self.global_env.find_local(name)
		if not class_entity:
			raise NotDeclaredTypeError(name)
		if class_entity.type_ != EntityType.Class:
			raise NotAClassError(name)


	def add_declaration(self, decl, access='public'):
		if not self.check_syntax:
			return
		parameter, value = decl.parameter, decl.value
		var_type, var_id = parameter.type, parameter.name
		var_name = var_id.name
		#OBJECT
		if isinstance(var_type, Identifier):
			class_name = var_type.name
			self.check_if_declared_class(class_name)

			if value:
				raise InitializingObjectError(var_name)
		else:
			if isinstance(var_type, TypeSpec) and var_type.value == 'void':
				raise VoidVariableDeclarationError(var_name) #TEST
			#CHECK IF PROPER TYPE ASSIGNED
			if value:
				l_type = var_type
				r_type = self.get_r_value_type(value)
				if not Semantic.check_two_types_compatibility(l_type, r_type):
					Semantic.throw_assign_mismatch_type_error(l_type, r_type)

		var_entity = Entity(EntityType.Var, VariableStruct(var_type, access))
		self.current_env.dict[var_name] = var_entity





	def add_function_definition(self, return_type, id_, access='public'): #FUN NAME CHECK
		if not self.check_syntax:
			return
		parent_env = self.current_env.parent
		fun_name = id_.name
		if parent_env.find_local(fun_name):
			raise AlreadyDeclaredError(fun_name)

		self.name_env(fun_name)
		fun_entity = Entity(EntityType.Fun, FunctionStruct(return_type, self.current_env, access))
		parent_env.dict[fun_name] = fun_entity


	def check_if_not_colliding_class_identifier(self, name):
		if self.global_env.find_local(name):
			raise AlreadyDeclaredError(name) 

	#pre leaving class_env
	def add_class(self, id_):
		if not self.check_syntax:
			return
		name = id_.name
		self.check_if_not_colliding_class_identifier(name)
		class_entity = Entity(EntityType.Class, ClassStruct(self.current_env))
		self.global_env.dict[name] = class_entity
		self.name_env(name)


	def check_parameter(self, param):
		if not self.check_syntax:
			return
		type_spec, name = param.type, param.name.name
		if self.current_env.find_local(name):
			raise AlreadyDeclaredError(name)
		parent = self.current_env.parent
		if parent and parent.env_type == EnvType.Fun:
			if parent.find_local(name):
				raise AlreadyDeclaredError(name)

	def add_parameter(self, param, access='public'):
		self.check_parameter(param)
		type_spec, name = param.type, param.name.name
		var = VariableStruct(type_spec, access)
		self.current_env.dict[name] = Entity(EntityType.Var, var)


	def check_if_inside_loop(self):
		if not self.check_syntax:
			return
		env = self.current_env
		while env != self.global_env:
			if env.env_type == EnvType.Loop:
				return
			env = env.parent
		raise JumpStmtOutsideLoopError('Continue or break outside loop')


	@staticmethod
	def throw_wrong_return_type_error(fun_name, fun_ret_type, return_type):
		fun_ret_type_name = Semantic.adjust_type(fun_ret_type)
		return_type_name = Semantic.adjust_type(return_type)
		type_dict = {
			('Identifier', 'TypeSpec') : lambda x,y : (x.to_text(), str(y.value)),
			('Identifier', 'Identifier') : lambda x,y: (x.to_text(), y.to_text()),
			('Identifier', 'Literal') : lambda x,y: (x.to_text(), str(y.value)),
			('TypeSpec', 'Identifier') : lambda x,y : (str(x.value), y.to_text()),
			('Void', 'TypeSpec') : lambda x,y: ('None', str(y.value)), 
			('Void', 'Identifier') : lambda x,y: ('None', y.to_text()), 
			('Void', 'Literal') : lambda x,y: ('None', str(y.value)), 
			('TypeSpec', 'Void') : lambda x,y: (str(x.value), 'None'), 
			('Identifier', 'Void') : lambda x,y: (x.to_text(), 'None'), 
		}
		gen_types_str = type_dict[(fun_ret_type_name, return_type_name)]
		fun_ret, ret = gen_types_str(fun_ret_type, return_type)
		raise WrongReturnTypeError(fun_name, fun_ret, ret)

	
	def get_return_variable_type(self, return_var):
		if isinstance(return_var, Identifier) or isinstance(return_var, Id):
			return_entity = self.check_if_id_is_variable(return_var)
			return_type = Semantic.get_entity_return_type(return_entity, check=False)
			return return_type;
		if not return_var:
			return TypeSpec('void')
		return return_var


	def check_return(self, jump_stmt):
		if not self.check_syntax:
			return
		env = self.current_env
		while env != self.global_env:
			if env.env_type == EnvType.Fun:
				fun_name = env.name
				return_var = jump_stmt.returnable
				return_type = self.get_return_variable_type(return_var)

				env = env.parent
				fun_entity = env.find_local(fun_name)
				#CHECK IF FUN?
				fun_type = Semantic.get_entity_return_type(fun_entity)
				if not Semantic.check_two_types_compatibility(fun_type, return_type):
					Semantic.throw_wrong_return_type_error(fun_name, fun_type, return_type)
				return
			env = env.parent
		raise ReturnOutsideFunctionError('Return statement outside function')
	