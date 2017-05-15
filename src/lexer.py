import sys
import re
import io
from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TokenType(AutoName):
    #NewLine = auto()
    Int = auto()
    Long = auto()
    Float = auto()
    Double = auto()
    Char = auto()
    Bool = auto()
    Break = auto()
    Class = auto()
    Continue = auto()
    Else = auto()
    False_ = auto()
    For = auto()
    If = auto()
    Private = auto()
    Protected = auto()
    Public = auto()
    Return = auto()
    True_ = auto()
    Void = auto()
    While = auto()
    Comma = auto()
    LBracket = auto()
    RBracket = auto()
    Dot = auto()
    Assign = auto()
    OpenParanthesis = auto()
    CloseParanthesis = auto()
    SemiColon = auto()
    Colon = auto()
    Plus = auto()
    Minus = auto()
    Asterix = auto()
    Slash = auto()
    LessOrEqual = auto()
    LessThan = auto()
    GreaterOrEqual = auto()
    GreaterThan = auto()
    Equals = auto()
    Differs = auto()
    Or = auto()
    And = auto()
    Not = auto()
    Character = auto()
    FloatNum = auto()
    IntNum = auto()
    Identifier = auto()
    EOF = auto()


token_exprs = [
    ('\n', None),
    (r'[ \t]+', None),
    (r'//[^\n]*', None),
    (r'std::cout[^\n]*', None),
    (r'#include[^\n]*', None),
    (r'int(?![A-Za-z\d])', TokenType.Int),
    (r'long(?![A-Za-z\d])', TokenType.Long),
    (r'float(?![A-Za-z\d])', TokenType.Float),
    (r'double(?![A-Za-z\d])', TokenType.Double),
    (r'char(?![A-Za-z\d])', TokenType.Char),
    (r'bool(?![A-Za-z\d])', TokenType.Bool),
    (r'break(?![A-Za-z\d])', TokenType.Break),
    (r'class(?![A-Za-z\d])', TokenType.Class),
    (r'continue(?![A-Za-z\d])', TokenType.Continue),
    (r'else(?![A-Za-z\d])', TokenType.Else),
    (r'false(?![A-Za-z\d])', TokenType.False_),
    (r'for(?![A-Za-z\d])', TokenType.For),
    (r'if(?![A-Za-z\d])', TokenType.If),
    (r'private(?![A-Za-z\d])', TokenType.Private),
    (r'protected(?![A-Za-z\d])', TokenType.Protected),
    (r'public(?![A-Za-z\d])', TokenType.Public),
    (r'return(?![A-Za-z\d])', TokenType.Return),
    (r'true(?![A-Za-z\d])', TokenType.True_),
    (r'void(?![A-Za-z\d])', TokenType.Void),
    (r'while(?![A-Za-z\d])', TokenType.While),
    (r',', TokenType.Comma),
    (r'\{', TokenType.LBracket),
    (r'\}', TokenType.RBracket),
    (r'\.', TokenType.Dot),
    (r'==', TokenType.Equals),
    (r'=', TokenType.Assign),
    (r'\(', TokenType.OpenParanthesis),
    (r'\)', TokenType.CloseParanthesis),
    (r';', TokenType.SemiColon),
    (r'\:', TokenType.Colon),
    (r'\+', TokenType.Plus),
    (r'-', TokenType.Minus),
    (r'\*', TokenType.Asterix),
    (r'/', TokenType.Slash),
    (r'<=', TokenType.LessOrEqual),
    (r'>=', TokenType.GreaterOrEqual),
    (r'<', TokenType.LessThan),
    (r'>', TokenType.GreaterThan),
    (r'!=', TokenType.Differs),
    (r'\|\|', TokenType.Or),
    (r'&&', TokenType.And),
    (r'!', TokenType.Not),
    (r'\'((\\t)|.| )\'', TokenType.Character),
    (r'(\d+(\.\d*))', TokenType.FloatNum),
    (r'(([1-9]\d*)|0)', TokenType.IntNum),
    (r'[A-Za-z_][A-Za-z0-9_]*', TokenType.Identifier),
]


class Token:
    def __init__(self, type, value, line=None):
        self.type = type
        self.value = value
        self.line = line

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __repr__(self):
        return 'TokenType: %s, value: %s' % (self.type.name, self.value)



class LexError(Exception):
    def __init__(self, char, line_num):
        self.char = char
        self.line_num = line_num

    def __repr__(self):
        return 'Illegal character: %s, at line %d\n' % (self.char, self.line_num)

class EndOfInputError(Exception):
    pass


class Lexer:
    def __init__(self, stream):
        self.stream = stream
        self.current_tokens = list()
        self.pos = 0
        self.current_line = 1
        self.load_more_tokens()

    def get_next_token(self):
        if self.pos == len(self.current_tokens):
            if self.current_tokens[self.pos-1].type == TokenType.EOF:
                raise EndOfInputError

        while self.pos >= len(self.current_tokens):
            self.load_more_tokens()
        token = self.current_tokens[self.pos]
        self.pos += 1
        return token
        

    def revert(self, pos):
        self.pos = pos


    def load_more_tokens(self):
        next_line = self.stream.readline()
        if not next_line:
            self.current_tokens += [Token(TokenType.EOF, 'EOF', self.current_line)]
            return
        #self.current_tokens += self.lex_line(next_line)
        tokens = self.lex_line(next_line)
        if not tokens:
            self.current_line += 1
            self.load_more_tokens()
        else:
            self.current_tokens += tokens
            self.current_line += 1


    def lex_line(self, characters):
        global token_exprs
        pos = 0
        tokens = []
        while pos < len(characters):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = Token(tag, text, self.current_line)
                        tokens.append(token)
                    break
            if not match:
                raise LexError(characters[pos], self.current_line)
            else:
                pos = match.end(0)
        return tokens


if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    lexer = Lexer()
    tokens = lexer.cpp_lex(characters)
    for token in tokens:
        print(token.value, "\t-->\t", token.type)
