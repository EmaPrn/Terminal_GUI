class _Node:
    def __init__(self, name, payload=None):
        self._name = name
        self._payload = payload
        self._parent = None
        self._children = []
        self.is_active = False

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

    def __iter__(self):
        if not self.has_children():
            yield self
        else:
            for child in self._children:
                for node in child:
                    yield node


class Tree:
    def __init__(self, root="root", root_payload=None):
        if isinstance(root, str):
            self._root = _Node(root, root_payload)
        elif isinstance(root, _Node):
            self._root = root
        self._current = self._root
        self._iterator = iter(self._root)

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

    def remove_node(self, node_name, refresh=True):
        node = self.get_node(node_name)
        if node:
            node.parent.remove_child(node)
            if refresh:
                self.activate_first()

    def add_node(self, parent_name, child_name, child_payload=None, refresh=True):
        if not self.get_node(child_name):
            child = _Node(child_name, child_payload)
            self.get_node(parent_name).add_child(child)
            if refresh:
                self.activate_first()

    def activate_first(self):
        self._iterator = iter(self._root)
        self._current = next(self._iterator)

    def activate_next(self):
        self._deactivate_current()

        try:
            self._current = next(self._iterator)
        except StopIteration:
            self.activate_first()

        node = self._current
        while node:
            node.is_active = True
            node = node.parent

    def _deactivate_current(self):
        node = self._current
        while node:
            node.is_active = False
            node = node.parent


tree = Tree("A")
tree.add_node("A", "B")
tree.add_node("A", "C")
tree.add_node("C", "D")
tree.add_node("C", "E")
tree.add_node("E", "F")

