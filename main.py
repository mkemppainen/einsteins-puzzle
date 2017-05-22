# bruteforcing won't work because there are something like 24,883,200,000
# combinations the houses could be in
# import Solver
from solving import Constraints, Solver
import solving

colors = ['red', 'green', 'ivory', 'yellow', 'blue']
people = ['englishman', 'spaniard', 'ukrainian', 'norwegian', 'japanese']
drinks = ['coffee', 'tea', 'milk', 'orange juice', 'water']
pets = ['dog', 'snails', 'fox', 'horse', 'zebra']
tobacco = ['old gold', 'kool', 'chesterfield', 'lucky strike', 'parliament']
attributes = [colors, people, drinks, pets, tobacco]

constraints = Constraints(5) \
    .together('englishman', 'red') \
    .together('spaniard', 'dog') \
    .together('coffee', 'green') \
    .together('ukrainian', 'tea') \
    .order('ivory', 'green') \
    .together('old gold', 'snails') \
    .together('kool', 'yellow') \
    .middle('milk') \
    .together('norwegian', 0) \
    .adjacent('chesterfield', 'fox') \
    .adjacent('kool', 'horse') \
    .together('lucky strike', 'orange juice') \
    .together('japanese', 'parliament') \
    .adjacent('norwegian', 'blue')
solver = Solver(attributes, constraints)
answer = solver.solve()
print(answer)


# houses are numbered from left to right from 0 to 4

# Solve not quite the Einstein's puzzle instead:
#
# 1. There are three houses.
# 2. The brit lives in the red house.
# 3. Norwegian lives in the second house.
# 4. American lives next to the house with a cat.
# 5. The dog lives in the green house.
# 6. The blue house is left of the green house.
#
# Who owns the goldfish? (brit)

# colors = ['red', 'blue', 'green']
# people = ['brit', 'norwegian', 'american']
# pets = ['cat', 'dog', 'goldfish']
# attributes = [people, colors, pets]
# goldfish_constraints = Constraints(3) \
#     .together('brit', 'red') \
#     .together('norwegian', 1) \
#     .adjacent('american', 'cat') \
#     .together('dog', 'green') \
#     .order('blue', 'green')
#
# solver = Solver(attributes, goldfish_constraints)
#
# answer = solver.solve()
# print(answer)

# answer = next(solver.solve())
# for group in answer:
#     if 'goldfish' in group:
#         # Attributes in the answer group are in
#         # the same order as in the input attributes
#         print('The %s owns the goldfish' % group[0])


# attributes: ([a,s,d],[1,2,3],[i,o,p])
# groups complete:  ([[a],[1],[i]],[[s],[2],[o]],[[d],[3],[p]])
# groups incomplete: (([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]))


# import pdb; pdb.set_trace()
# import code; code.interact(local=locals())

