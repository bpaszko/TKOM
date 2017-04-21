from my_ast import *
from lexer import *

comp_operators = ['!=', '==', '>', '<', '>=', '<=', '=']

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
    result = parser.bexp()
    print(result)