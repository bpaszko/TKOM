if __name__ == '__main__':
    from my_ast import *
    from lexer import *
elif __package__:
    from .my_ast import *
    from .lexer import *


comp_operators = ['!=', '==', '>', '<', '>=', '<=']

type_specifiers = ['bool', 'char', 'int', 'long', 'float', 'double', 'void']

access_specifiers = ['public', 'private', 'protected']

literals_types = [TokenType.Character, TokenType.IntNum, TokenType.FloatNum]

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token(type=TokenType.EOF, value='EOF'))
        self.pos = 0
        self.current_token = tokens[self.pos]

    def get_next_token(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            return Token(TokenType.EOF, None)
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            # self.error()
            raise Exception("Invalid syntax")

    def get_previous_token(self):
        self.pos -= 1
        self.current_token = self.tokens[self.pos]

    def peek_token(self, offset=1):
        return self.tokens[self.pos + offset]


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

    def parseIdSequence(self): #HARD SELECTION?
        parent = Identifier(self.current_token.value)
        self.eat(TokenType.Identifier)
        self.eat(TokenType.Dot)
        child = self.parseId()
        return Id(parent=parent, child=child)

    def parseIdentifier(self):
        token = self.current_token
        self.eat(TokenType.Identifier)
        return Identifier(token.value)

    def parseId(self):
        token = self.current_token
        if self.current_token.type == TokenType.Identifier:
            if self.peek_token().type == TokenType.Dot:
                return self.parseIdSequence()
            self.eat(TokenType.Identifier)
            return Identifier(token.value)



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
            return self.parseId()
        token = self.current_token
        if token.type == TokenType.OpenParanthesis:
            self.eat(TokenType.OpenParanthesis)
            node = self.parseAExp()
            self.eat(TokenType.CloseParanthesis)
            return node
        raise Exception("Can't parse Aexp")

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
            return self.parseId()
        if self.current_token.type in literals_types:
            return self.parseLiteral()
        raise Exception("Cant parse operand bexp")

    def parseComparisionOperator(self):
        token = self.current_token
        if token.value in comp_operators:
            self.eat(token.type)
            return token
        raise Exception("Expected comp operator bexp")

    def bexp(self):
        return self.parseBExp()




    # STATEMENTS
    def parseStmt(self):
        if self.current_token.type == TokenType.LBracket:
            return self.parseCompoundStmt()
        if self.current_token.type in [TokenType.Return, TokenType.Continue, TokenType.Break]:
            return self.parseJumpStmt()
        if self.current_token.type == TokenType.While:
            return self.parseWhileLoop()
        if self.current_token.type == TokenType.For:
            return self.parseForLoop()
        if self.current_token.type == TokenType.If:
            return self.parseSelectionStmt()
        if self.current_token.value in type_specifiers or self.current_token.type == \
          self.peek_token().type == TokenType.Identifier:
            return self.parseDeclStmt()
        try:
            return self.parseExpStmt()
        except:
            raise Exception("Can't parse statement")

    def parseCompoundStmt(self):
        nodes = []
        self.eat(TokenType.LBracket)
        while(self.current_token.type != TokenType.RBracket):
            nodes.append(self.parseStmt())
        self.eat(TokenType.RBracket)
        return CompoundStmt(nodes)

    def parseExpStmt(self):
        node = self.parseExp()
        self.eat(TokenType.SemiColon)
        return node 

    def parseDeclStmt(self):
        node = self.parseDecl()
        self.eat(TokenType.SemiColon)
        return node 

    def parseWhileLoop(self):
        self.eat(TokenType.While)
        self.eat(TokenType.OpenParanthesis)
        boolexp = self.parseBExp()
        self.eat(TokenType.CloseParanthesis)
        return WhileStmt(condition=boolexp, body=self.parseStmt())

    #FOR LOOP
    #RETURN DECL
    def parseForInit(self):
        node = self.parseParameter()
        init = self.parseInitialization()
        return Decl(node, init)

    #return relopbexp
    def parseConditionLessThan(self):
        left = self.parseId() #IDENTIFIER
        self.eat(TokenType.LessThan)
        if self.current_token.type == TokenType.Identifier:
            return RelopBexp(left=left, op='<', right=self.parseIdentifier())
        return RelopBexp(left=left, op='<', right=self.parseLiteral())

    #return Assign(id = Binopaexp(id + int)))
    def parseIncrement(self):
        left = self.parseIdentifier()
        self.eat(TokenType.Assign)
        first = self.parseIdentifier()
        self.eat(TokenType.Plus)
        second = self.parseLiteral()
        return AssignExp(name=left, value=BinopAexp(left=first, op='+', right=second))

    def parseForLoop(self):
        self.eat(TokenType.For)
        self.eat(TokenType.OpenParanthesis)
        init = self.parseForInit()
        self.eat(TokenType.SemiColon)
        cond = self.parseConditionLessThan()
        self.eat(TokenType.SemiColon)
        inc = self.parseIncrement()
        self.eat(TokenType.CloseParanthesis)
        return ForStmt(init=init, condition=cond, increment=inc, body=self.parseStmt())

    def parseSelectionStmt(self):
        self.eat(TokenType.If)
        self.eat(TokenType.OpenParanthesis)
        bexp = self.parseBExp()
        self.eat(TokenType.CloseParanthesis)
        true_stmt = self.parseStmt()
        if self.current_token.type == TokenType.Else:
            self.eat(TokenType.Else)
            return IfStmt(condition=bexp, true_stmt=true_stmt, false_stmt=self.parseStmt())
        return IfStmt(condition=bexp, true_stmt=true_stmt, false_stmt=None)

    def parseJumpStmt(self):
        if self.current_token.type == TokenType.Break:
            self.eat(TokenType.Break)
            self.eat(TokenType.SemiColon)
            return JumpStmt('break') 
        elif self.current_token.type == TokenType.Continue:
            self.eat(TokenType.Continue)
            self.eat(TokenType.SemiColon)
            return JumpStmt('continue') 
        elif self.current_token.type == TokenType.Return:
            self.eat(TokenType.Return)
            ret = None
            if self.current_token.type != TokenType.SemiColon:
                ret = self.parseReturnable()
            self.eat(TokenType.SemiColon)
            return JumpStmt('return', ret) 


    def parseReturnable(self):
        if self.current_token.type == TokenType.Identifier:
            return self.parseId()
        if self.current_token.type in literals_types:
            return self.parseLiteral()
        raise Exception("Expected returnable") 




    # EXPRESSIONS  - USED ONLY IN EXPSTMTS
    def parseExp(self):
        if self.checkIfFunCall():
            return self.parseFunctionCall()
        if self.checkIfAssignmentExp():
            return self.parseAssignment()
        if self.checkIfAExp():
            return self.parseAExp()
        if self.checkIfBExp():
            return self.parseBExp()
        raise Exception("Expected expression")

    def checkIfNextTokensCorrect(self, begin, allowed, ending):
        if self.current_token.type not in begin:
            return False
        i = 1
        next_token = self.peek_token(i)
        while next_token.type not in ending:
            if next_token.type not in allowed:
                return False
            i += 1
            next_token = self.peek_token(i)
        return True

    def checkIfFunCall(self):
        begin = [TokenType.Identifier]
        allowed = [TokenType.Identifier, TokenType.Dot]
        ending = [TokenType.OpenParanthesis]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def checkIfAssignmentExp(self):
        begin = [TokenType.Identifier]
        allowed = [TokenType.Identifier, TokenType.Dot]
        ending = [TokenType.Assign]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def checkIfAExp(self):
        begin = [TokenType.Identifier, TokenType.OpenParanthesis, TokenType.CloseParanthesis,
            TokenType.Plus, TokenType.Minus, TokenType.Slash, TokenType.Asterix]
        begin += literals_types
        allowed = list(begin)
        allowed.append(TokenType.Dot)
        ending = [TokenType.SemiColon]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def checkIfBExp(self):
        begin = [TokenType.Identifier, TokenType.OpenParanthesis, TokenType.CloseParanthesis,
            TokenType.And, TokenType.Not, TokenType.Or, TokenType.False_, TokenType.True_]
        begin += literals_types
        allowed = list(begin)
        allowed.append(TokenType.Dot)
        ending = [TokenType.SemiColon]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def checkIfId(self):
        begin = [TokenType.Identifier]
        allowed = [TokenType.Identifier, TokenType.Dot]
        ending = [TokenType.SemiColon]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def checkIfLiteral(self):
        begin = literals_types
        allowed = []
        ending = [TokenType.SemiColon]
        return self.checkIfNextTokensCorrect(begin, allowed, ending)

    def parseAssignment(self):
        id = self.parseId()
        if self.current_token.type == TokenType.Assign:
            init = self.parseInitialization()
            return AssignExp(id, init)
        raise Exception()

    def parseInitialization(self):
        self.eat(TokenType.Assign)
        return self.parseRValue()

    def parseRValue(self):
        if self.checkIfFunCall():
            return self.parseFunctionCall()
        if self.checkIfId():
            return self.parseId()
        if self.checkIfLiteral():
            return self.parseLiteral()
        if self.checkIfAExp():
            return self.parseAExp()
        if self.checkIfBExp():
            return self.parseBExp()

        raise Exception('Expected r-value')

    def parseDecl(self):
        node = self.parseParameter()
        init = None
        if self.current_token.type == TokenType.Assign:
            init = self.parseInitialization()
        return Decl(node, init)

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
        raise Exception("Expected type spec")


    def parseArgList(self):
        args = []
        while self.current_token.type != TokenType.CloseParanthesis:
            if self.current_token.type == TokenType.Identifier:
                args.append(self.parseId())
            elif self.current_token.type in literals_types:
                args.append(self.parseLiteral())
            if self.current_token.type == TokenType.CloseParanthesis:
                break
            self.eat(TokenType.Comma)
        return args

    def parseFunctionCall(self):    #TODO
        name = self.parseId()
        self.eat(TokenType.OpenParanthesis)
        args = self.parseArgList()
        self.eat(TokenType.CloseParanthesis)
        return FunCall(name, args)


    def stmt_parse(self):
        return self.parseStmt()





    def parseParameterList(self):
        parameters = []
        while self.current_token.type != TokenType.CloseParanthesis:
            if self.current_token.value not in type_specifiers:
                raise Exception("Expected parameter in function def")
            param = self.parseParameter()
            parameters.append(param)
            if self.current_token.type == TokenType.CloseParanthesis:
                break
            self.eat(TokenType.Comma)
        return parameters


    def parseFunctionDefinition(self):
        if self.peek_token(2).type != TokenType.OpenParanthesis:
            return
        type = self.parseTypeSpecifier()
        name = self.parseIdentifier()
        self.eat(TokenType.OpenParanthesis)
        params = self.parseParameterList()
        self.eat(TokenType.CloseParanthesis)
        return FunDef(type, name, params, body=self.parseCompoundStmt())



    def parseMemberDeclaration(self):   #TODO
        node = self.parseFunctionDefinition()
        if not node: 
            node = self.parseDeclStmt()
        return node

    def parseMembersDeclarations(self):
        access_members = []
        while self.current_token.value not in access_specifiers and \
          self.current_token.type != TokenType.RBracket:
            member_declaration = self.parseMemberDeclaration()
            access_members.append(member_declaration)
        return access_members

    def parseAccessMembers(self):
        access_type = self.current_token.value
        self.eat(self.current_token.type) #PROTECTED, PRIVATE, PUBLIC
        self.eat(TokenType.Colon)
        access_members = self.parseMembersDeclarations()
        return AccessMembers(access_type, access_members)

    def parseMemberSpecification(self):
        members = []
        while self.current_token.type != TokenType.RBracket:
            if self.current_token.value in access_specifiers:
                part_members = self.parseAccessMembers()
                members.append(part_members)
            else:
                members_decl = self.parseMembersDeclarations()
                members.append(AccessMembers('private', members_decl))
        return members

    def parseClassSpecifier(self):
        self.eat(TokenType.Class)
        if self.current_token.type != TokenType.Identifier:
            raise Exception("Expected class name")
        name = self.parseId() #IDENTIFIER
        self.eat(TokenType.LBracket)
        member_spec = self.parseMemberSpecification()
        self.eat(TokenType.RBracket)
        self.eat(TokenType.SemiColon)
        return Class(name, member_spec)



    def parseDefinition(self):
        if self.current_token.type == TokenType.Class:
            node = self.parseClassSpecifier()
            return node
        if self.current_token.value not in type_specifiers:
            raise Exception('Expected class or type specifier') 
        node = self.parseFunctionDefinition()
        if node:
            return node
        node = self.parseDeclStmt()
        if node:
            return node

    def parseProgram(self):
        nodes = []
        while(self.current_token.type != TokenType.EOF):
            node = self.parseDefinition()
            if node:
                nodes.append(node)
                continue
            else:
                raise Exception("Can't parse program") #TO REMOVE!!
        return Program(nodes)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s filename parsername' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    lexer = Lexer()
    tokens = lexer.cpp_lex(characters)
    parser = Parser(tokens)
    result = parser.parseProgram()
    print(result)
