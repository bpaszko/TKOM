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
	def __init__(self, id_):
		self.name = id_.to_name()

	def __str__(self):
		return '%s is not callable' % (self.name)

class WrongNumberOfArgsError(SemanticError):
	def __init__(self, fun, params_num, args_num):
		self.fun_name = fun.to_name()
		self.params_num = params_num
		self.args_num = args_num

	def __str__(self):
		return '%s takes %d args, got %d' % (self.fun_name, self.params_num, self.args_num)

class NotAVariableError(SemanticError):
	#def __init__(self, id_):
	#	self.name = id_.to_name()

	#def __str__(self):
	#	return '%s is not a variable' % (self.name)
	pass 
	
class LValueNotAVariableError(SemanticError):
	def __init__(self, id_):
		self.name = id_.to_name()

	def __str__(self):
		return '%s is not a variable' % (self.name)


class ReturnOutsideFunctionError(SemanticError):
	pass

class JumpStmtOutsideLoopError(SemanticError):
	pass

class WrongTypeReturnError(SemanticError):
	pass

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
	pass

#TODO
class InvalidArgError(SemanticError):
	def __init__(self, fun_name, param_type, arg_type):
		self.fun_name = fun_name
		self.param_type = param_name
		self.arg_type = arg_type

	def __str__(self):
		return '%s requires %s, got %s' % (self.fun_name, self.param_type, self.arg_type)

class UnknownTypeError(SemanticError):
	pass

class NotCompatibileTypeInExpressionError(SemanticError):
	def __init__(self, id_):
		self.name = id_.to_name()

	def __str__(self):
		return 'Cannot use object of type ' % (self.name)

class NotAnObjectError(SemanticError):
	pass