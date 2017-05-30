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


from re import findall

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

    def add_paranthesis(self):
        self.paranthesis = False

    def to_text(self):
        return str(self.value)

    def to_python(self, env, py_vars):
        return str(self.value)

class IntNum(Literal):  # IntAexp
    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, other):
        return self.value == other.value

    def get_aexp_type(self, env=None):
        return 'int'

    def get_type(self, env):
        return 'int'

    def __repr__(self):
        return 'IntNum(%s)' % self.value


class FloatNum(Literal):
    def __init__(self, value):
        self.value = float(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'FloatNum(%s)' % self.value

    def get_aexp_type(self, env=None):
        return 'float'

    def get_type(self, env):
        return 'float'


class Character(Literal):
    def __init__(self, value):
        self.value = value[1:2]

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'Char(%s)' % self.value

    def get_aexp_type(self, env=None):
        return 'int'

    def get_type(self, env):
        return 'int'

    def to_python(self, env, py_vars):
        return 'ord(\'' + str(self.value) + '\')'


class Id:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def __eq__(self, other):
        return self.parent == other.parent and self.child == other.child

    def __repr__(self):
        return 'Id(%s, %s)' % (self.parent, self.child)

    def get_aexp_type(self, env):
        ret = get_id_return_type(self, env)
        if isinstance(ret, TypeSpec):
            type_name = ret.value
            if type_name in ['int', 'long', 'bool', 'char']:
                return 'int'
            else:
                return 'float'
        return 'obj'

    def get_type(self, env):
        ret = get_id_return_type(self, env)
        if isinstance(ret, TypeSpec):
            type_name = ret.value
            if type_name in ['int', 'long', 'char']:
                return 'int'
            elif type_name == 'bool':
                return 'bool'
            else:
                return 'float'
        return 'obj'

    def to_text(self):
        return '%s.%s' % (self.parent.to_text(), self.child.to_text())

    def to_python(self, env, py_vars):
        return self.parent.to_python(env, py_vars) + '.' + self.child.to_python(None, py_vars)
  

class Identifier:  # VarAexp
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return 'Identifier(%s)' % self.name

    def get_aexp_type(self, env):
        ret = get_id_return_type(self, env)
        if isinstance(ret, TypeSpec):
            type_name = ret.value
            if type_name in ['int', 'long', 'bool', 'char']:
                return 'int'
            else:
                return 'float'
        return 'obj'

    def get_type(self, env):
        ret = get_id_return_type(self, env)
        if isinstance(ret, TypeSpec):
            type_name = ret.value
            if type_name in ['int', 'long', 'char']:
                return 'int'
            elif type_name == 'bool':
                return 'bool'
            else:
                return 'float'
        return 'obj'

    def to_text(self):
        return self.name

    def to_python(self, env, py_vars):
        code = ''
        while env and env.parent:
            if env.find_local(self.name):
                if env.env_type == EnvType.Class: 
                    code += 'self.'
                break
            env = env.parent

        if self.name in py_vars:
            pass
        elif self.name in py_vars.values():
            get_new_name(self.name, py_vars)
        else:
            py_vars[self.name]=self.name
        code += py_vars[self.name]
        return code

def get_new_name(name, py_vars):
    parts = findall(r'^.*_([0-9]+)$', name)
    if parts:
        part = parts[-1]
        part = str(int(part) + 1)
        new_name = name[:len(name)-len(part)] + part    
        while new_name in py_vars.values():
            part = str(int(part) + 1)
            new_name = name[:len(name)-len(part)] + part
        py_vars[name] = new_name
    elif name[-1] == '_':
        py_vars[name] = name + '1'
    else:
        py_vars[name] = name + '_'



class BinopAexp(Aexp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.paranthesis = False

    def add_paranthesis(self):
        self.paranthesis = True

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.left, self.op, self.right)

    def get_aexp_type(self, env=None):
        return 'int' if self.left.get_aexp_type(env) == 'int' and self.right.get_aexp_type(env) == 'int' \
            else 'float'

    def get_type(self, env):
        return self.get_aexp_type(env)

    def to_python(self, env, py_vars):
        code = ''
        if self.op == '/': 
            if self.left.get_aexp_type(env) == 'int' and self.right.get_aexp_type(env) == 'int':
                code = 'int(' + self.left.to_python(env, py_vars) + ' ' +self.op + \
                    ' ' + self.right.to_python(env, py_vars) + ')'
                return code
        code = self.left.to_python(env, py_vars) + ' ' + self.op + ' ' + \
            self.right.to_python(env, py_vars)
        return '(' + code + ')' if self.paranthesis else code


class Bexp:
    paranthesis = False

    def add_paranthesis(self):
        self.paranthesis = True


class BoolLit(Bexp):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'BoolLit(%s)' % self.value

    def get_aexp_type(self, env=None):
        return 'int'

    def get_type(self, env=None):
        return 'bool'

    def to_python(self, env, py_vars):
        return str(self.value).title()


class RelopBexp(Bexp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.left, self.op, self.right)

    def get_type(self, env=None):
        return 'bool'

    def to_python(self, env, py_vars):
        code = self.left.to_python(env, py_vars) + ' ' + str(self.op) + ' ' + self.right.to_python(env, py_vars)
        return '(' + code + ')' if self.paranthesis else code


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

    def get_type(self, env=None):
        return 'bool'

    def to_python(self, env, py_vars):
        code = self.left.to_python(env, py_vars) + ' and ' + self.right.to_python(env, py_vars)
        return '(' + code + ')' if self.paranthesis else code


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def get_type(self, env=None):
        return 'bool'

    def to_python(self, env, py_vars):
        code = self.left.to_python(env, py_vars) + ' or ' + self.right.to_python(env, py_vars)
        return '(' + code + ')' if self.paranthesis else code


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __eq__(self, other):
        return self.exp == other.exp

    def __repr__(self):
        return 'NotBexp(%s)' % (self.exp)

    def get_type(self, env=None):
        return 'bool'

    def to_python(self, env, py_vars):
        code = 'not ' + self.exp.to_python(env, py_vars)
        return '(' + code + ')' if self.paranthesis else code


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

    def to_python(self, env, py_vars):
        code = self.value
        if self.returnable:
            code += ' ' + self.returnable.to_python(env, py_vars)
        return code


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

    def to_python(self, env, py_vars):
        code = self.name.to_python(env, py_vars) + ' = '# + self.value.to_python(env, py_vars) 
        l_type = get_id_return_type(self.name, env)
        if isinstance(l_type, Id) or isinstance(l_type, Identifier):
            code += self.value.to_python(env, py_vars)
        else:
            modifier = find_type_modifier(l_type.value, self.value.get_type(env))
            if modifier:
                code += modifier + '('
                code += self.value.to_python(env, py_vars)
                code += ')'
            else:
                code += self.value.to_python(env, py_vars)
        return code


default_value = {
    'int' : 0,
    'long' : 0,
    'float': 0.0,
    'double' : 0.0,
    'char' : 0,
    'bool' : False,
}

type_mapping = {
    'float' : 'float',
    'double' : 'float', 
    'int' : 'int',
    'char' : 'int',
    'long' : 'int',
    'bool': 'bool',
}



"""def find_type_modifier(l_type, r_val, env):
    r_type = r_val.get_type(env)
    r_type = type_mapping[r_type]
    l_type = type_mapping[l_type]
    if l_type != r_type:
        return l_type"""

def find_type_modifier(l_type, r_type):
    r_type = type_mapping[r_type]
    l_type = type_mapping[l_type]
    if l_type != r_type:
        return l_type


class Decl:
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value

    def __eq__(self, other):
        return self.parameter == other.parameter and self.value == other.value

    def __repr__(self):
        return 'Decl(%s, =, %s)' % (self.parameter, self.value)

    def to_python(self, env, py_vars):
        code = self.parameter.to_python(None, py_vars) + ' = ' 
        type_ = self.parameter.type
        if isinstance(type_, Identifier):
            code += type_.to_python(env, py_vars) + '()'
        else:
            if self.value:
                modifier = find_type_modifier(type_.value, self.value.get_type(env))
                if modifier:
                    code += modifier + '('
                    code += self.value.to_python(env, py_vars)
                    code += ')'
                else:
                    code += self.value.to_python(env, py_vars)
            else:
                code += str(default_value[type_.value])
        return code

class TypeSpec:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return 'TypeSpec(%s)' % (self.value)

    def get_type(self, env=None):
        return self.value

class Param:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name

    def __repr__(self):
        return 'Param(%s, %s)' % (self.type, self.name)

    def to_python(self, env, py_vars):
        return self.name.to_python(env, py_vars)

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

    def get_type(self, env):
        type_ = get_id_return_type(self.name, env)
        return type_.value

    """def to_python(self, env, py_vars):
                    code = self.name.to_python(env, py_vars) + '(' 
                    for i, arg in enumerate(self.args):
                        #code += arg.to_python(env, py_vars)
                        arg_code = arg.to_python(env,py_vars)
                        if isinstance(arg, Identifier) or isinstance(arg, Id):
                            if isinstance(get_id_return_type(arg, env), Identifier):
                                arg_code = 'deepcopy(' + arg_code + ')'
                        code += arg_code
                        if i < len(self.args) - 1:
                            code += ', '
                    code += ')'
                    return code"""

    def to_python(self, env, py_vars):
        from src.semantic import Semantic
        code = self.name.to_python(env, py_vars) + '(' 
        fun_entity = get_id_entity(self.name, env)
        params = Semantic.get_function_parameters(fun_entity, check=False)
        for i, (arg, param_entity) in enumerate(zip(self.args, params.values())):
            arg_type = arg.get_type(env)
            arg_code = arg.to_python(env,py_vars)

            if isinstance(arg, Identifier) or isinstance(arg, Id):
                #OBJECT
                if isinstance(get_id_return_type(arg, env), Identifier):
                    code += 'deepcopy(' + arg_code + ')'
                #TYPESPEC
                else:
                    param_type = Semantic.get_entity_return_type(param_entity, check=False).value
                    modifier = find_type_modifier(param_type, arg_type)
                    if modifier:
                        code += modifier + '(' + arg_code + ')'
                    else:
                        code += arg_code
            #LITERAL
            else:
                param_type = Semantic.get_entity_return_type(param_entity, check=False).value
                modifier = find_type_modifier(param_type, arg_type)
                if modifier:
                    code += modifier + '(' + arg_code + ')'
                else:
                    code += arg_code

            if i < len(self.args) - 1:
                code += ', '
        code += ')'
        return code



def get_id_entity(id_, env):
    from src.semantic import Semantic
    global_env = env
    while global_env.parent:
        global_env = global_env.parent
    if isinstance(id_, Id):
        variable_to_check = id_.parent
        variable_entity = env.find(variable_to_check.name)
        while(isinstance(id_, Id)):
            variable_class = Semantic.get_var_class_name(variable_entity, variable_to_check)
            variable_to_check = id_ = id_.child
            if isinstance(id_, Id):
                variable_to_check = id_.parent

            class_ = global_env.find_local(variable_class)
            class_env = class_.struct.env    
            variable_entity = class_env.find_local(variable_to_check.name)
        return variable_entity
    else:
        variable_entity = env.find(id_.name)
        return variable_entity


def get_id_return_type(id_, env):
    entity = get_id_entity(id_, env)
    return entity.struct.type_