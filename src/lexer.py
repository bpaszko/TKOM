import sys
import re
from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class TokenType(AutoName):
    NewLine                 = auto()
    Int                     = auto()
    Long                    = auto()
    Float                   = auto()
    Double                  = auto()
    Char                    = auto()
    Bool                    = auto()
    Break                   = auto()
    Class                   = auto()
    Continue                = auto()
    Else                    = auto() 
    False_                  = auto()
    For                     = auto()
    If                      = auto()
    Private                 = auto()
    Protected               = auto()
    Public                  = auto()
    Return                  = auto()
    True_                   = auto()
    Void                    = auto()
    While                   = auto()
    LBracket                = auto()
    RBracket                = auto()
    Dot                     = auto()
    Assign                  = auto()
    OpenParanthesis         = auto()
    CloseParanthesis        = auto()
    SemiColon               = auto()
    Colon                   = auto()
    Plus                    = auto()
    Minus                   = auto()
    Asterix                 = auto()
    Slash                   = auto()
    LessOrEqual             = auto()
    LessThan                = auto()
    GreaterOrEqual          = auto()
    GreaterThan             = auto()
    Equals                  = auto()
    Differs                 = auto()
    Or                      = auto()
    And                     = auto()
    Not                     = auto()
    Character               = auto()
    FloatNum                = auto()
    IntNum                  = auto()
    Identifier              = auto()
    EOF                     = auto()


token_exprs = [
    ('\n',                          TokenType.NewLine),
    (r'[ \t]+',                     None),
    (r'//[^\n]*',                   None),
    (r'int',                        TokenType.Int),
    (r'long',                       TokenType.Long),
    (r'float',                      TokenType.Float),
    (r'double',                     TokenType.Double),
    (r'char',                       TokenType.Char),
    (r'bool',                       TokenType.Bool),
    (r'break',                      TokenType.Break),
    (r'class',                      TokenType.Class),
    (r'else',                       TokenType.Else),
    (r'false',                      TokenType.False_),
    (r'for',                        TokenType.For),
    (r'if',                         TokenType.If),
    (r'private',                    TokenType.Private),
    (r'protected',                  TokenType.Protected),
    (r'public',                     TokenType.Public),
    (r'return',                     TokenType.Return),
    (r'true',                       TokenType.True_),
    (r'void',                       TokenType.Void),
    (r'while',                      TokenType.While),
    (r'break',                      TokenType.Break),
    (r'continue',                   TokenType.Continue),
    (r'return',                     TokenType.Return),
    (r'\{',                         TokenType.LBracket),
    (r'\}',                         TokenType.RBracket),
    (r'\.',                         TokenType.Dot),
    (r'==',                         TokenType.Equals),
    (r'=',                          TokenType.Assign),
    (r'\(',                         TokenType.OpenParanthesis),
    (r'\)',                         TokenType.CloseParanthesis),
    (r';',                          TokenType.SemiColon),
    (r'\:',                         TokenType.Colon),
    (r'\+',                         TokenType.Plus),
    (r'-',                          TokenType.Minus),
    (r'\*',                         TokenType.Asterix),
    (r'/',                          TokenType.Slash),
    (r'<=',                         TokenType.LessOrEqual),
    (r'>=',                         TokenType.GreaterOrEqual),
    (r'<',                          TokenType.LessThan),
    (r'>',                          TokenType.GreaterThan),
    (r'!=',                         TokenType.Differs),
    (r'\|\|',                       TokenType.Or),
    (r'&&',                         TokenType.And),
    (r'!',                          TokenType.Not),
    (r'\'((\\t)|.| )\'',            TokenType.Character),
    (r'(\d+(\.\d*))',               TokenType.FloatNum),
    (r'(([1-9]\d*)|0)',             TokenType.IntNum),
    (r'[A-Za-z][A-Za-z0-9_]*',      TokenType.Identifier),
]


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def imp_lex(self, characters):
        return self.lex(characters, token_exprs)

    def lex(self, characters, token_exprs):
        pos = 0
        line_num = 1
        tokens = []
        while pos < len(characters):
            match = None
            for token_expr in token_exprs:
                pattern, tag = token_expr
                regex = re.compile(pattern)
                match = regex.match(characters, pos)
                if match:
                    if tag == TokenType.NewLine:
                        line_num += 1
                        break
                    text = match.group(0)
                    if tag:
                        token = Token(tag, text)
                        tokens.append(token)
                    break
            if not match:
                sys.stderr.write('Illegal character: %s, at line %d\n' % (characters[pos], line_num))
                sys.exit(1)
            else:
                pos = match.end(0)
        return tokens


if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    lexer = Lexer()
    tokens = lexer.imp_lex(characters)
    for token in tokens:
        print(token.value, "\t-->\t", token.type)