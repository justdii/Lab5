from ast import *
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def compound_statement(self):
        """
        compound_statement: statement_list
        """
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list : statement (SEMI statement)*
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        statement : assignment_statement
                  | if_else_statement
                  | empty
        """
        if self.current_token.type == IF:
            node = self.if_else_statement()
        elif self.current_token.type == PRINT:
            node = self.print_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def if_else_statement(self):
        """
        if_else_statement : IF expr OPEN compound_statement CLOSE 
                             (ELSE OPEN compound_statement CLOSE)
        """
        token = self.current_token
        self.eat(IF)

        condition = self.expr()

        self.eat(OPEN)
        left = self.compound_statement()
        right = NoOp()
        self.eat(CLOSE)

        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat(OPEN)
            right = self.compound_statement()
            self.eat(CLOSE)

        return If(token, condition, left, right)

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def print_statement(self):
        """
        print_statement: PRINT expr
        """
        token = self.current_token
        self.eat(PRINT)
        right = self.expr()
        node = Print(token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """
        term : factor ((MUL | DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            right = self.factor()
            if isinstance(node, Num):
                if int(node.value) == 0:
                    """
                    0 * term -> Num(0)
                    0 / term -> Num(0)
                    """
                    node = Num(Token(INTEGER, 0))
                    continue
                if int(node.value) == 1:
                    """
                    1 * term -> term
                    """
                    node = right
                    continue
        
            if isinstance(right, Num):
                if int(right.value) == 0:
                    """
                    term * 0 -> Num(0)
                    """
                    if token.type == DIV: 
                        raise ZeroDivisionError("Division by zero")    

                    node = Num(Token(INTEGER, 0))
                    continue
                if int(right.value) == 1:
                    """
                    term * 1 -> term
                    """
                    continue

            node = BinOp(left=node, op=token, right=right)

        return node

    def factor(self):
        """factor : PLUS  factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        node = self.compound_statement()
        if self.current_token.type != EOF:
            self.error()

        return node