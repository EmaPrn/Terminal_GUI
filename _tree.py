#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These annotations allow type hints, even to reference an object inside its own class

# Imports used for type hints
from __future__ import annotations
from typing import Any, Union, List


class Node(object):
    """Class representing a node of a tree.
    It yields its children when iterated upon.

    Attributes:
        name (str): The identifier of the node. A tree must ensure its uniqueness.
        payload (Any): The object carried by the node. It can be anything.
    """
    def __init__(self, name: str, payload: Any = None):
        self._name: str = name
        self._payload: Any = payload
        self._parent: Union[Node, None] = None
        self._children: List[Node] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def payload(self) -> Any:
        return self._payload

    @property
    def parent(self) -> Node:
        return self._parent

    # The use of a property setter ensures that if the parent is changed, the old parent will be modified accordingly.
    # Removing the node from the children list of the former parent.
    @parent.setter
    def parent(self, parent: Node) -> None:
        if self._parent:
            self._parent.remove_child(self)
        self._parent = parent

    def has_children(self) -> bool:
        return True if len(self._children) > 0 else False

    # The check ensure the uniqueness of the child name among its potential brothers before the insertion.
    def add_child(self, child: Node):
        for existing_child in self._children:
            if child.name == existing_child.name:
                raise ValueError("The node already has a child with the same name: " + child.name)

        self._children.append(child)
        child.parent = self

    def remove_child(self, child: Node):
        if child in self._children:
            self._children.remove(child)

    def get_child(self, child_name: str) -> Node:
        for child in self._children:
            if child.name == child_name:
                return child

    def __str__(self):
        return self._name

    # The node class is iterable.
    def __iter__(self) -> Node:
        for child in self._children:
            yield child


def _node_iterator(node: Node) -> Union[Node, _node_iterator]:
    """A generator that takes a Node as input and yields (one-by-one) all the leaves
        of the subtree originated from the node.

    Parameters:
        node (Node): A starting node. It defines the subtree for the research of leaves.

    Returns:
        The next available leaf of the subtree.
    """
    if not node.has_children():
        yield node
    else:
        for child in node:
            iterator = _node_iterator(child)
            stop = False
            while not stop:
                try:
                    yield next(iterator)
                except StopIteration:
                    stop = True


class Tree(object):
    """Class representing a tree.
    It can be seen as a "Leaves' Iterator" as it allows to iterate upon the leaves of the tree (nodes without children)
    by calling the method

    Attributes:
        _root (str | Node): The root node of the tree. If a string is provided the constructor will initialise it to
                            a new node with the provided name. If the root payload (optional) parameter is passed, it
                            will be the payload of the newly created root node.
        _current (Node): The current node. I.e. the last node yielded by the set_next() method.
    """
    def __init__(self, root: Union[str, Node] = "root", root_payload: Any = None):
        if isinstance(root, str):
            self._root: Node = Node(root, root_payload)
        elif isinstance(root, Node):
            self._root: Node = root
        self._current: Node = self._root
        self._iterator: _node_iterator = _node_iterator(self._root)

    @property
    def root(self) -> Node:
        return self._root

    @property
    def current(self) -> Node:
        return self._current

    def get_node(self, name: str, node: Node = None) -> Union[None, Node]:
        """Method looking for a node in the tree, given its name.

        Parameters:
            name (str): The name of the node to look for.
            node (Node): (Optional) The starting node for the research. Used to call the method in a recursive manner.
                         If not specified the research will start at the root node.

        Returns:
            The searched node if exists, None otherwise.

        """
        if not node:
            node: Node = self._root

        if node.name == name:
            return node
        else:
            for child in node:
                found: Node = self.get_node(name, child)
                if found:
                    return found
        return None

    def reset_current(self) -> None:
        """Resets the current leaf to the first one of the sequence.

        Note:
            If any node of the tree is modified this method MUST be called before any call of the set_next() method.

        """
        self._iterator = _node_iterator(self._root)
        self._current = next(self._iterator)

    def set_next(self) -> Node:
        """Yields the next leaf of the sequence

        Returns:
            The next leaf of the sequence, if the current leaf is the last then it loops back to the first.

        """
        try:
            self._current = next(self._iterator)
        except StopIteration:
            self.reset_current()

        return self._current
