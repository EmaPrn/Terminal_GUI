def _node_iterator(node):
    if not node.has_children():
        yield node
    else:
        for child in node.children:
            iterator = _node_iterator(child)
            stop = False
            while not stop:
                try:
                    yield next(iterator)
                except StopIteration:
                    stop = True


class Node:
    def __init__(self, name, payload=None):
        self._name = name
        self._payload = payload
        self._parent = None
        self._children = []

    @property
    def name(self):
        return self._name

    @property
    def payload(self):
        return self._payload

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent:
            self._parent.remove_child(self)
        self._parent = parent

    @property
    def children(self):
        return self._children

    @property
    def children_payload(self):
        return [child.payload for child in self._children]

    def has_children(self):
        return True if len(self._children) > 0 else False

    #TODO: Handle type of child and errors
    def add_child(self, child):
        if child not in self._children:
            self._children.append(child)
            child.parent = self

    def remove_child(self, child):
        if child in self._children:
            self._children.remove(child)

    def get_child(self, child_name):
        for child in self._children:
            if child.name == child_name:
                return child

    def __str__(self):
        return self._name


class Tree:
    def __init__(self, root="root", root_payload=None):
        if isinstance(root, str):
            self._root = Node(root, root_payload)
        elif isinstance(root, Node):
            self._root = root
        self._current = self._root
        self._iterator = _node_iterator(self._root)

    @property
    def root(self):
        return self._root

    @property
    def current(self):
        return self._current

    def get_node(self, name, node=None):
        if not node:
            node = self._root

        if node.name == name:
            return node
        else:
            for child in node.children:
                found = self.get_node(name, child)
                if found:
                    return found
        return None

    def _reset_current(self):
        self._iterator = _node_iterator(self._root)
        self._current = next(self._iterator)

    def set_next(self):
        try:
            self._current = next(self._iterator)
        except StopIteration:
            self._reset_current()

        return self._current