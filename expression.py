from itertools import product, combinations

## base class for logical expressions
class Exp:
    def __init__(self):
        pass

    def __or__(self, other):
        return BinopExp('\\/',self, other)

    def __and__(self, other):
        return BinopExp('/\\',self, other)

    def __invert__(self):
        return NegExp(self)

    def to_nnf(self):
        '''
        converts expression to negative normal form
        '''
        nnf =  self._nnf1()
        nnf = nnf._nnf2()
        return nnf

    def _nnf2cnf(self):
        '''
        converts expression in nnf to cnf
        '''
        if isinstance(self,TermExp):
            return CNF([Disjunct([self])])
        elif isinstance(self,BinopExp): 
            if self.type == '\\/':
                return self.left._nnf2cnf() | self.right._nnf2cnf()

            elif self.type == '/\\':
                return self.left._nnf2cnf() & self.right._nnf2cnf()
            else:
                raise ValueError('expression is not in nnf')
        elif isinstance(self, NegExp):
            c = self.child
            if isinstance(c,TermExp):
                return CNF([Disjunct([self])])

    def to_cnf(self):
        nnf = self.to_nnf()
        return nnf._nnf2cnf()

## Class for binary operations
class BinopExp(Exp):
    prec = {'<->':5,
            '->':4,
            '\\/':3,
            '/\\':2,
            }

    def __init__(self,type,left,right):
        self.type = type
        self.left = left 
        self.right = right
        self.prec = BinopExp.prec[type]

    
    def __str__(self):
        lrepr = str(self.left)
        rrepr = str(self.right)
        if isinstance(self.left,BinopExp) and  self.left.prec > self.prec:
            lrepr = f'({lrepr})'
            if isinstance(self.right,BinopExp) and self.right.prec > self.prec:
                rrepr = f'({rrepr})'
        return f'{lrepr} {self.type} {rrepr}'

    def _nnf1(self):
        '''
        strip all implications and equivalences
        '''
        left = self.left._nnf1()
        right = self.right._nnf1()
        if self.type == '->':
            return ~left | right
        elif self.type == '<->':
            return (~left | right) & (left | ~right) 
        else:
            return BinopExp(self.type,left,right)
    def _nnf2(self):
        return BinopExp(self.type,self.left._nnf2(),self.right._nnf2())

## class for storage of negation operation
class NegExp(Exp):
    def __init__(self,child):
        self.child = child
        self.prec = 1

    def __eq__(self,other):
            return self.child == other.child

    def __hash__(self):
        return hash('~'+ str(hash(self.child)))

    def __str__(self):
        repr = f'~{str(self.child)}'
        if isinstance(self.child,BinopExp):
            return '(' + repr + ')'
        else:
            return repr
    def _nnf1(self):
        child =  self.child._nnf1()
        return ~child

    def _nnf2(self):
        '''
        applies de Morgan laws and double negation rule
        '''
        c = self.child._nnf2()
        if isinstance(c,BinopExp):
            if c.type == '\\/':
                d = ~c.left & ~c.right
            elif c.type == '/\\':
                d = ~c.left | ~c.right
            else:
                raise ValueError('wrong op')
        elif isinstance(c,NegExp):
            d = c.child
        elif isinstance(c,TermExp):
            if c.val == '0': return TermExp('1')
            elif c.val == '1': return TermExp('0')
            else: return ~c
        return d._nnf2() 

class TermExp(Exp):
    def __init__(self,val):
        self.val = val
    def __eq__(self,other):
        return self.val == other.val
    def __ne__(self, other):
        return self.val != other.val
    def __repr__(self):
        return f'TermExp({self.val})'
    def __hash__(self):
        return hash(self.val)
    def __str__(self):
        return self.val
    def _nnf1(self):
        return TermExp(self.val)
    def _nnf2(self):
        return TermExp(self.val)



       





## auxiliary class for constructin CNF
class Disjunct:
    def __init__(self,literals):
        # remove zeroes from disjunct, if disjunct is empty it is always false
        state = {l for l in literals if not isinstance(l,TermExp) or l != TermExp('0')}
        # if there is ones among literals, replace disjunct with tautology of invalid(for parser) variable name.
        if TermExp('1') in state:
            a = TermExp('_1')
            self.state = frozenset([a,~a])
        else:
            self.state = frozenset(state)

    def __eq__(self,other):
        return len(self.state.symmetric_difference(other.state)) == 0

    def __hash__(self):
        return hash((hash(x) for x in self.state))

    def __or__(self,d):
        return Disjunct(set().union(self.state,d.state))

    def __str__(self):
        repr = ' \\/ '.join(map(str,self.state))
        if len(self.state) > 1:
            return '(' + repr + ')'
        else:
            return repr
    
    ## functions for use in resolution method 
    def positive_literals(self):
        return frozenset({var.val for var in self.state if not isinstance(var,NegExp)})

    def negative_literals(self):
           return frozenset({var.child.val for var in self.state if isinstance(var,NegExp)})

    def is_tautology(self):
        pos = self.positive_literals()
        neg = self.negative_literals()
        return len(pos.intersection(neg)) != 0

    def make_clause(self):
        return (self.negative_literals(),self.positive_literals())
        
## constructs cnf from set of disjuncts or pair of cnf's
class CNF:
    def __init__(self, disjuncts):
       #remove tautologies:
        self.state = {d if not d.is_tautology() else Disjunct([TermExp('1')]) for d in disjuncts }

    def __and__(self,c):
        "trivially unite sets of dijuncts"
        return CNF(self.state.union(c.state))

    def __or__(self,c):
        "apply distribution law to interchange conjunctions and disjunctions"
        return CNF(a|b for a,b in product(self.state, c.state))

    def __str__(self):
        return ' /\\ '.join(str(d) for d in self.state)

    def make_clauses(self):
        return {x.make_clause() for x in self.state}


## tests if set of clauses (disjuncts) are satisfiable. Input is set of pairs (frozensets of positive and negative literals in each clause)
def resolution(clauses):
    pairs = combinations(clauses,2)
    n = len(clauses)
    for c1,c2 in pairs:
        # check whether there are complimentary literals in pair
        if(c1[0].intersection(c2[1]) or c1[1].intersection(c2[0])):
            pos_ = c1[0].union(c2[0])
            neg_ = c1[1].union(c2[1])
            # remove complimentary literals
            neg = neg_.difference(pos_)
            pos = pos_.difference(neg_)
        # if we can produce empty clause, then initial formula is unsatisfiable
            if len(pos) == 0 and len(neg) == 0:
                return 'no'
            clauses.add((pos,neg))
    # process is repeated until we unable to produce new clauses (or derive empty one)
    if n == len(clauses):
        return('yes')
    else:
        return resolution(clauses)


