#from equality import *
class Equality:
    pass

class Aexp:
    pass

class Literal(Aexp):
    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'Literal(%s)' % self.value

    def __hash__(self):
        return hash(self.value)

class IntNum(Literal):  # IntAexp
    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'IntNum(%s)' % self.value


class FloatNum(Literal):
    def __init__(self, value):
        self.value = float(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'FloatNum(%s)' % self.value


class Character(Literal):
    def __init__(self, value):
        self.value = value[1:2]

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'Char(%s)' % self.value


class Id:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __eq__(self, other):
        return self.parent == other.parent and self.child == other.child

    def __repr__(self):
        return 'Id(%s, %s)' % (self.parent, self.child)

    def to_name(self):
        return '%s.%s' % (self.parent.to_name(), self.child.to_name())
 

class Identifier:  # VarAexp
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return 'Identifier(%s)' % self.name

    def to_name(self):
        return self.name


class BinopAexp(Aexp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.left, self.op, self.right)


class Bexp:
    pass


class BoolLit(Bexp):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'BoolLit(%s)' % self.value


class RelopBexp(Bexp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.left, self.op, self.right)


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __eq__(self, other):
        return self.exp == other.exp

    def __repr__(self):
        return 'NotBexp(%s)' % (self.exp)


class Statement(Equality):
    pass


class CompoundStmt(Statement):
    def __init__(self, statements):
        self.statements = statements

    def __eq__(self, other):
        return self.statements == other.statements

    def __repr__(self):
        return 'CompoundStmt(%s)' % (self.statements)


class IfStmt(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __eq__(self, other):
        return self.condition == other.condition and self.true_stmt == other.true_stmt and self.false_stmt == other.false_stmt

    def __repr__(self):
        return 'IfStmt(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)


class WhileStmt(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __eq__(self, other):
        return self.condition == other.condition

    def __repr__(self):
        return 'WhileStmt(%s, %s)' % (self.condition, self.body)


class JumpStmt(Statement):
    def __init__(self, value, returnable=None):
        self.value = value
        self.returnable = returnable

    def __eq__(self, other):
        return self.value == other.value and self.returnable == other.returnable

    def __repr__(self):
        return 'JumpStmt(%s, %s)' % (self.value, self.returnable)


class ForStmt(Statement):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def __eq__(self, other):
        return self.init == other.init and self.condition == other.condition and \
            self.increment == other.increment and self.body == other.body

    def __repr__(self):
        return 'ForStmt(%s, %s, %s, %s)' % (self.init, self.condition, self.increment, self.body)


class AssignExp(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def __repr__(self):
        return 'AssignExp(%s, =, %s)' % (self.name, self.value)


class Decl:
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value

    def __eq__(self, other):
        return self.parameter == other.parameter and self.value == other.value

    def __repr__(self):
        return 'Decl(%s, =, %s)' % (self.parameter, self.value)


class TypeSpec:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'TypeSpec(%s)' % (self.value)


class Param:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name

    def __repr__(self):
        return 'Param(%s, %s)' % (self.type, self.name)


class Program:
    def __init__(self, definitions):
        self.definitions = definitions

    def __eq__(self, other):
        return self.definitions == other.definitions

    def __repr__(self):
        return 'Program(%s)' % (self.definitions)

class FunDef:
    def __init__(self, type, name, parameters, body):
        self.type = type
        self.name = name
        self.parameters = parameters
        self.body = body

    def __eq__(self, other):
        return self.type == other.type and  self.name == other.name and\
            self.parameters == other.parameters and self.body == other.body

    def __repr__(self):
        return 'FunDef(%s, %s, %s, %s)' % (self.type, self.name, self.parameters, self.body)

class Class:
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __eq__(self, other):
        return self.name == other.name and self.members == other.members

    def __repr__(self):
        return 'Class(%s, %s)' % (self.name, self.members)

class AccessMembers:
    def __init__(self, access_specifier, members_declarations):
        self.access_specifier = access_specifier
        self.members_declarations = members_declarations

    def __eq__(self, other):
        return self.access_specifier == other.access_specifier and \
            self.members_declarations == other.members_declarations

    def __repr__(self):
        return 'AccessMembers(%s, %s)' % (self.access_specifier, self.members_declarations)

class FunCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

    def __repr__(self):
        return 'FunCall(%s, %s)' % (self.name, self.args)