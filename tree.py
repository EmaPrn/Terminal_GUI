#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Any, Union, List


class Node(object):
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

    @parent.setter
    def parent(self, parent: Node) -> None:
        if self._parent:
            self._parent.remove_child(self)
        self._parent = parent

    def has_children(self) -> bool:
        return True if len(self._children) > 0 else False

    def add_child(self, child: Node):
        if child not in self._children:
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

    def __iter__(self) -> Node:
        for child in self._children:
            yield child


def _node_iterator(node: Node) -> Union[Node, _node_iterator]:
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

    def _reset_current(self) -> None:
        self._iterator = _node_iterator(self._root)
        self._current = next(self._iterator)

    def set_next(self) -> Node:
        try:
            self._current = next(self._iterator)
        except StopIteration:
            self._reset_current()

        return self._current
