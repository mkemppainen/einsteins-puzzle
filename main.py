from solving import Constraints, Solver

colors = ['red', 'green', 'ivory', 'yellow', 'blue']
people = ['englishman', 'spaniard', 'ukrainian', 'norwegian', 'japanese']
drinks = ['coffee', 'tea', 'milk', 'orange juice', 'water']
pets = ['dog', 'snails', 'horse', 'zebra', 'fox']
tobacco = ['old gold', 'kool', 'chesterfield', 'lucky strike', 'parliament']
attributes = [colors, people, drinks, pets, tobacco]

constraints = Constraints() \
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
answer, _ = solver.solve()

# People are defined in index 1
for group in answer:
    # print(group[1][0])
    if ['water'] in group:
        print("The {} drinks water.".format(group[1][0]))
    if ['zebra'] in group:
        print("The {} owns the zebra.".format(group[1][0]))