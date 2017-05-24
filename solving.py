from copy import deepcopy
from collections import Counter
import itertools
import time
import doctest

class NoMatchException(Exception):
    pass

class UnsolvableException(Exception):
    pass

class Solver:
    """ Can be used to solve logic puzzles such as Einsteins puzzle. """
    def __init__(self, attributes, constraints):
        # list of attributes: [['att1','att2'],['otheratt1','otheratt2']]
        self.attributes = attributes
        # list of functions
        self.constraints = constraints.constraints
        self.groups = []
        # initialize with groups containing all attributes
        self.groups = [deepcopy(attributes) for _ in range(len(attributes[0]))]

    # todo apply constraints and alternate with bruteforce
    def solve(self):
        return apply_constraints(self.constraints, self.groups)




def apply_constraints(constraints, groups):
    """ Apply all constraints several times as long as groups change. """
    last_iteration = ''
    while last_iteration != str(groups):
        last_iteration = str(groups.copy())
        for constraint in constraints:
            constraint(groups)
        only_one_attribute_constraint(groups)
    return groups

def only_one_attribute_constraint(groups):
    """ Remove other attributes from group if an attribute is the only one. 
    
    If an attribute exists in exactly one group, remove other
    attributes of that type from that group.
    
    # there is only one 'red' so remove other colors from the same group
    >>> groups = [[['red', 'blue', 'green']], [['blue', 'green']]]
    >>> only_one_attribute_constraint(groups)
    [[['red']], [['blue', 'green']]]
    """
    ### Remove other attributes from group of a lone attribute
    flattened = [x for y in groups for z in y for x in z]
    counts = Counter(flattened)
    for attribute, count in counts.items():
        if count == 1:
            indexes = attribute_indexes(groups, attribute)
            for index in indexes:
                remove_other_attributes(groups, index, attribute)

    return groups

def solved_attribute_constraint(groups):
    """ Remove solved attribute from other groups.
    
    If there is only one attribute of a specific type in a group,
    remove the attribute from all the other groups.
    
    # 'blue' is alone in a group so remove it from everywhere else
    >>> groups = [[['blue', 'green'], ['cat','dog']], [['red','blue']], [['blue']]]
    >>> solved_attribute_constraint(groups)
    [[['green'], ['cat', 'dog']], [['red']], [['blue']]]
    
    # 'red' is a loner in 2 groups so task is unsolvable
    >>> groups2 = [[['red']], [['red']], [['blue', 'red']]]
    >>> solved_attribute_constraint(groups2) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnsolvableException
    
    # multiple singleton attributes
    >>> groups3 = [[['green'], ['cat', 'dog']], [['blue', 'green'], ['cat']], [['yellow'], []]]
    >>> solved_attribute_constraint(groups3)
    [[['green'], ['dog']], [['blue'], ['cat']], [['yellow'], []]]
    """
    singleton_indexes = {}
    for group in enumerate(groups):
        for attributes in group[1]:
            if len(attributes) == 1 and attributes[0] in singleton_indexes:
                raise UnsolvableException("Multiple groups with only one possible attribute.")
            elif len(attributes) == 1:
                singleton_indexes[attributes[0]] = group[0]
    for attribute, index in singleton_indexes.items():
        indexes_to_remove = set(range(len(groups))).difference({index})
        remove_attributes(groups, indexes_to_remove, [attribute])
    return groups


def remove_other_attributes(groups, index, attribute):
    for attributes in groups[index]:
        if attribute in attributes:
            attributes.clear()
            attributes.append(attribute)


def attribute_indexes(groups, attribute):
    """ Return indexes of groups that contain the attribute.
    
    If attribute is a number, return it inside a list instead
    """
    if(isinstance(attribute, int )):
        return [attribute]
    indexes = []
    for group in enumerate(groups):
        for attributes in group[1]:
            if attribute in attributes:
                indexes.append(group[0])
    return indexes

