from kanren import *

# colors = ['red', 'green', 'ivory', 'yellow', 'blue']
# people = ['englishman', 'spaniard', 'ukrainian', 'norwegian', 'japanese']
# drinks = ['coffee', 'tea', 'milk', 'orange juice', 'water']
# pets = ['dog', 'snails', 'horse', 'zebra', 'fox']
# tobacco = ['old gold', 'kool', 'chesterfield', 'lucky strike', 'parliament']
# attributes = [colors, people, drinks, pets, tobacco]

# constraints = Constraints() \
#     .together('englishman', 'red') \
#     .together('spaniard', 'dog') \
#     .together('coffee', 'green') \
#     .together('ukrainian', 'tea') \
#     .order('ivory', 'green') \
#     .together('old gold', 'snails') \
#     .together('kool', 'yellow') \
#     .middle('milk') \
#     .together('norwegian', 0) \
#     .adjacent('chesterfield', 'fox') \
#     .adjacent('kool', 'horse') \
#     .together('lucky strike', 'orange juice') \
#     .together('japanese', 'parliament') \
#     .adjacent('norwegian', 'blue')

# Var('House')
# a, b, c, d, e = vars(5)
#
# r = run(1, (a,b,c,d,e),
#            (membero, a, colors),
#            (membero, b, people),
#            (membero, c, drinks),
#            (membero, d, pets),
#            (membero, e, tobacco))
# print(list(r))

colors = ['red', 'green', 'ivory', 'yellow', 'blue']
people = ['englishman', 'spaniard', 'ukrainian', 'norwegian', 'japanese']
drinks = ['coffee', 'tea', 'milk', 'orange juice', 'water']
pets = ['dog', 'snails', 'horse', 'zebra', 'fox']
tobacco = ['old gold', 'kool', 'chesterfield', 'lucky strike', 'parliament']
# attributes = [colors, people, drinks, pets, tobacco_brand]



# todo: use facts to determine colors, people etc.

# color, nativity, drink, pet, tobacco = [Relation() for _ in range(5)]
attributes = Relation()
facts(attributes, *(('tobacco', x) for x in tobacco),
                  *(('person', x) for x in people),
                  *(('pet', x) for x in pets),
                  *(('drink', x) for x in drinks),
                  *(('color', x) for x in colors))



def test(x):
    return type(x) == int

if False:
    testo = goalify(test)

    house = Relation()
    facts(house, )

    x = var()
    y = var()

    results = run(0, x, (membero, x, [1, 2, 3, 'cat','dd']), (testo, x, True))

    # results = run(2, (x,y) , attributes('tobacco', x),
    #                         attributes('person', y))

    for result in results:
        print(result)


# cond, vars = houses()
# results = run(7, vars, cond)
# for r in results:
#     print(r)

# cond, atts = houses(5)
# x = var()
# a=houses(1)
# print(next(a)[0])
#
# pair = [(c, (eq, x, a)) for c, a in houses(5)]
# print(pair[0])
# results = run(4, x,
#               # *(cond, (eq, x, atts)),
#               *pair
#               )
# print(*((c, (eq, x, a)) for c, a in houses(5)))


# for r in results:
#     print(r)

# def houses(n):
#     return range(n)

def make_houses():
    n = 5
    for _ in range(n):
        a, b, c, d, e = vars(n)
        cond = lall((membero, a, colors),
                    (membero, b, people),
                    (membero, c, drinks),
                    (membero, d, pets),
                    (membero, e, tobacco))
        yield cond, (a,b,c,d,e)

def together(group):
    return True

has_attributeo = goalify(lambda group, el: el in group)
""" Return goal for group has attribute. """


if __name__ == '__main__':
    a = (2,3)
    houses = make_houses()
    house1, house2, house3, house4, house5 = houses
    # houses are (cond, vars)
    # print(house1[0])
    results = ()
    x = var()
    # print(has_attributeo(([1,2,3],8), 'df'))
    results= run(5, house1[1], house1[0], (has_attributeo, (house1[1], 'japanese'), True))
    # g = [2,3,4,8]
    # results = run(0, x, membero(x, [1,2,3,4,5]), (has_attributeo, (g, x), True))

    # results = run(5, house1[1], house1[0],
    #               lany(
    #                   (membero, )
    #
    #               ))

    for r in results:
        print(r)




    # x = var()
    # set_a = {1, 2, 3}
    # set_b = {2, 3, 4}
    # r= run(10, x, (membero, x, set_a),  # x is a member of (1, 2, 3)
    #              (membero, x, set_b))  # x is a member of (2, 3, 4)
    #
    # parent = Relation()
    # facts(parent, ("Homer", "Bart"),
    #               ("Marge", "Bart"),
    #               ("Homer", "Lisa"),
    #               ("Marge", "Lisa"),
    #               ("Homer", "Maggie"),
    #               ("Marge", "Maggie"),
    #               ("Abe",  "Homer"))
    #
    #
    # y = var()
    # run(1, x, parent(x, y),
    #           parent(y, 'Bart'))
    # r= run(1, (x, y), parent(x, y),
    #                parent(y, 'Bart'))

# permuteq(a,b)
# For example (1, 2, 2) equates to (2, 1, 2) under permutation

# seteq(a,b)
# For example (1, 2, 3) set equates to (2, 1, 3)

# funo = goalify(fun)
# constructs a goal so that
# funo(arg, x) -> fun(arg) == x

# adjacent(att1, att2)
# if group contains 'attribute1' -> left or right group contains 'attribute2'