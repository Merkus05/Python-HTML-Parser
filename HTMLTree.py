class HTMLNode():
    def __init__(self, tag, content, parent, attrib):
        self.id = id(self)
        self.tag = tag
        self.content = content
        self.parent = parent
        self.children = []
        self.attrib = attrib
        
    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children.remove(child_node)
    
    def __setitem__(self, key, item):
        self.children[key] = item
        
    def __getitem__(self, key):
        return self.children[key]
    
    def __str__(self):
        if self.parent != None:
            t =  "{%s | Tag: %s; Content: %s; Parent: %s; Attrib: %s}\n" % (self.id, self.tag, self.content, str(self.parent.id) + " " + self.parent.tag, self.attrib)
        else:
            t =  "{%s | Tag: %s; Content: %s; Parent: %s; Attrib: %s}\n" % (self.id, self.tag, self.content, self.parent, self.attrib)
        return t
        
        
class HTMLTree():
    def __init__(self):
        self.root = None
        self.nodes = []
        self.no_parent_tags = ['img', 'link', 'meta', 'br/', 'br', 'area', 'base', 'col', 'input']
    
    def parse_from_string(self, string):
        def first_split(source, char):
            # Check if char is in source
            if char not in source:
                return [source]
            index = source.index(char)
            return [source[0:index].lstrip().rstrip(), source[index + 1: ].lstrip().rstrip().rstrip('"').lstrip('"')]
            
        # Find all tags and filter out comments and doctype
        tags = map(lambda x: x.lstrip().rstrip(), string.split('<'))
        tags = filter(lambda x: x != '' and not x.startswith('!'), tags)

        raw_nodes = []
        
        for _tag in tags:
            # Find content
            content = ""
            if '>' in _tag:
                content = _tag.split('>')[1]

            tag_map = map(lambda x: x.lstrip().rstrip(), _tag.split('>')[0].split(' '))

            # Get tag name and remove it from tag map
            tag = tag_map[0]
            tag_map.remove(tag)

            tag_map = [ first_split(x, '=') for x in tag_map]
            raw_nodes.append([tag, tag_map, content])            

        self.construct_tree(raw_nodes)
    
    def construct_tree(self, raw_nodes):
        cur_parent = None
        #print(raw_nodes)
        for _node in raw_nodes:
            node = self.construct_node(_node)
            
            # Check if node is endnode
            if node.tag.startswith('/'):   
                to_close = node.tag[1:]
                
                # Find tag to close
                for _node in self.nodes[::-1]:
                    if _node.tag == to_close:
                        cur_parent = _node.parent
                        break
                        if cur_parent == None:
                            return
            # Check if node is not able to be a parent object
            elif node.tag in self.no_parent_tags:
                node.parent = cur_parent
                cur_parent.add_child(node)
                self.nodes.append(node)
                
            else:
                if self.root == None:
                    self.root = cur_parent = node
                    continue 
                # Add note to list
                node.parent = cur_parent
                cur_parent.add_child(node)
                cur_parent = node
                self.nodes.append(node)
                
    def construct_node(self, node_data):
        tag = node_data[0]
        content = node_data[2]
        attrib = {}

        for row in node_data[1]:
            if len(row) > 1:
                attrib[row[0]] = row[1]

        return HTMLNode(tag, content, None, attrib)
    
    def parse_from_file(self, file):
        with open(file, 'r') as f:
            self.parse_from_string(f.read())
    
    def find_tag(self, tag):
        return [x for x in self.nodes if x.tag == tag]

    def find_id(self, id):
        f = [x for x in self.nodes if 'id' in x.attrib and x.attrib['id'] == id]
        if len(f) > 0:
            return f[0]
        return None
    
    def find_class(self, _class):
        f = [x for x in self.nodes if 'class' in x.attrib and x.attrib['class'] == _class]
        return f

    def __setitem__(self, key, item):
        self.nodes[key] = item
    
    def __getitem__(self, key):
        return self.nodes[key]

    def __str__(self):
       t = ""
       for n in self.nodes:
           t += str(n)
       return t
        
    def log(self,message):
        with open('log.txt', 'a') as f:
            f.write(message)

