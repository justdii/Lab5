from ast import *

def main():
    text = '''
    a := 5*99999+0;
    b:= 35 + 3            -- 1 * a;
    print b;
    print a;
    c:= 99*9 + a -b;
    print c + 2*10*(1-2)
    '''

    iftext = '''
    a := 3;
    c := 5;
    if a-2 {
        x := 16;
        if x*2 {
            print 0
        };
        print 8;
        print 17
    }else {
        print 4;
        print c
    };
    print 99
    '''

    lexer = Lexer(iftext)

    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

if __name__ == '__main__':
    main()