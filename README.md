# hse_dm
__author__: Misiutin Roman 

withdrawal assignment for discrete math course

main.py prompts for logical expression, and for syntactically correct ones derives and prints CNF, and then check it for satisfiability.
parser.py  contains rules for ply generated lexer and parser, expression.py contains classes for representation of logical expression and also function for testing satisfiability with resolution method  
Valid operations: ~, /\, \/, ->, <-> (in this order of precedence) and grouping with parentheses. Equivalence and implication asumed right associative.  
Empty cnf corresponds to false statement. Tautology is denoted as '_1 \/ ~_1'.  
Tested with python 3.7 and ply 3.11
