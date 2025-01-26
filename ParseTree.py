import graphviz

class ParseTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class ParseTree:
    def __init__(self, start_symbol):
        self.root = ParseTreeNode(start_symbol)

    def add_production(self, parent_node, production):
        for symbol in production:
            child_node = ParseTreeNode(symbol)
            parent_node.add_child(child_node)

    def visualize(self, output_file="parse_tree", format="png"):
        dot = graphviz.Digraph()
        self._add_nodes(dot, self.root)
        dot.render(output_file, format=format, cleanup=True)
        print(f"Parse tree saved to {output_file}.{format}")

    def _add_nodes(self, dot, node, parent_id=None):
        node_id = id(node)
        dot.node(str(node_id), node.value)
        if parent_id is not None:
            dot.edge(str(parent_id), str(node_id))
        for child in node.children:
            self._add_nodes(dot, child, node_id)

    def build_from_productions(self, productions):
        current_nodes = {self.root.value: self.root}
        for production in productions:
            left, right = production.split(" -> ")
            right_symbols = right.split()
            if left in current_nodes:
                parent_node = current_nodes[left]
                del current_nodes[left]
                for symbol in right_symbols:
                    child_node = ParseTreeNode(symbol)
                    parent_node.add_child(child_node)
                    if symbol not in ["number", "identifier", "string", "+", "-", "*", "=", "<", ">", "<=", ">=", "!=", ";", "cin", "cout", "return", "while", "(", ")", "{", "}"]:
                        current_nodes[symbol] = child_node