def remove_attributes(groups, indexes, attributes):
    """ Remove all given attributes from the given indexes.
    
    >>> groups = [[['blue'], ['cat', 'dog']], [['red', 'blue'], ['cat', 'dog']]]
    >>> remove_attributes(groups, [0, 1], ['cat'])
    [[['blue'], ['dog']], [['red', 'blue'], ['dog']]]
    >>> remove_attributes(groups, [1], ['red', 'dog'])
    [[['blue'], ['dog']], [['blue'], []]]
    """
    for index in indexes:
        for group in groups[index]:
            for attribute in attributes:
                if attribute in group:
                    group.remove(attribute)
    return groups

# todo: constraint: when attribute is constrained with attribute that is the sole one
# todo:             one can remove other attributes of those types
# todo:             in both styles like only_one_attribute and solved_attribute constraints
class Constraints:
    """ Defines constraints for solver.
    
    Data attribute 'constraints' contains a list of functions that
    can be used to test if a a list of groups fulfills the constraints.
    Ordering of the group list matters: first item in the list is the 
    leftmost group and last is the rightmost.
    """

    def __init__(self):
        """ Initialize constraints with a number of groups."""
        self.constraints = []

    def together(self, attribute1, attribute2):
        """ Add constraint: Attributes belong in the same group.
        >>> groups = [[['blue', 'green'],['cat','dog']],[['red','blue'],['cat','dog']]]
        >>> constraints = Constraints()
        >>> constraints.together('red','cat') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> constraints.constraints[0](groups)
        [[['blue', 'green'], ['dog']], [['red', 'blue'], ['cat', 'dog']]]
        >>> constraints.together('green','dog') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> constraints.constraints[1](groups)
        [[['blue', 'green'], ['dog']], [['red', 'blue'], ['cat']]]
        """
        def together_test(groups):
            """ Remove attributes that don't adhere to constraints from the groups. """
            indexes1 = set(attribute_indexes(groups, attribute1))
            indexes2 = set(attribute_indexes(groups, attribute2))
            wrong_indexes = indexes1.symmetric_difference(indexes2)
            if len(wrong_indexes) == len(groups):
                raise NoMatchException("No attributes found together.")
            if len(indexes1) == 1 or len(indexes2) == 1:
                # todo: remove other attributes in 2 ways
                pass
            remove_attributes(groups, wrong_indexes, [attribute1, attribute2])
            return groups

        self.constraints.append(together_test)
        return self

    def adjacent(self, attribute1, attribute2):
        """ Add constraint: Attributes are next to each other in any order.

        >>> constraints = Constraints() 
        >>> constraints.adjacent('red','cat') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> groups = [[['blue'],['cat','dog']],[['red','blue'],['cat','dog']]]
        >>> constraints.constraints[0](groups)
        [[['blue'], ['cat', 'dog']], [['red', 'blue'], ['dog']]]
        >>> groups2 = [[['red'],['cat','dog']],[['red','green'],['dog']]]
        >>> constraints.constraints[0](groups2)
        [[[], ['cat', 'dog']], [['red', 'green'], ['dog']]]
        >>> groups3 = [[['red']],[['dog']]]
        >>> constraints.constraints[0](groups3) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        NoMatchException
        >>> groups4 = [[['red']], [['llama']], [['red', 'green']], [['cat']]]
        >>> constraints.constraints[0](groups4)
        [[[]], [['llama']], [['red', 'green']], [['cat']]]
        """

        def adjacent_test(groups):
            index1 = set(attribute_indexes(groups, attribute1))
            index2 = set(attribute_indexes(groups, attribute2))
            length = len(groups)
            # attribute is legal if the other attribute is on either side
            legal_indexes1 = {item for i in index2 for item in (i-1, i+1)
                              if 0 <= item < length}
            legal_indexes2 = {item for i in index1 for item in (i-1, i+1)
                              if 0 <= item < length}
            if len(legal_indexes1) == 0:
                raise NoMatchException("No matching adjacent attributes found.")
            wrong_indexes1 = set(range(length)).difference(legal_indexes1)
            # if len(wrong_indexes1) == len(groups):
            #     raise NoMatchException("No matching adjacent attributes found.")
            wrong_indexes2 = set(range(length)).difference(legal_indexes2)
            remove_attributes(groups, wrong_indexes1, [attribute1])
            remove_attributes(groups, wrong_indexes2, [attribute2])
            return groups

        self.constraints.append(adjacent_test)
        return self

    def order(self, attribute1, attribute2):
        """ Add constraint: First attribute is adjacent and left of the second.
        >>> constraints = Constraints() 
        >>> constraints.order('red','cat') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> groups = [[['red', 'blue'], ['cat','dog']], [['red', 'blue'], ['cat', 'dog']]]
        >>> constraints.constraints[0](groups)
        [[['red', 'blue'], ['dog']], [['blue'], ['cat', 'dog']]]
        >>> groups2 = [[['red'],['cat','dog']],[['red','green'],['dog']]]
        >>> constraints.constraints[0](groups2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        NoMatchException
        >>> groups3 = [[['red']],[['cat']]]
        >>> constraints.constraints[0](groups3)
        [[['red']], [['cat']]]
        >>> groups4 = [[['red']], [['llama']], [['red', 'green']], [['cat']]]
        >>> constraints.constraints[0](groups4)
        [[[]], [['llama']], [['red', 'green']], [['cat']]]
        """

        def order_test(groups):
            index1 = set(attribute_indexes(groups, attribute1))
            index2 = set(attribute_indexes(groups, attribute2))
            length = len(groups)
            legal_indexes1 = {item - 1 for item in index2 if 0 <= item - 1 < length}
            legal_indexes2 = {item + 1 for item in index1 if 0 <= item + 1 < length}
            if len(legal_indexes1) == 0:
                raise NoMatchException("No matching adjacent attributes found.")
            wrong_indexes1 = set(range(length)).difference(legal_indexes1)
            wrong_indexes2 = set(range(length)).difference(legal_indexes2)
            remove_attributes(groups, wrong_indexes1, [attribute1])
            remove_attributes(groups, wrong_indexes2, [attribute2])
            return groups

        self.constraints.append(order_test)
        return self

    def middle(self, attribute):
        """ Add constraint: Attribute is in the middle group. If number
        of groups is even both centermost groups are considered middle.
        
        >>> constraints = Constraints() 
        >>> constraints.middle('red') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> groups = [[['red', 'blue']], [['red', 'blue']], [['cat', 'dog']]]
        >>> constraints.constraints[0](groups)
        [[['blue']], [['red', 'blue']], [['cat', 'dog']]]
        >>> groups2 = [[['red']],[['cat']]]
        >>> constraints.constraints[0](groups2)
        [[['red']], [['cat']]]
        >>> groups3 = [[['red']], [['black']], [['red']]]
        >>> constraints.constraints[0](groups3) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        NoMatchException
        """

        def middle_test(groups):
            middle = len(groups) // 2
            indexes = {middle}
            if len(groups) % 2 == 0:
                indexes.add(middle - 1)
            wrong_indexes = set(range(len(groups))).difference(indexes)

            if len(set(attribute_indexes(groups, attribute)).intersection(indexes)) < 1:
                raise NoMatchException("No attribute found in the middle.")

            remove_attributes(groups, wrong_indexes, [attribute])
            return groups

        self.constraints.append(middle_test)
        return self

if __name__ == '__main__':
    doctest.testmod()

# a,s,d   1,2,3   i,o,p
# attributes: ([a,s,d],[1,2,3],[i,o,p])
# groups complete:  ([[a],[1],[i]],[[s],[2],[o]],[[d],[3],[p]])
# groups incomplete:
# (([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]))

# kaikki mahdollisuudet on groupissa
# ota groupeista pois attribuutteja constrainttien perusteella:
#   muuta constraintit palauttamaan listan vaarista indekseista tai
#   poistamaan attribuutit jotka eivat vastaa constraintteja
# todo: lisaa 'universaaleja' constraintteja:
# esim attribuutti voi
# olla vain kerrallaan yhdessa groupissa. jos yksi group tai sen
# attribuutti on varma, sen voi poistaa muualta