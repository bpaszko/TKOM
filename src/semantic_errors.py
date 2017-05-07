class SemanticError(Exception):
	pass

class NotDeclaredVariableError(SemanticError):
	pass

class NotAClassMemberError(SemanticError):
	pass

class NotCallableError(SemanticError):
	pass

class WrongNumberOfArgsError(SemanticError):
	pass

class NotAVariableError(SemanticError):
	pass

class LValueNotAVariableError(SemanticError):
	pass

class ReturnOutsideFunctionError(SemanticError):
	pass

class JumpStmtOutsideLoopError(SemanticError):
	pass

class WrongTypeReturnError(SemanticError):
	pass

class InitializingObjectError(SemanticError):
	pass

class NotDeclaredTypeError(SemanticError):
	pass

class InvalidForIncrementError(SemanticError):
	pass

class InvalidForConditionError(SemanticError):
	pass

class AlreadyDeclaredError(SemanticError):
	pass

class AssignMismatchTypeError(SemanticError):
	pass

class InvalidArgError(SemanticError):
	pass

class UnknownTypeError(SemanticError):
	pass

class NotCompatibileTypeInExpressionError(SemanticError):
	pass