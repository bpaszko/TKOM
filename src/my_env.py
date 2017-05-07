from enum import Enum, auto

class EnvType(Enum):
	Fun = auto()
	Loop = auto()
	Class = auto()
	Compound = auto()
	If = auto()
	Else = auto()

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
	def __init__(self, type_):
		self.type_ = type_

	def __repr__(self):	
		return '%s' % self.type_

class FunctionStruct:
	def __init__(self, type_, env):
		self.type_ = type_
		self.env = env #USED TO CHECK ARGS

	def __repr__(self):
		return '%s, %s' % (self.type_,self.env) 

class ClassStruct:
	def __init__(self, env):
		self.env = env

	def __repr__(self):
		return ''

class Env:
	def __init__(self, parent=None, name=None, env_type=None):
		self.name = name
		self.env_type = env_type
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