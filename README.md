# hse_dm
__author__: Misiutin Roman 

withdrawal assignment for discrete math course

files:
1. _main.py_ prompts for logical expression, and for syntactically correct ones derives and prints CNF, and then check it for satisfiability.
2. _parser.py_  contains rules for ply generated lexer and parser,
3. _expression.py_ contains classes for representation of logical expression and also function for testing satisfiability with resolution method  

Valid operations: ~, /\, \/, ->, <-> (in this order of precedence) and also grouping with parentheses. Equivalence and implication are asumed right associative.  
Empty cnf corresponds to false statement. Tautology is denoted as '_1 \\/ ~_1'.  

Tested with python 3.7 and ply 3.11
