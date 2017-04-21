from lexer import *

class Result:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)


class Parser:
    def __call__(self, tokens, pos):
        return None  # subclasses will override this

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
           tokens[pos][0] == self.value and \
           tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result


class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return Result(None, pos)


class Rep(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)


class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None


class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result      


#from equality import *
class Equality:
	pass 

class Aexp(Equality):
    pass

class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return self.i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i


class FloatAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'FloatAexp(%d)' % self.i


class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            #return 0
            raise RuntimeError('unknown variable: ' + self.name)

    def __repr__(self):
        return 'VarAexp(%s)' % self.name


class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)



class Bexp(Equality):
    pass

class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return valu

    def __repr__(self):
        return 'RelopAexp(%s, %s, %s)' % (self.op, self.left, self.right)


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
    	value = self.exp.eval(env)
    	return not value


class Statement(Equality):
    pass

class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def eval(self, env):
    	value = self.aexp.eval(env)
    	env[self.name] = value

    def __repr__(self):
        return 'AssignStmt(=, %s, %s)' % (self.name, self.aexp)


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
    	self.first.eval(env)
    	self.second.eval(env)


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
    	condition_value = self.condition.eval(env)
    	if condition_value:
    		self.true_stmt.eval(env)
    	else: 
    		if self.false_stmt:
    			self.false_stmt.eval(env)


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
    	condition_value = self.condition.eval(env)
    	while condition_value:
    		self.body.eval(env)
    		condition_value = self.condition.eval(env)
			    	

#class ForStatement(Statement):
#    def __init__(self, condition, body):
#        ...



def keyword(kw):
    if kw in keyword_tags:
        return Reserved(kw, keyword_tags[kw])
    return Reserved(kw, None)

id = Tag(TokenType.Identifier)

num = Tag(TokenType.IntNum) ^ (lambda i: int(i))

def aexp_value():
	return (num ^ (lambda i: IntAexp(i))) | \
	(id  ^ (lambda v: VarAexp(v)))

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def aexp_group():
	return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group

def aexp_term():
    return aexp_value() | aexp_group()

def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

from functools import reduce

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)




def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_not():
    return keyword('!') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

bexp_precedence_levels = [
    ['&&'],
    ['||'],
]

def process_logic(op):
    if op == '&&':
        return lambda l, r: AndBexp(l, r)
    elif op == '||':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)





def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + aexp() ^ process


def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process


def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process



def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()


def parser():
    return Phrase(stmt_list())    

def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast

import sys


if __name__ == '__main__':
	if len(sys.argv) != 3:
	    sys.stderr.write('usage: %s filename parsername' % sys.argv[0])
	    sys.exit(1)
	filename = sys.argv[1]
	file = open(filename)
	characters = file.read()
	file.close()
	tokens = imp_lex(characters)
	#result = imp_parse(tokens)
	parser = globals()[sys.argv[2]]()
	result = parser(tokens, 0)
	print(result)
"""

def test():
	filename = "test.cpp"
	file = open(filename)
	characters = file.read()
	file.close()
	tokens = imp_lex(characters)
	parser = globals()["aexp"]()
	result = parser(tokens, 0)
	print(result)
	return result;

"""