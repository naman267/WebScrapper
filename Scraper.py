import re
from urllib.request import urlopen
from Info import Info
from Tag import Tag

def isVoid(str):
    if(str == "area" or str == "base" or str == "br" or str == "col" or str == "command"
    or str == "embed" or str == "img" or str == "input" or str == "input" or str == "keygen"
    or str == "link" or str == "meta" or str == "param" or str == "source" or str == "track" or str == "wbr"
    or str == "<!--"):
        return True
    else:
        return False

class Scraper:
    def __init__(self, input):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        self.data = input
        if(re.match(regex, input)):
            self.getData(self.data)

        self.data = self.data.replace("\\r", "")
        self.data = self.data.replace("\\n", "")

    def getData(self, url):
        self.data = str(urlopen(url).read())

    def getSubstring(self, lr):
        return self.data[lr[0]:lr[1]]

    def findOpening(self, _tag = None, _class = None, _id = None):
        output = []

        if(_tag == None and _class == None and _id == None):
            return Exception("No parameter provided")
        
        elif(_tag != None and _class != None and _id != None):
            rxp1 = '<' + _tag + '[^>]*?class="' + _class + '"[^>]*?id="' + _id + '".*?>'
            rxp2 = '<' + _tag + '[^>]*?id="' + _id + '"[^>]*?class="' + _class + '".*?>'
            for match in re.finditer('|'.join([rxp1, rxp2]), self.data):
                output.append(match.span())

        elif(_tag != None and _class != None):
            rxp = '<' + _tag + '[^>]*?class="' + _class + '".*?>'
            for match in re.finditer(rxp, self.data):
                output.append(match.span())

        elif(_tag != None and _id != None):
            rxp = '<' + _tag + '[^>]*?id="' + _id + '".*?>'
            for match in re.finditer(rxp, self.data):
                output.append(match.span())

        elif(_class != None and _id != None):
            rxp1 = '<[^>]*?class="' + _class + '"[^>]*?id="' + _id + '".*?>'
            rxp2 = '<[^>]*?id="' + _id + '"[^>]*?class="' + _class + '".*?>'
            for match in re.finditer('|'.join([rxp1, rxp2]), self.data):
                output.append(match.span())
            
        elif(_tag != None):
            rxp1 = "<" + _tag + " .*?>"
            rxp2 = "<" + _tag + ">"
            for match in re.finditer('|'.join([rxp1, rxp2]), self.data):
                output.append(match.span())

        elif(_class != None):
            rxp = '<[^>]*?class="' + _class + '".*?>'
            for match in re.finditer(rxp, self.data):
                output.append(match.span())

        elif(_id != None):
            rxp = '<[^>]*?id="' + _id + '".*?>'
            for match in re.finditer(rxp, self.data):
                output.append(match.span())
        
        return output
    
    def findEnd(self, l, str):
        tag = ""
        i = l + 1
        while(i < len(str) and str[i] != ' ' and str[i] != '>'):
            tag += str[i]
            i += 1
    
        if(isVoid(tag)):
            while(i < len(str) and str[i] != '>'):
                i += 1
            return i

        else:
            stack = [tag]
            i += 1
            tag = ""
            flag = False
            while(i < len(str)):
                if(flag == True and (str[i] == ' ' or str[i] == '>')):
                    flag = False
                    if(isVoid(tag)):
                        tag = ""
                        continue
                    if(tag[0] == '/'):
                        stack.pop()
                    else:
                        stack.append(tag)
                    tag = ""
                elif(flag == True):
                    tag += str[i]
                elif(str[i] == '<'):
                    flag = True

                if(len(stack) == 0):
                    return i
                i += 1

        return -1

    def find(self, _tag = None, _class = None, _id = None):
        output = self.findOpening(_tag = _tag, _class = _class, _id = _id)
        ans = []
        for x in output:
            y = self.findEnd(x[0], self.data)
            ans.append((x[0], y + 1))
        return ans

    def parse(self, str, par = None):
        if(len(str) == 0):
            return None
        i = 0
        strings = []
        tags = []
        cur = ""
        while(i < len(str)):
            while(i < len(str) and str[i] != '<'):
                cur += str[i]
                i += 1
        
            if(i == len(str)):
                break

            if(cur != ""):
                cur = cur.lstrip()
                cur = cur.rstrip()
                if(len(cur) != 0):
                    strings.append(cur)

            cur = ""
            j = self.findEnd(i, str)
            l = i + 1
            r = j 
            props = ""
            while(l < r and str[l] != '>'):
                props += str[l]
                l += 1

            while(r > l and str[r] != '<'):
                r -= 1

            k = 0
            t = ""
            while(k < len(props) and props[k] != ' ' and props[k] != '>'):
                t += props[k]
                k += 1

            tags.append(Tag(props, par, str[i:j + 1], self.parse(str[l+1:r], t)))
            i = j + 1
    
        cur = cur.lstrip()
        cur = cur.rstrip()
        if(cur != ""):
            strings.append(cur)

        if(len(strings) == 0 and len(tags) == 1):
            return tags[0]
        return Info(strings, tags, par)
                    