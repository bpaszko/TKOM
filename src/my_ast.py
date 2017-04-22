#from equality import *
class Equality:
	pass 



class Aexp(Equality):
    pass

class IntNum(Aexp):     #IntAexp
    def __init__(self, i):
        self.i = int(i)

    def __eq__(self, other):
        return self.i == other.i

    def __repr__(self):
        return 'IntNum(%s)' % self.i



class FloatNum(Aexp):
    def __init__(self, i):
        self.i = i



class Identifier(Aexp):     #VarAexp
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return  self.name == other.name

    def __repr__(self):
        return 'Identifier(%s)' % self.name



class BinopAexp(Aexp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.left, self.op, self.right)



class Bexp(Equality):
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



class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __eq__(self, other):
        return self.condition == other.condition and self.true_stmt == other.true_stmt and self.false_stmt == other.false_stmt

    def __repr__(self):
        return 'IfStmt(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)



class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __eq__(self, other):
        return self.condition == other.condition

    def __repr__(self):
        return 'WhileStmt(%s, %s)' % (self.condition, self.body)

#class ForStatement(Statement):
#    def __init__(self, condition, body):
#        ...


class AssignExp(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def __repr__(self):
        return 'AssignExp(%s, =, %s)' % (self.name, self.value)

class Decl():
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value

    def __eq__(self, other):
        return self.parameter == other.parameter and self.value == other.value 

    def __repr__(self):
        return 'Decl(%s, =, %s)' % (self.parameter, self.value)


class TypeSpec():
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'TypeSpec(%s)' % (self.value)


class Param():
    def __init__(self, type, name):
        self.type=type
        self.name=name

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name

    def __repr__(self):
        return 'Param(%s, %s)' % (self.type, self.name)