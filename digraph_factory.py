import svgwrite
from graphviz import Digraph

class DummyDigraph:
    def __init__(self):
        pass

    def node(self, node_id, label=''):
        pass

    def edge(self, parent_id, child_id):
        pass
    
    def render(self, path, format='svg', cleanup=False):
        if format != 'svg':
            raise ValueError("Only 'svg' format is supported for DummyDigraph.")
        
        path = path + ".svg"
        
        # Create an SVG drawing
        dwg = svgwrite.Drawing(filename=path, profile='tiny')
        
        # Add a string to the SVG
        dwg.add(dwg.text('Tree is too big to keep', insert=(10, 20)))
        
        # Save the SVG file
        dwg.save()

class Digraph_factory:
    def __init__(self):
        pass

    def create_digraph(self, algorithm, k):
        if algorithm == 'minimax':
            if k <= 4:
                return Digraph()
        elif algorithm == 'alpha-beta':
            if k <= 5:
                return Digraph()
        elif algorithm == 'expectiminimax':
            if k <= 4:
                return Digraph()
        return DummyDigraph()
        
