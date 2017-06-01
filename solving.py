from copy import deepcopy
from collections import Counter
import itertools
import time
import doctest


class UnsolvableException(Exception):
    pass


class Solver:
    """ Can be used to solve logic puzzles such as Einsteins puzzle. """
    def __init__(self, attributes, constraints):
        # list of attributes: [['att1','att2'],['otheratt1','otheratt2']]
        self.attributes = attributes
        # list of functions>
        self.constraints = constraints.constraints
        self.groups = []
        # initialize with groups containing all attributes
        self.groups = [deepcopy(attributes) for _ in range(len(attributes[0]))]

    def solve(self):
        apply_constraints(self.constraints, self.groups)
        return try_to_solve(self.constraints, self.groups)


def try_to_solve(constraints, groups, start_offset=0):
    """ Try to recursively solve the puzzle."""
    original_copy = deepcopy(groups)
    try:
        apply_constraints(constraints, groups)
    except UnsolvableException:
        return [], False

    flattened = flatten_groups(groups)
    if len(flattened) == len(set(flattened)):
        return groups, True
    copy = deepcopy(groups)
    offset = start_offset
    # Offsets to skip
    skip_offsets = set()
    # Offsets to return
    return_skip_offsets = generate_skip_offsets(original_copy, copy)
    while True:
        if offset in skip_offsets:
            offset += 1
            continue
        if remove_possibility(copy, offset):
            result, success = try_to_solve(constraints, copy, offset)
            if success:
                return result, True
            else:
                copy = deepcopy(groups)
                skip_offsets.update(result)
                offset += 1
        else:
            # This path was exhausted
            return return_skip_offsets, False


def generate_skip_offsets(groups1, groups2):
    """ Return list of offsets to skip for function remove_possibility.

    If remove_possibility is called with group1 and all the offsets from the
    return value starting from the last, the result will be group2.

    group2 must be same as group1 with some values removed. Else return nonsense.

    >>> groups1 = [[['cat', 'dog', 'bat']]]
    >>> groups2 = [[['dog']]]
    >>> skips = generate_skip_offsets(groups1, groups2)
    >>> skips
    [0, 2]
    >>> remove_possibility(groups1, skips[1])
    True
    >>> remove_possibility(groups1, skips[0])
    True
    >>> groups1 == groups2
    True
    >>> groups3 = [[['cat', 'dog'], ['red', 'blue']], [['horse'], ['red', 'blue']], [['bat']]]
    >>> groups4 = [[['dog'], ['blue']], [['horse'], ['red']],[['bat']]]
    >>> generate_skip_offsets(groups3, groups4)
    [0, 2, 5]
    >>> groups5 = [[['dog'], ['blue']], [['horse'], ['red', 'blue', 'green']]]
    >>> groups6 = [[['dog'], ['blue']], [['horse'], ['green']]]
    >>> generate_skip_offsets(groups5, groups6)
    [0, 1]

    # first list must be longer
    >>> generate_skip_offsets([[['mad']]], [[['bat', 'cat']]]) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    >>> generate_skip_offsets([[['cat']]], [[['cat']]])
    []
    """
    copy1 = deepcopy(groups1)
    copy2 = deepcopy(groups2)

    # remove singleton lists because function remove_possibility skips them
    for group1, group2 in zip(copy1, copy2):
        for attributes1, attributes2 in zip(group1, group2):
            if len(attributes1) == 1:
                attributes1.clear()
                attributes2.clear()

    flattened1 = flatten_groups(copy1)
    flattened2 = flatten_groups(copy2)
    if len(flattened1) < len(flattened2):
        raise ValueError("First group is shorter than second.")

    missing_attribute_indexes = []
    offset = 0
    next_index = 0
    for i, attribute in enumerate(flattened1):
        try:
            other_attribute = flattened2[next_index]
        except IndexError:
            other_attribute = None
        if other_attribute == attribute:
            next_index += 1
            continue
        else:
            missing_attribute_indexes.append(i)
            offset += 1
    return missing_attribute_indexes


