class HTMLNode():
    def __init__(self, tag, content, parent, attrib):
        """Constructor of HTMLNode. Represents a single HTML element and all its content.

            Args:
                tag     (String)    : HTML tag of element. 
                content (String)    : Content of element. (E.g. text inside a <h1></h1>)
                parent  (String)    : Parent HTMLNode.
                attrib  (Dicc)      : Dictionary cotaining all extra tags inside the HTML tag. (E.g. width, height etc.)
        """
        self.id = id(self)
        self.tag = tag
        self.content = content
        self.parent = parent
        self.children = []
        self.attrib = attrib
        
    def add_child(self, child_node):
        """Method to add child to HTMLNode.

            Args:
                child_node (HTMLNode) : New child.
        """
        self.children.append(child_node)

    def remove_child(self, child_node):
        """Method to remove child from HTMLNode.

            Args:
                child_node (HTMLNode) : Node to remove.
        """
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
        """Constructor of HTMLTree class.

            Usage:
                my_tree = HTMLTree()
        """
        self.root = None
        self.nodes = []
        self.no_parent_tags = ['img', 'link', 'meta', 'br/', 'br', 'area', 'base', 'col', 'input']
    
    def parse_from_string(self, string):
        """Method to parse HTML from given String.

            Args:
                string (String): String to parse from.
            
            Usage:
                Obj.parse_from_string(<html string>)
        """
        def first_split(source, char):
            # Check if char is in source
            if char not in source:
                return [source]
            index = source.index(char)
            return [source[0:index].lstrip().rstrip(), source[index + 1: ].lstrip().rstrip().rstrip('"').lstrip('"')]
            
        # Find all tags and filter out comments and doctype
        tags = list(map(lambda x: x.lstrip().rstrip(), string.split('<')))
        tags = list(filter(lambda x: x != '' and not x.startswith('!'), tags))

        raw_nodes = []
        
        for _tag in tags:
            # Find content
            content = ""
            if '>' in _tag:
                content = _tag.split('>')[1]

            tag_map = list(map(lambda x: x.lstrip().rstrip(), _tag.split('>')[0].split(' ')))

            # Get tag name and remove it from tag map
            tag = tag_map[0]
            tag_map.remove(tag)

            tag_map = [ first_split(x, '=') for x in tag_map]
            raw_nodes.append([tag, tag_map, content])            

        self.construct_tree(raw_nodes)
    
    def construct_tree(self, raw_nodes):
        """Constructs DOM tree based on previous parsed string.
           Is automaticly called by parse functions.

           Args:
                raw_nodes (List) : List of lists where each sublist contains information about one node.
        """

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
        """Method to construct node based on a raw_node item.

            Args:
                node_data (List) : List containing infos about node. (tag, tag_map, content).abs
            
            Returns:
                HTMLNode : HTMLNode based on given node_data.
        """
        tag = node_data[0]
        content = node_data[2]
        attrib = {}

        for row in node_data[1]:
            if len(row) > 1:
                attrib[row[0]] = row[1]

        return HTMLNode(tag, content, None, attrib)
    
    def parse_from_file(self, file):
        """Method to read html from file. After it finished reading the content is parsed as a string.

            Args:
                file (String): Filename or path to file.

            Usage:
                OBJ.parse_from_file(<MyHtmlFile>)
        """
        with open(file, 'r') as f:
            self.parse_from_string(f.read())
    
    def find_tag(self, tag):
        """Method to find HTML elements based on their tag.

            Args:
                tag (String) : Tag to look for.
            
            Returns:
                List : Contains all found HTMLNodes with given tag.
        """
        return [x for x in self.nodes if x.tag == tag]

    def find_id(self, id):
        """Method to find HTML element with given id. 
           If multiple elements have the same id (should not happen in valid HTML),
           only the first is returned.

            Args:
                id (String) : id to look for.
            
            Returns:
                HTMLNode : If node with given id is found else...
                None
        """
        f = [x for x in self.nodes if 'id' in x.attrib and x.attrib['id'] == id]
        if len(f) > 0:
            return f[0]
        return None
    
    def find_class(self, _class):
        """Method to find all HTML elements with given class.

            Args:
                class (String) : Name of class to look for.
            
            Returns:
                List : List containing all found HTMLNodes.
        
        """
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