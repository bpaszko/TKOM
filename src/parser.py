if __name__ == '__main__':
    from my_ast import *
    from lexer import *
    from semantic import *
    from pythonGenerator import *
elif __package__:
    from .my_ast import *
    from .lexer import *
    from .semantic import *
    from .pythonGenerator import *


comp_operators = ['!=', '==', '>', '<', '>=', '<=']

type_specifiers = ['bool', 'char', 'int', 'long', 'float', 'double', 'void']

access_specifiers = ['public', 'private', 'protected']

literals_types = [TokenType.Character, TokenType.IntNum, TokenType.FloatNum]

class SyntaxError(Exception):
    pass

class InvalidSyntaxError(SyntaxError):
    pass

class ParseSemanticError(SemanticError):
    def __init__(self, line, prev_exception):
        self.line = line
        self.prev_exception = prev_exception

    def __str__(self):
        return 'On line: %d, %s' % (self.line, self.prev_exception)

class Parser():
    def __init__(self, stream, semantic=False, pygen=False):
        self.lexer = Lexer(stream)
        self.current_token = self.lexer.get_next_token()
        self.semantic = Semantic(check=semantic)
        self.pygen = PythonGenerator('other/python_code.py', check=pygen)
        

    def get_next_token(self):
        return self.lexer.get_next_token()

    def get_env(self):
        return self.semantic.current_env

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            raise InvalidSyntaxError("Expected %s, got %s, line: %s" 
                % (token_type.name, self.current_token.value, self.current_token.line))

    def revert(self, pos):
        self.lexer.revert(pos)
        self.current_token = self.lexer.current_tokens[pos-1]


    def parseLiteral(self):
        token = self.current_token
        if self.current_token.type == TokenType.Character:
            self.eat(TokenType.Character)
            return Character(token.value)
        if self.current_token.type == TokenType.IntNum:
            self.eat(TokenType.IntNum)
            return IntNum(token.value)
        if self.current_token.type == TokenType.FloatNum:
            self.eat(TokenType.FloatNum)
            return FloatNum(token.value)
        raise InvalidSyntaxError("Expected literal, got %s, line: %s" 
                % (self.current_token.value, self.current_token.line))


    def parseIdentifier(self):
        token = self.current_token
        self.eat(TokenType.Identifier)
        return Identifier(token.value)

    def parseId(self):
        token = self.current_token
        ident = self.parseIdentifier()
        if self.current_token.type == TokenType.Dot:
            self.eat(TokenType.Dot)
            return Id(parent=ident, child=self.parseId())
        return ident


    # arithmetic-expression
    def parseAExp(self):
        node = self.parseATerm()
        while self.current_token.type in (TokenType.Plus, TokenType.Minus):
            token = self.current_token
            if token.type == TokenType.Plus:
                self.eat(TokenType.Plus)
            elif token.type == TokenType.Minus:
                self.eat(TokenType.Minus)

            node = BinopAexp(left=node, op=token.value,
                             right=self.parseATerm())
        return node

    def parseATerm(self):
        node = self.parseAFactor()
        while self.current_token.type in (TokenType.Asterix, TokenType.Slash):
            token = self.current_token
            if token.type == TokenType.Asterix:
                self.eat(TokenType.Asterix)
            elif token.type == TokenType.Slash:
                self.eat(TokenType.Slash)

            node = BinopAexp(left=node, op=token.value,
                             right=self.parseAFactor())
        return node

    def parseAFactor(self):
        if self.current_token.type in literals_types:
            return self.parseLiteral()
        if self.current_token.type == TokenType.Identifier:
            id_ = self.parseId()
            self.semantic.check_if_id_is_simple_type_variable(id_)
            return id_
        token = self.current_token
        if token.type == TokenType.OpenParanthesis:
            self.eat(TokenType.OpenParanthesis)
            node = self.parseAExp()
            self.eat(TokenType.CloseParanthesis)
            node.add_paranthesis()
            return node
        raise InvalidSyntaxError("Can't parse Aexp")

    def aexp(self):
        return self.parseAExp()



    # BOOLEAN EXPRESSION
    def parseBExp(self):
        node = self.parseBTerm()
        while self.current_token.type == TokenType.Or:
            self.eat(TokenType.Or)
            node = OrBexp(left=node, right=self.parseBTerm())
        return node

    def parseBTerm(self):
        node = self.parseBFactor()
        while self.current_token.type == TokenType.And:
            self.eat(TokenType.And)
            node = AndBexp(left=node, right=self.parseBFactor())
        return node

    def parseBFactor(self):
        token = self.current_token
        if token.type == TokenType.Not:
            self.eat(TokenType.Not)
            return NotBexp(exp=self.parseBFactor())

        elif token.type == TokenType.OpenParanthesis:
            self.eat(TokenType.OpenParanthesis)
            node = self.parseBExp()
            self.eat(TokenType.CloseParanthesis)
            node.add_paranthesis()
            return node

        elif token.type in (TokenType.False_, TokenType.True_):
            if token.type == TokenType.False_:
                self.eat(TokenType.False_)
            else:
                self.eat(TokenType.True_)
            return BoolLit(token.value)

        else:
            return self.parseCondition()

    def parseCondition(self):
        node = self.parseOperand()
        operator = self.parseComparisionOperator()
        return RelopBexp(left=node, op=operator.value, right=self.parseOperand())

    def parseOperand(self):
        if self.current_token.type == TokenType.Identifier:
            id_ = self.parseId()
            self.semantic.check_if_id_is_simple_type_variable(id_)
            return id_
        if self.current_token.type in literals_types:
            return self.parseLiteral()
        raise InvalidSyntaxError("Cant parse operand bexp")

    def parseComparisionOperator(self):
        token = self.current_token
        if token.value in comp_operators:
            self.eat(token.type)
            return token
        raise InvalidSyntaxError("Expected comp operator bexp")

    def bexp(self):
        return self.parseBExp()


    # STATEMENTS
    def parseStmt(self):
        if self.current_token.type == TokenType.LBracket:
            return self.parseCompoundStmt()
        return self.parseNonCompoundStmt()


    def parseNonCompoundStmt(self):
        if self.current_token.type in [TokenType.Return, TokenType.Continue, TokenType.Break]:
            return self.parseJumpStmt()
        if self.current_token.type == TokenType.While:
            return self.parseWhileLoop()
        if self.current_token.type == TokenType.For:
            return self.parseForLoop()
        if self.current_token.type == TokenType.If:
            return self.parseSelectionStmt()

        node = self.try_to_parse_decl()
        if node:
            self.pygen.create_declaration(node, self.get_env())
            return node

        return self.parseExpStmt()


    def try_to_parse_decl(self):
        if self.current_token.value in type_specifiers:
            param = self.parseParameter()
            decl = self.parseDeclStmt(param)
            self.semantic.add_declaration(decl)
            return decl
        elif self.current_token.type == TokenType.Identifier:
            try:
                pos = self.lexer.pos
                param = self.parseParameter()
            except InvalidSyntaxError:
                self.revert(pos)
            else:
                decl = self.parseDeclStmt(param)
                self.semantic.add_declaration(decl)
                return decl


    def parseCompoundStmt(self):
        self.semantic.set_new_env(env_type=EnvType.Compound)
        nodes = []
        self.eat(TokenType.LBracket)
        while(self.current_token.type != TokenType.RBracket):
            nodes.append(self.parseNonCompoundStmt())
        self.eat(TokenType.RBracket)
        self.semantic.previous_env()
        return CompoundStmt(nodes)


    def parseExpStmt(self):
        node = self.try_to_parse_exp(self.parseFunctionCall)
        if node:
            self.eat(TokenType.SemiColon)
            self.pygen.create_funcall(node, self.get_env())
            return node
        node = self.try_to_parse_exp(self.parseAssignment)
        if node:
            self.eat(TokenType.SemiColon)
            self.pygen.create_assignment(node, self.get_env())
            return node
        node = self.try_to_parse_exp(self.parseAExp)
        if node:
            self.eat(TokenType.SemiColon)
            self.pygen.create_aexp(node, self.get_env())
            return node
        node = self.try_to_parse_exp(self.parseBExp)
        if node:
            self.eat(TokenType.SemiColon)
            self.pygen.create_bexp(node, self.get_env())
            return node

        raise InvalidSyntaxError("Expected expression, got: %s, line: %d" 
                % (self.current_token.value, self.current_token.line))


    def try_to_parse_exp(self, fun):
        try:
            pos = self.lexer.pos
            node = fun()
            if self.current_token.type != TokenType.SemiColon:
                self.revert(pos)
                return None    
        except InvalidSyntaxError:
            self.revert(pos)
            return None
        else:
            return node



    def parseDeclStmt(self, param):
        node = self.parseDecl(param)
        self.eat(TokenType.SemiColon)
        return node 

    def parseWhileLoop(self):
        self.semantic.set_new_env(env_type=EnvType.Loop)
        self.eat(TokenType.While)
        self.eat(TokenType.OpenParanthesis)
        boolexp = self.parseBExp()
        self.eat(TokenType.CloseParanthesis)
        self.pygen.create_while_loop(boolexp, self.get_env())
        body = self.parseStmt()
        if isinstance(body, CompoundStmt) and not body.statements:
            self.pygen.create_pass()
        self.pygen.decrease()
        self.semantic.previous_env()
        return WhileStmt(condition=boolexp, body=body)

    #FOR LOOP
    #RETURN DECL
    def parseForInit(self):
        node = self.parseParameter()
        self.semantic.check_parameter(node)
        init = self.parseInitialization()
        decl = Decl(node, init)
        self.semantic.add_declaration(decl)
        return Decl(node, init)

    #return relopbexp
    def parseConditionLessThan(self, decl):
        left = self.parseIdentifier()  
        self.semantic.check_if_valid_id(left)
        node = None
        self.eat(TokenType.LessThan)
        if self.current_token.type == TokenType.Identifier:
            right=self.parseIdentifier()
            self.semantic.check_if_valid_id(right)
            node = RelopBexp(left=left, op='<', right=right)
        else:
            node = RelopBexp(left=left, op='<', right=self.parseLiteral())
        self.semantic.check_for_condition(node, decl)
        return node

    #return Assign(id = Binopaexp(id + int)))
    def parseIncrement(self, decl):
        left = self.parseIdentifier()
        self.eat(TokenType.Assign)
        first = self.parseIdentifier()
        self.eat(TokenType.Plus)
        second = self.parseLiteral()
        node = AssignExp(name=left, value=BinopAexp(left=first, op='+', right=second))
        self.semantic.check_for_increment(node, decl)
        return node

    def parseForLoop(self): #PYGEN SHOULD HANDLE
        self.semantic.set_new_env(env_type=EnvType.Loop)
        self.eat(TokenType.For)
        self.eat(TokenType.OpenParanthesis)
        init = self.parseForInit()
        self.eat(TokenType.SemiColon)
        cond = self.parseConditionLessThan(init)
        self.eat(TokenType.SemiColon)
        inc = self.parseIncrement(init)
        self.eat(TokenType.CloseParanthesis)
        self.pygen.create_for_loop(init, cond, inc, self.get_env())
        body = self.parseStmt()
        if isinstance(body, CompoundStmt) and not body.statements:
            self.pygen.create_pass()
        self.pygen.decrease()
        self.semantic.previous_env()
        return ForStmt(init=init, condition=cond, increment=inc, body=body)

    def parseSelectionStmt(self): #PYGEN SHOULD HANDLE
        self.semantic.set_new_env(env_type=EnvType.If)
        self.eat(TokenType.If)
        self.eat(TokenType.OpenParanthesis)
        bexp = self.parseBExp()
        self.pygen.create_if_stmt(bexp, self.get_env())
        self.eat(TokenType.CloseParanthesis)
        true_stmt = self.parseStmt()
        if isinstance(true_stmt, CompoundStmt) and not true_stmt.statements:
            self.pygen.create_pass()
        self.pygen.decrease()
        self.semantic.previous_env()
        if self.current_token.type == TokenType.Else:
            self.semantic.set_new_env(env_type=EnvType.Else)
            self.eat(TokenType.Else)
            self.pygen.create_else_stmt()
            false_stmt = self.parseStmt()
            if isinstance(false_stmt, CompoundStmt) and not false_stmt.statements:
                self.pygen.create_pass()
            self.pygen.decrease()
            self.semantic.previous_env()
            return IfStmt(condition=bexp, true_stmt=true_stmt, false_stmt=false_stmt)
        return IfStmt(condition=bexp, true_stmt=true_stmt, false_stmt=None)

    def parseJumpStmt(self): #PYGEN SHOULD HANDLE
        node = None
        if self.current_token.type == TokenType.Break:
            self.eat(TokenType.Break)
            self.eat(TokenType.SemiColon)
            self.semantic.check_if_inside_loop()
            node = JumpStmt('break') 
            self.pygen.create_jump_stmt(node, self.get_env())
        elif self.current_token.type == TokenType.Continue:
            self.eat(TokenType.Continue)
            self.eat(TokenType.SemiColon)
            self.semantic.check_if_inside_loop()
            node = JumpStmt('continue') 
            self.pygen.create_jump_stmt(node, self.get_env())
        elif self.current_token.type == TokenType.Return:
            self.eat(TokenType.Return)
            ret = None
            if self.current_token.type != TokenType.SemiColon:
                ret = self.parseReturnable()
            self.eat(TokenType.SemiColon)
            node = JumpStmt('return', ret)
            self.semantic.check_return(node)
            self.pygen.create_jump_stmt(node, self.get_env())    
        return node 


    def parseReturnable(self):
        if self.current_token.type == TokenType.Identifier:
            return self.parseId()
        if self.current_token.type in literals_types:
            return self.parseLiteral()
        raise InvalidSyntaxError("Expected returnable, got %s, line: %d" 
                % (self.current_token.value, self.current_token.line))

    def parseAssignment(self):
        id = self.parseId()
        init = self.parseInitialization()
        node = AssignExp(id, init)
        self.semantic.check_if_valid_assignment(node)
        return node

    def parseInitialization(self):
        self.eat(TokenType.Assign)
        return self.parseRValue()

    def parseRValue(self): 
        node = self.try_to_parse_exp(self.parseId)
        if node:
            return node
        node = self.try_to_parse_exp(self.parseLiteral)
        if node:
            return node
        node = self.try_to_parse_exp(self.parseFunctionCall)
        if node:
            return node
        node = self.try_to_parse_exp(self.parseAExp)
        if node:
            return node
        node = self.try_to_parse_exp(self.parseBExp)
        if node:
            return node
 
        raise InvalidSyntaxError("Expected r-value, line: %d" 
                % (self.current_token.line))

    def parseDecl(self, param):
        self.semantic.check_parameter(param)
        init = None
        if self.current_token.type == TokenType.Assign:
            init = self.parseInitialization()
        decl = Decl(param,init)
        return decl

    def parseParameter(self):
        node = self.parseTypeSpecifier()
        return Param(type=node, name=self.parseIdentifier())

    def parseTypeSpecifier(self):
        if self.current_token.value in type_specifiers:
            token = self.current_token
            self.eat(token.type)
            return TypeSpec(token.value)
        if self.current_token.type == TokenType.Identifier:
            return self.parseIdentifier()
        raise InvalidSyntaxError("Expected type specifier, got %s, line: %d" 
                % (self.current_token.value, self.current_token.line))


    def parseArgList(self): 
        args = []
        if self.current_token.type != TokenType.CloseParanthesis:
            while True:
                #while self.current_token.type != TokenType.CloseParanthesis:
                if self.current_token.type == TokenType.Identifier:
                    args.append(self.parseId())
                elif self.current_token.type in literals_types:
                    args.append(self.parseLiteral())
                else:
                    raise InvalidSyntaxError("Expected argument, got %s, line: %d" 
                        % (self.current_token.value, self.current_token.line))
                if self.current_token.type == TokenType.CloseParanthesis:
                    break
                self.eat(TokenType.Comma)
        return args

    def parseFunctionCall(self): 
        name = self.parseId()
        self.eat(TokenType.OpenParanthesis)
        args = self.parseArgList()
        self.eat(TokenType.CloseParanthesis)
        node = FunCall(name, args)
        self.semantic.check_if_valid_funcall(node)
        return node




    def parseParameterList(self):
        parameters = []
        if self.current_token.type != TokenType.CloseParanthesis:
            while True:
                #while self.current_token.type != TokenType.CloseParanthesis:
                if self.current_token.value not in type_specifiers and \
                  self.current_token.type != TokenType.Identifier:
                    raise InvalidSyntaxError("Expected parameter, got %s, line: %d" 
                        % (self.current_token.value, self.current_token.line))
                param = self.parseParameter()
                self.semantic.add_parameter(param)
                parameters.append(param)
                if self.current_token.type == TokenType.CloseParanthesis:
                    break
                self.eat(TokenType.Comma)
        return parameters

    def parseFunctionDefinition(self, param, access='public'): 
        self.semantic.set_new_env(env_type=EnvType.Fun)
        type_, name = param.type, param.name
        self.eat(TokenType.OpenParanthesis)
        params = self.parseParameterList()

        self.semantic.add_function_definition(type_, name, access)
        self.pygen.create_function(name, params, self.get_env())

        self.eat(TokenType.CloseParanthesis)
        body=self.parseCompoundStmt()
        node = FunDef(type_, name, params, body)
        
        if not body.statements:
            self.pygen.create_pass()
        self.pygen.decrease()
        self.semantic.previous_env()

        return node

    def parseMemberDeclaration(self, access):
        param = self.parseParameter()
        if self.current_token.type == TokenType.OpenParanthesis:
            return self.parseFunctionDefinition(param, access)

        decl = self.parseDeclStmt(param)
        self.semantic.add_declaration(decl, access)
        self.pygen.create_declaration(decl, self.get_env())
        return decl

    def parseMembersDeclarations(self, access):
        access_members = []
        while self.current_token.value not in access_specifiers and \
          self.current_token.type != TokenType.RBracket:
            member_declaration = self.parseMemberDeclaration(access)
            access_members.append(member_declaration)
        return access_members

    def parseAccessMembers(self):
        access_type = self.current_token.value
        self.eat(self.current_token.type) #PROTECTED, PRIVATE, PUBLIC
        self.eat(TokenType.Colon)
        access_members = self.parseMembersDeclarations(access_type)
        return AccessMembers(access_type, access_members)

    def parseMemberSpecification(self):
        members = []
        while self.current_token.type != TokenType.RBracket:
            if self.current_token.value in access_specifiers:
                part_members = self.parseAccessMembers()
                members.append(part_members)
            else:
                members_decl = self.parseMembersDeclarations('private')
                members.append(AccessMembers('private', members_decl))
        return members

    def parseClassSpecifier(self):
        self.semantic.set_new_env(env_type=EnvType.Class)
        self.eat(TokenType.Class)
        name = self.parseIdentifier()

        self.semantic.add_class(name)
        self.pygen.create_class(name)
        
        self.eat(TokenType.LBracket)
        member_spec = self.parseMemberSpecification()
        self.eat(TokenType.RBracket)
        self.eat(TokenType.SemiColon)
        class_ = Class(name, member_spec)
        if Parser.checkIfEmptyClass(class_):
            self.pygen.create_pass()
        self.pygen.decrease()
        self.semantic.previous_env()
        return class_

    @staticmethod
    def checkIfEmptyClass(class_):
        for member in class_.members:
            if member.members_declarations:
                return False
        return True

    def parseDefinition(self):
        if self.current_token.type == TokenType.Class:
            return self.parseClassSpecifier()
        if self.current_token.value not in type_specifiers and self.current_token.type != TokenType.Identifier:
            raise InvalidSyntaxError("Expected class or type spec, got %s, line: %d" 
                % (self.current_token.value, self.current_token.line))

        param = self.parseParameter()
        if self.current_token.type == TokenType.OpenParanthesis:
            return self.parseFunctionDefinition(param)

        decl = self.parseDeclStmt(param)
        self.semantic.add_declaration(decl)
        self.pygen.create_declaration(decl, self.get_env())
        return decl

    def parseProgram(self):
        nodes = []
        self.pygen.create_copy_import()
        while(self.current_token.type != TokenType.EOF):
            node = self.parseDefinition()
            nodes.append(node)
        self.pygen.create_main_call()
        return Program(nodes)



def print_env(env, tb=0):
    print(tb*'\t' + str(env))
    if env.childs:
        for i in env.childs:
            print_env(i, tb+1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s filename parsername' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    stream = None
    with open(filename, 'r') as f:
        parser = Parser(f, semantic=True, pygen=False)
        try:
            result = parser.parseProgram()
        except (SyntaxError, SemanticError) as e:
            print(e.__class__.__name__)
            print(e)
        else:
            print(result)

    #result = parser.parseProgram()

    #print('\n\n')
    #print_env(parser.semantic.global_env)