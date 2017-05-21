import itertools
import time
import doctest

class AttributeNotFoundException(Exception):
    pass

class NoMatchingConstraintException(Exception):
    pass

class Solver:
    """ Can be used to solve logic puzzles such as Einsteins puzzle.
     
    """

    def __init__(self, attributes, constraints):
        # list of attributes: [['att1','att2'],['otheratt1','otheratt2']]
        self.attributes = attributes
        # list of functions
        self.constraints = constraints.constraints
        self.groups = []
        # initialize with groups containing all attributes
        self.groups = [attributes] * len(attributes)

    def remove_attribute(self, index, attribute):
        """ Remove attribute from the group in the specified index."""
        for attributes in self.groups[index]:
            if attribute in attributes:
                attributes.remove(attribute)
                break

    def solve(self):
        """ Return solution. """
        pass

    # together tests 1 group at a time:
    # if both att1 and att2 present, do nothing
    # else remove the lone attribute

    # middle   tests 1 group at a time
    # if
    # adjacent tests 2 ajacent at a time
    # ordert   tests 2 ajacent at a time

    # if there are no groups passing the constrain throw exception/;q

    # todo
    def apply_constraint(self, constraint):
        """ Call the constrain with group. Remove attributes the constrain indicates."""
        constrain(self.groups)

def attribute_indexes(groups, attribute):
    """ Return indexes of groups that contain the attribute."""
    indexes = []
    for group in enumerate(groups):
        for attributes in group[1]:
            if attribute in attributes:
                indexes.append(group[0])
    return indexes


class Constraints:
    """ Defines constraints for solver.
    Data attribute 'constraints' contains a list of functions that
    can be used to test if a a list of groups fulfills the constraints.
    Ordering of the group list matters: first item in the list is the 
    leftmost group and last is the rightmost.
    
    If constraints are defined for attributes that don't exist in
    groups that are tested AttributeNotFoundException will be thrown.
    """

    def __init__(self, group_count):
        """ Initialize constraints with a number of groups."""

        self.constraints = []
        self.groupCount = group_count

    def together(self, attribute1, attribute2):
        """ Add constraint: Attributes belong in the same group.
        
        >>> import solving
        >>> groups = [[['blue'],['cat','dog']],[['red','blue'],['cat','dog']]]
        >>> constraints = solving.Constraints(2) 
        >>> constraints.together('red','cat') # doctest: +ELLIPSIS
        <solving.Constraints object at ...>
        >>> constraints.constraints[0](groups)
        {0}
        """
        def together_test(groups):
            """ Return list of indexes that have one but not the other attribute. """
            indexes1 = set(attribute_indexes(groups, attribute1))
            indexes2 = set(attribute_indexes(groups, attribute2))
            intersection = indexes1.intersection(indexes2)
            if(len(intersection) == 0):
                raise NoMatchingConstraintException("Attributes were not found together.")
            return indexes1.symmetric_difference(indexes2)

        self.constraints.append(together_test)
        return self

    # tonow: tama seka muut testit kuntoon
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

if __name__ == '__main__':
    doctest.testmod()

# a,s,d   1,2,3   i,o,p
# attributes: ([a,s,d],[1,2,3],[i,o,p])
# groups complete:  ([[a],[1],[i]],[[s],[2],[o]],[[d],[3],[p]])
# groups incomplete: (([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]),([a,s,d],[1,2,3],[i,o,p]))

# kaikki mahdollisuudet on groupissa
# ota groupeista pois attribuutteja constrainttien perusteella:
#   muuta constraintit palauttamaan listan vaarista indekseista tai
#   poistamaan attribuutit jotka eivat vastaa constraintteja