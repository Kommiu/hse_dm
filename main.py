from parser import parser
import expression as e


if __name__ == '__main__':
    while True:
        try:
            s = input('Logical expression:> ')
        except EOFError:
            break
        p = parser.parse(s)
        cnf = p.to_cnf()
        clauses = cnf.make_clauses()
        print(f'CNF of {str(p)}:')
        print(cnf)
        print('Is formula satisfiable?')
        print(e.resolution(clauses))

else:
    s = '(a->d2<->0)//\~v\//1'
    p = parser.parse(s)
    print(p)
    print(p.to_cnf())
    print(e.resolution(p.to_cnf().make_clauses()))
