from ast import *

def main():
    text = '''
    a := 5 + 7;
    b:= a * 3;
    print 7
    '''

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

if __name__ == '__main__':
    main()