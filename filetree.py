import os
import json

class AbstractNode:
    def __init__(self, name):
        self.name = name
        self.iswrite = True
        self.child = None
        self.parent = None
        self.path = None
        self.brother = None

    def setname(self, name):
        self.name = name

    def setbrother(self, brother):
        self.brother = brother
        self.brother.parent = self.parent

    def addchild(self, child):
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

    def setroot(self, root):
        self.root = root
        self.root.path = self.root.name

    def seek(self, path):
        dirnames = path.split('/')[:-1]
        filename = path.split('/')[-1]

        cur_note = self.root
        i = 0
        while(i < len(dirnames)):
            if cur_note.name == dirnames[i]:
                cur_note = cur_note.child
            elif cur_note.brother != None:
                cur_note = cur_note.brother
                i -= 1
            else:
                return None
            i += 1
        while(cur_note):
            if cur_note.name == filename:
                return cur_note
            else:
                cur_note = cur_note.brother

        return None

    def makePath(self):
        for note in self.BFS():
            note.path = note.parent.path+'/'+note.name if note.parent else note.name

    def seriesToPath(self):
        path_list = []
        for note in self.BFS():
            path_list.append(note.path)
        return path_list

    def __str__(self):
        name_list = []
        for node in self.BFS():
            name_list.append(node.name)
        return str(name_list)

    def deseriesFromPath(self, path_list):
        self.root = AbstractNode(path_list.pop(0))
        for path in path_list:
            dir_path = '/'.join(path.split('/')[:-1])
            name = path.split('/')[-1]
            note = AbstractNode(name)
            parent_note = self.seek(dir_path)
            if parent_note:
                parent_note.addchild(note)
            else:
                self.root.addbrother(note)

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

if __name__ == "__main__":
    a = AbstractNode('a')
    b = AbstractNode('b')
    c = AbstractNode('c')
    d = AbstractNode('d')
    e = AbstractNode('e')
    a.setbrother(b)
    b.addchild(c)
    c.setbrother(d)
    d.addchild(e)

    tr = Tree()
    tr.setroot(a)
    tr.makePath()
    print(tr.seriesToPath())

    new_tr = Tree()
    new_tr.deseriesFromPath(tr.seriesToPath())
    print(new_tr)
