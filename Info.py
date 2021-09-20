import re

class Info:
    def __init__(self, strings, tags, parent):
        self.strings = strings
        self.tags = tags
        self.parent = parent

    def display(self, tabs = 0):
        print("\t" * tabs , "parent: ", self.parent)
        print("\t" * tabs , "text: ",self.strings)
        print("\t" * tabs , "tags: ", end=" ")
        if(len(self.tags) == 0):
            print("None")
        else:
            print()
            for tag in self.tags:
                tag.display(tabs + 1)

    def getString(self):
        return self.strings

    def find(self, _tag = None, _id = None, _class = None):
        for tag in self.tags:
            rem = tag.find(_tag, _id, _class)
            if(rem != None):
                return rem
        return None
        
