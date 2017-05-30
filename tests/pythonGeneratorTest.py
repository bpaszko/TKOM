import unittest

if __name__ == '__main__':
    import sys
    import io
    from os import path
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    from src.my_ast import *
    from src.pythonGenerator import *
    from src.my_env import *



class pygenTest(unittest.TestCase):
    def setUp(self):
        self.pygen = PythonGenerator()

    def test_create_class(self):
        ast = Identifier('MyClass')
        self.pygen.create_class(ast)
        expected = 'class MyClass:\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_function(self):
        id_ = Identifier('my_fun')
        params = [Identifier('x'), Identifier('y')]
        global_env = Env(env_type=None)
        local_env = Env(parent=global_env, env_type=EnvType.Fun)
        self.pygen.create_function(id_, params, local_env)
        expected = 'def my_fun(x, y):\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_method(self):
        id_ = Identifier('my_fun')
        params = [Identifier('x'), Identifier('y')]
        global_env = Env(env_type=EnvType.Class)
        local_env = Env(parent=global_env, env_type=EnvType.Fun)
        self.pygen.create_function(id_, params, local_env)
        expected = 'def my_fun(self, x, y):\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_while_loop(self):
        bexp = RelopBexp(left=Identifier('x'), op='<', right=IntNum(2))
        self.pygen.create_while_loop(bexp, None)
        expected = 'while x < 2:\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_for_loop(self):
        init = Decl(Param(TypeSpec('int'), Identifier('i')), IntNum(0))
        cond = RelopBexp(left=Identifier('i'), op='<', right=IntNum(2))
        increment = AssignExp(Identifier('i'), BinopAexp(Identifier('i'), '+', IntNum(1)))
        self.pygen.create_for_loop(init, cond, increment, None)
        expected = 'for i in range(0,2,1):\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_if_stmt(self):
        cond = RelopBexp(left=Identifier('x'), op='<', right=IntNum(2))
        self.pygen.create_if_stmt(cond, None)
        expected = 'if x < 2:\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_else_stmt(self):
        self.pygen.create_else_stmt()
        expected = 'else:\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_break(self):
        ast = JumpStmt('break')
        self.pygen.create_jump_stmt(ast, None)
        expected = 'break\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_continue(self):
        ast = JumpStmt('continue')
        self.pygen.create_jump_stmt(ast, None)
        expected = 'continue\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_return_void(self):
        ast = JumpStmt('return')
        self.pygen.create_jump_stmt(ast, None)
        expected = 'return\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_return_var(self):
        ast = JumpStmt('return', Identifier('x'))
        self.pygen.create_jump_stmt(ast, None)
        expected = 'return x\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_pass(self):
        self.pygen.create_pass()
        expected = 'pass\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_identifier(self):
        ast = Identifier('var')
        self.pygen.create_id(ast)
        expected = 'var\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_id(self):
        ast = Id(Identifier('x'), Id(Identifier('y'), Identifier('var')))
        self.pygen.create_id(ast)
        expected = 'x.y.var\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_literal(self):
        ast = IntNum(2)
        self.pygen.create_literal(ast)
        expected = '2\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_float(self):
        ast = FloatNum(2.45)
        self.pygen.create_literal(ast)
        expected = '2.45\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_char(self):
        ast = Character("'a'")
        self.pygen.create_literal(ast)
        expected = 'ord(\'a\')\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_bool_lit(self):
        ast = BoolLit('true')
        self.pygen.create_literal(ast)
        expected = 'True\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_funcall(self): 
        env_glob = Env()
        env_fun = Env(env_glob)
        entity_var_param1 = VariableStruct(Identifier('X'), 'public')
        entity_var_param2 = VariableStruct(TypeSpec('int'), 'public')
        entity_var_param3 = VariableStruct(TypeSpec('int'), 'public')
        entity_var_param4 = VariableStruct(TypeSpec('char'), 'public')
        entity_param1 = Entity(EntityType.Var, entity_var_param1)
        entity_param2 = Entity(EntityType.Var, entity_var_param2)
        entity_param3 = Entity(EntityType.Var, entity_var_param3)
        entity_param4 = Entity(EntityType.Var, entity_var_param4)
        env_fun.dict['p1'] = entity_param1
        env_fun.dict['p2'] = entity_param2
        env_fun.dict['p3'] = entity_param3
        env_fun.dict['p4'] = entity_param4
        env_glob.childs.append(env_fun)
        params = [Param(Identifier('X'), Identifier('p1')), Param(TypeSpec('int'), Identifier('p2')), 
            Param(TypeSpec('int'), Identifier('p3')), Param(TypeSpec('char'), Identifier('p4'))]
        fundef = FunDef(TypeSpec('void'), Identifier('fun'), params, [])
        fun_struct = FunctionStruct(TypeSpec('void'), env_fun, 'public')
        entity_fun = Entity(EntityType.Fun, fun_struct)
        env_glob.dict['fun'] = entity_fun
        ast = FunCall(Identifier('fun'), [Identifier('obj'), Identifier('x'), IntNum('2'), Character("'a'")])
        entity_var = VariableStruct(Identifier('X'), 'public')
        entity = Entity(EntityType.Var, entity_var)
        entity_var_2 = VariableStruct(TypeSpec('int'), 'public')
        entity_2 = Entity(EntityType.Var, entity_var_2)
        env = Env(env_fun)
        env_fun.childs.append(env)
        env.dict['obj'] = entity
        env.dict['x'] = entity_2
        self.pygen.create_funcall(ast, env)
        expected = 'fun(deepcopy(obj), x, 2, ord(\'a\'))\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_simple_aexp(self):
        ast = BinopAexp(Identifier('x'), '+', IntNum(2))
        self.pygen.create_aexp(ast, None)
        expected = 'x + 2\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_complex_aexp(self):
        #a * (2 / (2-1))
        ast1 = BinopAexp(IntNum(2), '-', IntNum(1))
        ast1.add_paranthesis()
        ast2 = BinopAexp(IntNum(2), '/', ast1)
        ast2.add_paranthesis()
        ast = BinopAexp(Identifier('a'), '*', ast2)
        self.pygen.create_aexp(ast, None)
        expected = 'a * int(2 / (2 - 1))\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_bexp_condition(self):
        ast = RelopBexp(Identifier('x'), '<', IntNum(2))
        self.pygen.create_bexp(ast, None)
        expected = 'x < 2\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_simple_bexp(self):
        ast = AndBexp(Identifier('x'), IntNum(2))
        self.pygen.create_bexp(ast, None)
        expected = 'x and 2\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_complex_bexp(self):
        ast1 = RelopBexp(Identifier('k'), '<', IntNum(2))
        ast1.add_paranthesis()
        ast2 = RelopBexp(Identifier('l'), '>', Identifier('k'))
        ast2.add_paranthesis()
        ast2 = NotBexp(ast2)
        ast3 = AndBexp(ast1, ast2)
        ast3.add_paranthesis()
        ast = AndBexp(BoolLit('false'), ast3)
        self.pygen.create_bexp(ast, None)
        expected = 'False and ((k < 2) and not (l > k))\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_declaration(self):
        ast = Decl(Param(TypeSpec('int'), Identifier('i')), IntNum(2))
        self.pygen.create_declaration(ast, None)
        expected = 'i = 2\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_declaration_without_assignment(self):
        ast = Decl(Param(TypeSpec('int'), Identifier('i')), None)
        self.pygen.create_declaration(ast, None)
        expected = 'i = 0\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_assignment(self):
        ast = AssignExp(Identifier('x'), Identifier('y'))
        entity_var = VariableStruct(TypeSpec('int'), 'public')
        entity = Entity(EntityType.Var, entity_var)
        entity_var_2 = VariableStruct(TypeSpec('int'), 'public')
        entity_2 = Entity(EntityType.Var, entity_var_2)
        env = Env()
        env.dict['x'] = entity
        env.dict['y'] = entity_2
        self.pygen.create_assignment(ast, env)
        expected = 'x = y\n'
        self.assertEqual(self.pygen.code, expected)

    def test_create_main_call(self):
        self.pygen.create_main_call()
        expected = 'print(main())'
        self.assertEqual(self.pygen.code, expected)

    def test_create_copy_import(self):
        self.pygen.create_copy_import()
        expected = 'from copy import deepcopy\n\n'
        self.assertEqual(self.pygen.code, expected)


if __name__ == '__main__':
    unittest.main()