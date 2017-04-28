if __name__ == '__main__':
    from my_ast import *
    from lexer import *
elif __package__:
    from .my_ast import *
    from .lexer import *


comp_operators = ['!=', '==', '>', '<', '>=', '<=']

type_specifiers = ['bool', 'char', 'int', 'long,' 'float', 'double', 'void']

access_specifiers = ['public', 'private', 'protected']


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

    def parseNumber(self):
        token = self.current_token
        if self.current_token.type == TokenType.IntNum:
            self.eat(TokenType.IntNum)
            return IntNum(token.value)
        elif self.current_token.type == TokenType.FloatNum:
            self.eat(TokenType.FloatNum)
            return Floatnum(token.value)

    def parseId(self):
        token = self.current_token
        if self.current_token.type == TokenType.Identifier:
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
        node = self.parseNumber()
        if node:
            return node
        node = self.parseId()
        if node:
            return node
        token = self.current_token
        if token.type == TokenType.OpenParanthesis:
            self.eat(TokenType.OpenParanthesis)
            node = self.parseAExp()
            if not node:
                self.get_previous_token()
                return None
            self.eat(TokenType.CloseParanthesis)
            return node

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
        if node and operator:
            return RelopBexp(left=node, op=operator.value, right=self.parseOperand())

    def parseOperand(self):
        node = self.parseNumber()
        if node:
            return node
        node = self.parseId()
        if node:
            return node

    def parseComparisionOperator(self):
        token = self.current_token
        if token.value in comp_operators:
            self.eat(token.type)
            return token

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
            self.parseForLoop()
        node = self.parseExpStmt()
        if node:
            return node
        node = self.parseDeclStmt()
        if node:
            return node
        node = self.parseSelectionStmt()
        if node:
            return node

    def parseCompoundStmt(self):
        nodes = []
        self.eat(TokenType.LBracket)
        while(self.current_token.type != TokenType.RBracket):
            nodes.append(self.parseStmt())
        self.eat(TokenType.RBracket)
        return CompoundStmt(nodes)

    def parseExpStmt(self):
        node = self.parseExp()
        if node:
            self.eat(TokenType.SemiColon)
            return node  # PARAMETRY

    def parseDeclStmt(self):
        node = self.parseDecl()
        if node:
            self.eat(TokenType.SemiColon)
            return node  # PARAMETRY

    def parseWhileLoop(self):
        if self.current_token.type == TokenType.While:
            self.eat(TokenType.While)
            self.eat(TokenType.OpenParanthesis)
            boolexp = self.parseBExp()
            self.eat(TokenType.CloseParanthesis)
            return WhileStmt(condition=boolexp, body=self.parseStmt())

    # FOR LOOP
    def parseForLoop(self):
        return None

    def parseSelectionStmt(self):
        if self.current_token.type == TokenType.If:
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
            return JumpStmt()  # PARAMS
        elif self.current_token.type == TokenType.Continue:
            self.eat(TokenType.Continue)
            self.eat(TokenType.SemiColon)
            return JumpStmt()  # PARAMS
        elif self.current_token.type == TokenType.Return:
            self.eat(TokenType.Return)
            if self.current_token.type != TokenType.SemiColon:
                self.parseReturnable()  # IMPLEMENT
            self.eat(TokenType.SemiColon)
            return JumpStmt()  # PARAMS


    def parseReturnable():
        # MORE RETURNABLES!!!
        if self.current_token.type not in [TokenType.Identifier, TokenType.Int]:
            raise Exception("EXPECTED RETURNABLE")
        if self.current_token.type == TokenType.Identifier:
            return self.parseId()
        else:
            return self.parseNumber() #CHANGE PARSE LITERAL


    # EXPRESSIONS
    def parseExp(self):
        node = self.parseAssignment()
        if node:
            return node
        node = self.parseAExp()
        if node:
            return node
        node = self.parseBExp()
        if node:
            return node
        node = self.parseFunctionCall()
        if node:
            return node

    def parseAssignment(self):
        if self.peek_token().type != TokenType.Assign:
            return
        id = self.parseId()
        init = self.parseInitialization()
        if id and init:
            return AssignExp(id, init)

    def parseInitialization(self):
        if self.current_token.type == TokenType.Assign:
            self.eat(TokenType.Assign)
            return self.parseRValue()

    def parseRValue(self):
        node = self.parseAExp()
        if node:
            return node
        node = self.parseBExp()
        if node:
            return node
        node = self.parseFunctionCall()
        if node:
            return node
        node = self.parseId()
        if node:
            return node
        node = self.parseNumber()
        if node:
            return node

    def parseDecl(self):
        node = self.parseParameter()
        if node:
            init = self.parseInitialization()
            return Decl(node, init)

    def parseParameter(self):
        node = self.parseTypeSpecifier()
        if node:
            return Param(type=node, name=self.parseId())

    def parseTypeSpecifier(self):
        if self.current_token.value in type_specifiers:
            token = self.current_token
            self.eat(token.type)
            return TypeSpec(token.value)

    def parseFunctionCall(self):
        return None

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
        name = self.parseId()
        self.eat(TokenType.OpenParanthesis)
        params = self.parseParameterList()
        self.eat(TokenType.CloseParanthesis)
        return FunDef(type, name, params, body=self.parseCompoundStmt())



    def parseMemberDeclaration(self):
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
            node = parseClassSpecifier()
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
    tokens = lexer.imp_lex(characters)
    parser = Parser(tokens)
    result = parser.parseClassSpecifier()
    print(result)
