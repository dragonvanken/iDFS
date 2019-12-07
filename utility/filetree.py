from termcolor import colored

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

    def addchild(self, child):
        """当children名字不重复时插入成功并返回True，否则返回False"""
        assert self.isFolder
        if not self.child:
            self.child = child
        else:
            cur_note = self.child
            while (cur_note.brother):
                if cur_note.name == child.name:
                    return False
                cur_note = cur_note.brother
            cur_note.setbrother(child)
        child.parent = self
        return True

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

    def __process_path(self, path):
        dir_path = '/'.join(path.split('/')[:-1])
        name = path.split('/')[-1]
        assert name != ""
        return dir_path, name

    def __makePath(self):
        if self.changed:
            for node in self.BFS():
                node.path = node.parent.path+'/'+node.name if node.parent else node.name
            self.changed = False

    def __pprint_tree(self, node, isTmpTop, _prefix="", _last=True):
        if not isTmpTop:
            print(_prefix, "`- " if _last else "|- ", colored(node.name, "green" if node.isFolder else None), sep="")
            _prefix += "   " if _last else "|  "
        child = node.child
        while(child):
            _last = child.brother is None
            self.__pprint_tree(child, False, _prefix, _last)
            child = child.brother

    def __str__(self):
        self.__makePath()
        path_list = []
        for node in self.BFS():
            path_list.append((node.path, node.isFolder))
        return str(path_list)

    def insertNode(self, path, isFolder):
        """当插入成功时返回True"""
        self.changed = True
        dir_path, name = self.__process_path(path)
        parent_node = self.seek(dir_path)
        if parent_node and parent_node.isFolder:
            node = AbstractNode(name, isFolder)
            return parent_node.addchild(node)
        elif dir_path == "":
            node = AbstractNode(name, isFolder)
            self.root.addbrother(node)
        else:
            self.changed = False
            return False

    def removeNode(self, path):
        """当删除成功时返回True"""
        self.changed = True
        dir_path, name = self.__process_path(path)
        parent_node = self.seek(dir_path)
        if parent_node and parent_node.child:
            if parent_node.child.name == name:
                parent_node.child = parent_node.child.brother
                return True
            else:
                pre_node = parent_node.child
                cur_node = parent_node.child.brother
                while (cur_node):
                    if cur_node.name == name:
                        pre_node.brother = cur_node.brother
                        return True
                    else:
                        pre_node = cur_node
                        cur_node = cur_node.brother
        self.changed = False
        return False

    def seek(self, path):
        """返回指定路径上的节点"""
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

    def seriesToPath(self):
        self.__makePath()
        path_list = []
        for node in self.BFS():
            path_list.append((node.path, node.isFolder))
        return path_list

    def getNodes(self, FilePath):
        self.__makePath()
        mynode = self.seek(FilePath)
        assert mynode != None
        path_list = []
        for node in self.BFS(path=mynode):
            path_list.append(node.path)
        return path_list

    def deseriesFromPath(self, path_list):
        self.root = AbstractNode(*path_list.pop(0))
        for path, isFolder in path_list:
            self.insertNode(path, isFolder)
        self.changed = True
        self.__makePath()

    def BFS(self, FilePath=self.root):
        """返回一个按照广度优先搜索顺序抛出节点的生成器"""
        stack = []
        cur_note = FilePath
        while (cur_note or len(stack)):
            if cur_note:
                yield cur_note

                stack.append(cur_note.child)
                cur_note = cur_note.brother
            else:
                cur_note = stack.pop(0)
    def print_tree(self):
        tmp = AbstractNode('tmp', True)
        tmp.child = self.root
        self.__pprint_tree(tmp, True)

FileTree = Tree()

if __name__ == "__main__":
    a = AbstractNode('a',True)
    b = AbstractNode('b',True)
    c = AbstractNode('c',False)
    d = AbstractNode('d',True)
    e = AbstractNode('e',True)
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
    print(new_tr.insertNode('b/d/e/a',True))
    print(new_tr.insertNode('b/d/e/b',False))
    print(new_tr.insertNode('b/d/e/c',True))
    print(new_tr.insertNode('b/d/e/c/asdf',False))
    print(new_tr)
    print(new_tr.removeNode('b/c'))
    print(new_tr)

    new_tr.print_tree()