import itertools
import time

class Solver:
    """ Can be used to solve logic puzzles such as Einsteins puzzle.
    
    """

    def __init__(self, attributes, constraints):
        """ Initialize solver.
        
        :param attributes: List of attribute groups. Each group is a
         collection of attributes of the same type.
        :param constraints: Constraints object
        """
        self.attributes = attributes
        self.constraints = constraints.constraints

    def check(self, group_set):
        """ Check if a set of groups passes all constraints."""
        for constraint in self.constraints:
            if not constraint(group_set):
                return False
        return True

    def solve(self):
        """ Return generator that produces all groups that pass the 
        constraints. Returned tuples contains correct groups ordered 
        so leftmost group is the first group in the list and rightmost
        is the last and so on. 
        """
        search_space = all_groupings(self.attributes)
        # Stop iteration early because 25 billion is too much
        n = 10000000
        for _, group_set in zip(range(n), search_space):
            if(self.check(group_set)):
                yield group_set

def remove_used(group, attributes):
    """" Return attributes that are not in the group."""
    ret = [[subelt for subelt in elt if subelt not in group]
            for elt in attributes]
    return ret


def all_groupings(attributes):
    """ Return generator that generates all possible groupings
    containing an item from each list. Each item is used exactly once
    in each grouping. Number of groups is the length of sublist.
    """
    if len(attributes[0]) == 1:
        yield (tuple(x[0] for x in attributes),)
        return
    # all permutations from the attributes
    search_groups = itertools.product(*attributes)
    for group in search_groups:
        # complete set of groups containing all attributes
        group_sets = ((group, *rest) for rest in
                      all_groupings(remove_used(group, attributes)))
        for set in group_sets:
            yield set


class Constraints:
    """ Defines constraints for solver.
    Data attribute 'constraints' contains a list of functions that that
    can be used to test if a a list of groups fulfills the constraints.
    Ordering of the group list matters: first item in the list is the 
    leftmost group and last is the rightmost.
    
    If constraints are defined for attributes that don't exist in
    groups that are tested AttributeNotFoundException will be thrown
    while testing.
    """

    def __init__(self, group_count):
        """ Initialize constraints with a number of groups."""

        self.constraints = []
        self.groupCount = group_count

    def together(self, attribute1, attribute2):
        """ Add constraint: Attributes belong in the same group."""
        def together_test(groups):
            return attribute_group_index(groups, attribute1) == \
                   attribute_group_index(groups, attribute2)

        self.constraints.append(together_test)
        return self

    def adjacent(self, attribute1, attribute2):
        """ Add constraint: Attributes are next to each other in any order."""

        def adjacent_test(groups):
            index1 = attribute_group_index(groups, attribute1)
            index2 = attribute_group_index(groups, attribute2)
            return abs(index1 - index2) == 1

        self.constraints.append(adjacent_test)
        return self

    def order(self, left_attribute, right_attribute):
        """ Add constraint: First attribute is adjacent and left of the second."""

        def order_test(groups):
            index1 = attribute_group_index(groups, left_attribute)
            index2 = attribute_group_index(groups, right_attribute)
            return index2 - index1 == 1

        self.constraints.append(order_test)
        return self

    def middle(self, attribute):
        """ Add constraint: Attribute is in the middle group. If number
        of groups is even the attribute may be in any of the 2 middle
        groups.
        """

        def middle_test(groups):
            middle = self.groupCount // 2
            index = attribute_group_index(groups, attribute)
            if self.groupCount % 2 == 0:
                return middle == index or middle - index == 1
            else:
                return middle == index

        self.constraints.append(middle_test)
        return self


class AttributeNotFoundException(Exception):
    pass


def attribute_group_index(groups, attribute):
    """ Return index of the group containing the attribute.
    Return -1 if attribute is not found in any of the groups.
    If attribute is not found in groups throw Group
    """
    # return the attribute itself if it's number
    # because it already is the index
    if(isinstance(attribute, int)):
        return attribute
    for group in enumerate(groups):
        if attribute in group[1]:
            return group[0]
    raise AttributeNotFoundException(
        'Attribute: %s not found in groups: %s' % (attribute, groups))
