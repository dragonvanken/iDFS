class AbstractNode:
    def __init__(self, name, isFolder):
        self.name = name
        self.iswrite = True
        self.child = None
        self.parent = None
        self.path = None
        self.brother = None
        self.isFolder = isFolder

    def setname(self, name):
        self.name = name

    def setbrother(self, brother):
        self.brother = brother
        self.brother.parent = self.parent

    def addchild(self, child) :
        assert self.isFolder
        if not self.child:
            self.child = child
        else:
            cur_note = self.child
            while (cur_note.brother):
                cur_note = cur_note.brother
            cur_note.setbrother(child)
        child.parent = self

    def addbrother(self, brother):
        if not self.brother:
            self.setbrother(brother)
        else:
            cur_note = self.brother
            while (cur_note.brother):
                cur_note = cur_note.brother
            cur_note.setbrother(brother)

    def getname(self):
        return self.name

    def getbrother(self):
        return self.brother


class Tree:
    def __init__(self):
        self.root = None
        self.changed = False

    def setroot(self, root):
        self.root = root
        self.root.path = self.root.name

        self.changed = True
        self.__makePath()

    def insertNode(self, path, isFolder):
        """Return True if path is valid, otherwise False will be returned."""
        self.changed = True
        dir_path = '/'.join(path.split('/')[:-1])
        name = path.split('/')[-1]
        parent_node = self.seek(dir_path)
        if parent_node and parent_node.isFolder:
            node = AbstractNode(name, isFolder)
            parent_node.addchild(node)
            return True
        elif dir_path == "":
            node = AbstractNode(name, isFolder)
            self.root.addbrother(node)
        else:
            self.changed = False
            return False

    def seek(self, path):
        dirnames = path.split('/')[:-1]
        filename = path.split('/')[-1]

        cur_node = self.root
        i = 0
        while(i < len(dirnames)):
            if cur_node and cur_node.name == dirnames[i]:
                cur_node = cur_node.child
            elif cur_node and cur_node.brother != None:
                cur_node = cur_node.brother
                i -= 1
            else:
                return None
            i += 1
        while(cur_node):
            if cur_node.name == filename:
                return cur_node
            else:
                cur_node = cur_node.brother

        return None

    def __makePath(self):
        if self.changed:
            for note in self.BFS():
                note.path = note.parent.path+'/'+note.name if note.parent else note.name
            self.changed = False

    def seriesToPath(self):
        self.__makePath()
        path_list = []
        for node in self.BFS():
            path_list.append((node.path, node.isFolder))
        return path_list

    def __str__(self):
        self.__makePath()
        name_list = []
        for node in self.BFS():
            name_list.append((node.name, node.isFolder))
        return str(name_list)

    def deseriesFromPath(self, path_list):
        self.root = AbstractNode(*path_list.pop(0))
        for path, isFolder in path_list:
            self.insertNode(path, isFolder)
        self.__makePath()

    def BFS(self):
        stack = []
        cur_note = self.root
        while (cur_note or len(stack)):
            if cur_note:
                yield cur_note

                stack.append(cur_note.child)
                cur_note = cur_note.brother
            else:
                cur_note = stack.pop(0)


FileTree = Tree()


if __name__ == "__main__":
    a = AbstractNode('a',True)
    b = AbstractNode('b',True)
    c = AbstractNode('c',False)
    d = AbstractNode('d',True)
    e = AbstractNode('e',False)
    a.setbrother(b)
    b.addchild(c)
    c.setbrother(d)
    d.addchild(e)

    tr = Tree()
    tr.setroot(a)
    print(tr.seriesToPath())

    new_tr = Tree()
    new_tr.deseriesFromPath(tr.seriesToPath())
    print(new_tr)