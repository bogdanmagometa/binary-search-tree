"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_repr = ""
            if node != None:
                str_repr += recurse(node.right, level + 1)
                str_repr += "| " * level
                str_repr += str(node.data) + "\n"
                str_repr += recurse(node.left, level + 1)
            return str_repr

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
                # End of recurse
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int

        >>> bst = LinkedBST()
        >>> bst.height()
        0
        >>> bst.add(1)
        >>> bst.height()
        0
        >>> bst.add(2)
        >>> bst.height()
        1
        >>> bst.add(0)
        >>> bst.height()
        1
        >>> bst.add(0)
        >>> bst.height()
        2
        '''

        def height1(top):
            '''
            Helper function
            :param top: BSTNode
            :return: int
            '''
            # base case
            if top.left is None and top.right is None:
                return 0

            # recursive cases
            maximum = 0
            for child in top.left, top.right:
                if child is not None:
                    child_height = height1(child)
                    if child_height > maximum:
                        maximum = child_height

            return maximum + 1

        if self._root is None:
            return 0

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return: bool
        '''

        return self.height() < (2*log(self._size + 1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low: int
        :param high: int
        :return: list of items

        >>> bst = LinkedBST()
        >>> bst.add(1)
        >>> bst.add(2)
        >>> bst.add(3)
        >>> bst.range_find(1, 3)
        [1, 2, 3]
        >>> bst.rebalance()
        >>> bst.range_find(1, 3)
        [1, 2, 3]
        >>> bst.add(4)
        >>> bst.add(5)
        >>> bst.range_find(3, 4)
        [3, 4]
        >>> bst.rebalance()
        >>> bst.add(1200)
        >>> bst.add(120)
        >>> bst.range_find(4, 200)
        [4, 5, 120]
        '''

        def recurse(node, items_range):
            if node is not None:
                if node.data > low:
                    recurse(node.left, items_range)
                if low <= node.data <= high:
                    items_range.append(node.data)
                if node.data <= high:
                    recurse(node.right, items_range)

        needed_items = []

        recurse(self._root, needed_items)

        return needed_items

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:

        >>> bst = LinkedBST()
        >>> bst.add(1)
        >>> bst.add(2)
        >>> bst.add(3)
        >>> bst.height()
        2
        >>> bst.rebalance()
        >>> bst.height()
        1
        >>> bst.add(4)
        >>> bst.add(5)
        >>> bst.height()
        3
        >>> bst.rebalance()
        >>> bst.height()
        2
        '''

        # helper method for adding elements from sorted list to BST
        def recurse(bst, sorted_list, start, end):
            middle = (start + end + 1) // 2
            bst.add(sorted_list[middle])

            if (middle - 1) >= start:
                recurse(bst, sorted_list, start, middle - 1)
            if end >= (middle + 1):
                recurse(bst, sorted_list, middle + 1, end)

        lyst = list(self.inorder())
        self.clear()

        recurse(self, lyst, 0, len(lyst)-1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item: the item of which to find the successor
        :type item: anything comparable with items of tree
        :return: the item from the tree coming after the passed in one
        :rtype: anything comparable

        >>> bst = LinkedBST()
        >>> bst.add(1)
        >>> bst.add(2)
        >>> bst.add(3)
        >>> bst.successor(2)
        3
        >>> bst.rebalance()
        >>> bst.successor(1)
        2
        >>> bst.add(4)
        >>> bst.add(5)
        >>> bst.successor(4)
        5
        >>> bst.rebalance()
        >>> bst.successor(3)
        4
        >>> bst.successor(5) is None
        True
        >>> bst.successor(-1000)
        1
        """

        last_left = None
        walk = self._root

        # finding the needed item
        while walk is not None and walk.data != item:
            if item < walk.data:
                last_left = walk
                walk = walk.left
            else:
                walk = walk.right

        if walk is None or walk.right is None:
            # the successor is above or doesn't exist in the tree.
            if last_left is None:
                return None
            return last_left.data

        # the successor is to the right of the found item
        walk = walk.right
        while walk.left is not None:
            walk = walk.left
        return walk.data

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item: the item of which to find the predecessor
        :type item: anything comparable with items of tree
        :return: the item from the tree coming before the passed in one
        :rtype: anything comparable

        >>> bst = LinkedBST()
        >>> bst.add(1)
        >>> bst.add(2)
        >>> bst.add(3)
        >>> bst.predecessor(2)
        1
        >>> bst.rebalance()
        >>> bst.predecessor(3)
        2
        >>> bst.add(4)
        >>> bst.add(5)
        >>> bst.predecessor(4)
        3
        >>> bst.rebalance()
        >>> bst.predecessor(3)
        2
        >>> bst.predecessor(1) is None
        True
        >>> bst.predecessor(100000)
        5
        """

        last_right = None
        walk = self._root

        # finding the needed item
        while walk is not None and walk.data != item:
            if item < walk.data:
                walk = walk.left
            else:
                last_right = walk
                walk = walk.right

        if walk is None or walk.left is None:
            # the successor is above or doesn't exist in the tree.
            if last_right is None:
                return None
            return last_right.data

        # the successor is to the left of the found item
        walk = walk.left
        while walk.right is not None:
            walk = walk.right
        return walk.data

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
