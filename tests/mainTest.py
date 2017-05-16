if __name__ == '__main__':
    import sys
    import os
    sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
    from src.parser import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s filename' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    print(filename)
    stream = None

    os.system('g++ -std=c++11 -o other/a.out %s' % filename)
    os.system('other/a.out')
    print()

    with open(filename, 'r') as f:
        parser = Parser(f, True)
        try:
            parser.parseProgram()
        except SemanticError as e:
            print(e.__class__.__name__)
            print(e)
            sys.exit(0)

    parser.pygen.dump()
    os.system('python other/python_code.py')