def remove_possibility(groups, offset=0):
    """ Removes one attribute from attribute group where there are several. 
    
    Skip 'offset' number of possible removals.
    Return True if successfully removed an attribute. If can't remove any
    attributes (possibly because of offset), return False.
    
    >>> groups = [[['red', 'blue', 'green']], [['blue', 'green']]]
    >>> remove_possibility(groups) #1
    True
    >>> groups #1
    [[['blue', 'green']], [['blue', 'green']]]
    >>> remove_possibility(groups) #2
    True
    >>> groups #2
    [[['green']], [['blue', 'green']]]
    >>> remove_possibility(groups) #3
    True
    >>> groups #3
    [[['green']], [['green']]]
    >>> remove_possibility(groups) #4
    False
    >>> groups #4
    [[['green']], [['green']]]
    
    >>> groups2 = [[['cat', 'dog', 'bat', 'fish', 'mouse']]]
    >>> remove_possibility(groups2, 4) #1
    True
    >>> groups2
    [[['cat', 'dog', 'bat', 'fish']]]
    >>> remove_possibility(groups2, 5) #2
    False
    >>> groups2 #2
    [[['cat', 'dog', 'bat', 'fish']]]
    
    >>> groups3 = [[['cat', 'dog'], ['red', 'blue']], [['fish'], ['red', 'blue']]]
    >>> remove_possibility(groups3, 4) #1
    True
    >>> groups3 #1
    [[['cat', 'dog'], ['red', 'blue']], [['fish'], ['blue']]]
    >>> remove_possibility(groups3, 3) #2
    True
    >>> groups3 #2
    [[['cat', 'dog'], ['red']], [['fish'], ['blue']]]
    >>> remove_possibility(groups3, -1) #3
    False
    >>> groups3 #3
    [[['cat', 'dog'], ['red']], [['fish'], ['blue']]]
    """
    if offset < 0:
        return False
    skips_left = offset
    for group in groups:
        for attributes in group:
            if len(attributes) > 1:
                if skips_left < len(attributes):
                    attributes.pop(skips_left)
                    return True
                else:
                    skips_left -= len(attributes)
    return False


def length_check(groups):
    """ Return list of lengths of attribute groups."""
    return [len(atts) for group in groups for atts in group]


def apply_constraints(constraints, groups):
    """ Apply all constraints several times as long as groups change. """
    last_iteration = ''
    iteration_count = 0
    while last_iteration != str(groups):
        iteration_count += 1
        last_iteration = str(groups)
        for constraint in constraints:
            constraint(groups)
        only_one_attribute_constraint(groups)
        solved_attribute_constraint(groups)
    return groups


def flatten_groups(groups):
    """ Return groups as flattened list.
    
    >>> flatten_groups([[['red', 'blue'], ['cat', 'dog']], [['cat']]])
    ['red', 'blue', 'cat', 'dog', 'cat']
    """
    return [x for y in groups for z in y for x in z]


def only_one_attribute_constraint(groups):
    """ Remove other attributes from group if an attribute is the only one. 
    
    If an attribute exists in exactly one group, remove other
    attributes of that type from that group.
    
    # there is only one 'red' so remove other colors from the same group
    >>> groups = [[['red', 'blue', 'green']], [['blue', 'green']]]
    >>> only_one_attribute_constraint(groups)
    [[['red']], [['blue', 'green']]]
    """
    flattened = flatten_groups(groups)
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
    """ Remove other attributes from the group in the index.
    
    If attribute does not exist in the index do nothing.
    
    >>> groups = [[['cat', 'dog', 'mouse']], [['dog']]]
    >>> remove_other_attributes(groups, 0, 'cat')
    [[['cat']], [['dog']]]
    >>> remove_other_attributes(groups, 0, 'platypus') # doctest: +IGNORE_EXCEPTION_DETAIL
    [[['cat']], [['dog']]]
    """
    for attributes in groups[index]:
        if attribute in attributes:
            attributes.clear()
            attributes.append(attribute)
    return groups


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
        
        >>> constraints2 = Constraints()
        >>> constraints2.together('old gold', 'snails') # doctest: +ELLIPSIS
        <...Constraints object at ...>
        >>> groups2 = [[['platypus']], [['old gold']]]
        >>> constraints2.constraints[0](groups2) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        UnsolvableException
        """
        def together_test(groups):
            """ Remove attributes that don't adhere to constraints from the groups. """
            indexes1 = set(attribute_indexes(groups, attribute1))
            indexes2 = set(attribute_indexes(groups, attribute2))
            legal_indexes = indexes1.intersection(indexes2)
            wrong_indexes = indexes1.symmetric_difference(indexes2)
            if len(legal_indexes) == 0:
                raise UnsolvableException("No attributes '{0}' and '{1}' found together"
                                           .format(attribute1, attribute2))
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
        UnsolvableException
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
                raise UnsolvableException("No matching adjacent attributes found.")
            wrong_indexes1 = set(range(length)).difference(legal_indexes1)
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
        UnsolvableException
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
                raise UnsolvableException("No matching adjacent attributes found.")
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
        UnsolvableException
        """
        def middle_test(groups):
            middle = len(groups) // 2
            indexes = {middle}
            if len(groups) % 2 == 0:
                indexes.add(middle - 1)
            wrong_indexes = set(range(len(groups))).difference(indexes)
            if len(set(attribute_indexes(groups, attribute)).intersection(indexes)) < 1:
                raise UnsolvableException("No attribute found in the middle.")
            remove_attributes(groups, wrong_indexes, [attribute])
            return groups

        self.constraints.append(middle_test)
        return self

if __name__ == '__main__':
    doctest.testmod()
