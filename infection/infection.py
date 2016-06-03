"""
Khan Academy coding project
Infection

Control release of changes to coaches and students
"""
import networkx as nx

class User(object):
    """Simplified user representation"""
    def __init__(self):
        self.connections = []

def total_infection(users, target_user):
    """Create an infection of all users connected to the target user"""
    if not target_user:
        return []

    user_graph = nx.Graph()
    for user in users:
        user_graph.add_node(user)
        for coached_student in user.connections:
            user_graph.add_edge(user, coached_student)
    connected_users = nx.node_connected_component(user_graph, target_user)
    return list(connected_users)

def limited_infection():
    """Create an infection that is bounded by the target size"""
    pass
