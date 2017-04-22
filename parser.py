from my_ast import *
from lexer import *

comp_operators = ['!=', '==', '>', '<', '>=', '<=', '=']

type_specifiers = ['bool', 'char', 'in', 'long,' 'float', 'double', 'void']

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
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
            #self.error()
            raise Exception("Invalid syntax")



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

            node = BinopAexp(left=node, op=token.value, right=self.parseATerm())
        return node


    def parseATerm(self):
        node = self.parseAFactor()

        while self.current_token.type in (TokenType.Asterix, TokenType.Slash):
            token = self.current_token
            if token.type == TokenType.Asterix:
                self.eat(TokenType.Asterix)
            elif token.type == TokenType.Slash:
                self.eat(TokenType.Slash)

            node = BinopAexp(left=node, op=token.value, right=self.parseAFactor())
        return node


    def parseAFactor(self):
        node = self.parseNumber()
        if node:
            return node
        token = self.current_token
        if token.type == TokenType.OpenParanthesis:
            self.eat(TokenType.OpenParanthesis)
            node = self.parseAExp()
            self.eat(TokenType.CloseParanthesis)
            return node


    def aexp(self):
        return self.parseAExp()



    #BOOLEAN EXPRESSION
    def parseBExp(self):
        node = self.parseBTerm()
        while self.current_token.type == TokenType.Or:
            token = self.current_token
            self.eat(TokenType.Or)
            node = OrBexp(left=node, right=self.parseBTerm())
        return node


    def parseBTerm(self):
        node = self.parseBFactor()
        while self.current_token.type == TokenType.And:
            token = self.current_token
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
            return BoolLit(token)

        else:
            return self.parseCondition()


    def parseCondition(self):
        node = self.parseOperand()
        operator=self.parseComparisionOperator()
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




    #STATEMENTS

    def parseStmt(self):
        node = self.parseExpStmt()
        if node: 
            return node
        node = self.parseDeclStmt()
        if node: 
            return node
        node = self.parseForLoop()
        if node: 
            return node
        node = self.parseWhileLoop()
        if node: 
            return node
        node = self.parseSelectionStmt()
        if node: 
            return node
        node = self.parseJumpStmt()
        if node: 
            return node


    def parseCompoundStmt(self):
        token = self.current_token
        if token.type == TokenType.LeftBracket:
            nodes = []
            self.eat(TokenType.LeftBracket)
            while(self.current_token.type != TokenType.RightBracket):
                nodes.append(self.parseStmt())
            self.eat(TokenType.RightBracket)
            return CompountStmt(nodes)  ##


    def parseExpStmt(self):
        node = self.parseExp()
        if node:
            self.eat(TokenType.SemiColon)
            return node    #PARAMETRY

    def parseDeclStmt(self):
        node = self.parseDecl()
        if node:
            self.eat(TokenType.SemiColon)
            return node   #PARAMETRY

    def parseWhileLoop(self):
        if self.current_token.type == TokenType.While:
            self.eat(TokenType.While)
            self.eat(TokenType.OpenParanthesis)
            boolexp = self.parseBExp()
            self.eat(TokenType.CloseParanthesis)
            return WhileStatement(condition=boolexp, body=self.parseStmt())

    #FOR LOOP
    def parseForLoop(self):
        return None

    def parseSelectionStmt(self):
        if self.current_token.type == TokenType.If:
            self.eat(TokenType.If)
            self.eat(TokenType.OpenParanthesis)
            cond = self.parseCondition()
            self.eat(TokenType.CloseParanthesis)
            true_stmt = self.parseStmt()
            if self.current_token.type == TokenType.Else:
                self.eat(TokenType.Else)
                return IfStatement(condition=cond, true_stmt=true_stmt, false_stmt=self.parseStmt())
            return IfStatement(condition=cond, true_stmt=true_stmt, false_stmt=None)

    def parseJumpStmt(self):
        if self.current_token.type == TokenType.Break:
            self.eat(TokenType.Break)
            self.eat(TokenType.SemiColon)
            return JumpStatement() #PARAMS
        elif self.current_token.type == TokenType.Continue:
            self.eat(TokenType.Continue)
            self.eat(TokenType.SemiColon)
            return JumpStatement() #PARAMS
        elif self.current_token.type == TokenType.Return:
            self.eat(TokenType.Return)
            if self.current_token.type != TokenType.SemiColon:
                self.parseReturnable() # IMPLEMENT
            self.eat(TokenType.SemiColon)
            return JumpStatement() #PARAMS


    #EXPRESSIONS 
    def parseExp(self):
        node = self.parseAExp()
        if node:
            return node
        node = self.parseBExp()
        if node:
            return node
        node = self.parseAssignment()
        if node:
            return node
        node = self.parseFunctionCall()
        if node:
            return node


    def parseAssignment(self):
        id = self.parseId()
        init = self.parseInitialization()
        if id and init:
            return AssignExp(id, init)

    def parseInitialization(self):
        if self.current_token.type == TokenType.Assign:
            self.eat(TokenType.Assign)
            return self.parseRValue()

    def parseRValue(self):
        node = self.parseId()
        if node:
            return node
        node = self.parseNumber()
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


    def parseDecl(self):
        node = self.parseParameter()
        if node:
            init = self.parseInitialization()
            return Decl(node, init)

    def parseParameter(self):
        if self.current_token.type in type_specifiers:
            token = self.current_token
            self.eat(token.type)
            return TypeSpec(token)
        return self.parseId() #SHOULD BE IDENTIFIER


    def parseFunctionCall(self):
        return None


    def stmt_parse(self):
        return self.parseStmt()



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
    parser = Parser(tokens)
    result = parser.stmt_parse()
    print(result)