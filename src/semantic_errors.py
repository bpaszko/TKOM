class SemanticError(Exception):
	pass

class NotDeclaredVariableError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s has not been declared' % (self.name)

class NotAClassMemberError(SemanticError):
	def __init__(self, var, class_):
		self.var = var
		self.class_ = class_

	def __str__(self):
		return '%s is not a member of %s' % (self.var, self.class_)

class NotCallableError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s is not callable' % (self.name)

class WrongNumberOfArgsError(SemanticError):
	def __init__(self, fun, params_num, args_num):
		self.fun_name = fun
		self.params_num = params_num
		self.args_num = args_num

	def __str__(self):
		return '%s takes %d args, got %d' % (self.fun_name, self.params_num, self.args_num)

class NotAVariableError(SemanticError):
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return '%s is not a variable' % (self.name) 

class LValueNotAVariableError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s is not a variable' % (self.name)

class WrongReturnTypeError(SemanticError):
	def __init__(self, fun_name, fun_ret, ret):
		self.fun_name = fun_name
		self.fun_ret = fun_ret
		self.ret = ret

	def __str__(self):
		return 'Function %s should return: %s, instead of: %s' \
			% (self.fun_name, self.fun_ret, self.ret)

class InitializingObjectError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s is an object and cannot be initialized' % (self.name)

class NotDeclaredTypeError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'Type %s has not been declared' % (self.name)

class InvalidForIncrementError(SemanticError):
	pass

class InvalidForConditionError(SemanticError):
	def __init__(self, name_1, name_2):
		self.name_1 = name_1
		self.name_2 = name_2

	def __str__(self):
		return 'For requires %s and %s be the same variable' % (self.name_1, self.name_2)

class AlreadyDeclaredError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s has already been declared' % (self.name)

class AssignMismatchTypeError(SemanticError):
	def __init__(self, type_1, type_2):
		self.type_1 = type_1
		self.type_2 = type_2

	def __str__(self):
		return 'Cannot assign %s to %s' % (self.type_2, self.type_1)


class InvalidArgError(SemanticError):
	def __init__(self, fun_name, param_type, arg_type):
		self.fun_name = fun_name
		self.param_type = param_type
		self.arg_type = arg_type
	
	def __str__(self):
		return '%s requires %s, got %s' % (self.fun_name, self.param_type, self.arg_type)

class NotCompatibileTypeInExpressionError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'Cannot use object of type ' % (self.name)

class NotAClassError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s is not a class name' % (self.name)

class NotAnObjectError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s is not an object' % self.name

class VoidVariableDeclarationError(SemanticError):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'Declaring void variable: %s' % self.name

class AccessSpecifierError(SemanticError):
	def __init__(self, var, class_, access):
		self.var = var
		self.class_ = class_
		self.access = access

	def __str__(self):
		return 'Trying to access %s, which is %s field of class %s.' % \
			(self.var, self.access, self.class_)


class UnknownTypeError(SemanticError):
	pass

class ReturnOutsideFunctionError(SemanticError):
	pass

class JumpStmtOutsideLoopError(SemanticError):
	pass