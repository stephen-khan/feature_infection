"""
Khan Academy coding project
Infection

Control release of changes to coaches and students
"""
from operator import itemgetter

import networkx as nx
from . import subset_sum as ss


class User(object):
    """Simplified user representation"""
    def __init__(self):
        self.connections = []


def generate_connection_graph(users):
    """Convert a list of users into a graph using coaching relationships as the edges"""
    user_graph = nx.Graph()
    for user in users:
        user_graph.add_node(user)
        for coached_student in user.connections:
            user_graph.add_edge(user, coached_student)
    return user_graph


def total_infection(users, target_user):
    """Create an infection of all users connected to the target user"""
    if not target_user:
        return []

    user_graph = generate_connection_graph(users)
    connected_users = nx.node_connected_component(user_graph, target_user)
    return list(connected_users)


def limited_infection(users, target_size):
    """Create an infection that is bounded by the target size"""
    user_graph = generate_connection_graph(users)
    user_groups = [(len(group), group)
                   for group in nx.connected_components(user_graph)]
    get_count = itemgetter(0)
    get_users = itemgetter(1)
    _, infection_groups = ss.greedy(user_groups, target_size, key=get_count)
    return map(get_users, infection_groups)
