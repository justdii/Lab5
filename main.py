from ast import *

def main():
    text = '''
    a := 5.3 + 7;
    b:= a * 3;
    print a
    '''

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

if __name__ == '__main__':
    main()