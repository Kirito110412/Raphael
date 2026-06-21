import networkx as nx

class SocialGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def update_relationship(self, person_a: str, person_b: str, context: str):
        self.graph.add_edge(person_a, person_b, context=context)
