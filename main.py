from ast import *

def main():

    with open("source.dd") as f:
        code = ''.join(f.readlines())
    print(code)
    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

if __name__ == '__main__':
    main()