from .context import feature_infection
import pytest
import uuid
from operator import attrgetter

@pytest.fixture(scope="module")
def test_feature(request):
    return feature_infection.CDC.get_infector("test")

def infected(feature, entities):
    return map(feature.is_infected, entities)

class Entity(object):
    """Simplified user representation"""
    def __init__(self):
        self.connections = []
        self.id = uuid.uuid4()

    def __eq__(self, other):
        return self.id == other.id

    get_connections = attrgetter("connections")


class TestTotalInfection:
    def test_no_entities(self, test_feature):
        entities = []
        assert test_feature.total_infection(entities, None,
            connections=Entity.get_connections) == set()

    def test_single_user(self, test_feature):
        entities = [Entity()]
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities)

    def test_disconnected_user(self, test_feature):
        entities = [Entity(), Entity()]
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities[0:1])

    def test_connected_entities(self, test_feature):
        user1 = Entity()
        user2 = Entity()
        user1.connections.append(user2)
        entities = [user1, user2]
        assert test_feature.total_infection(entities, user1,
            connections=Entity.get_connections) == set(entities)
        assert test_feature.total_infection(entities, user2,
            connections=Entity.get_connections) == set(entities)

    def test_disjoint_connected_groups(self, test_feature):
        entities = [Entity(), Entity(), Entity(), Entity()]
        entities[0].connections.append(entities[1])
        entities[2].connections.append(entities[3])
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities[:2])
        assert test_feature.total_infection(entities, entities[2],
            connections=Entity.get_connections) == set(entities[2:])

    def test_transitive_connection(self, test_feature):
        entities = [Entity(), Entity(), Entity()]
        entities[0].connections.append(entities[1])
        entities[1].connections.append(entities[2])
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities)

    def test_connection_cycle(self, test_feature):
        entities = [Entity(), Entity(), Entity()]
        entities[0].connections.append(entities[1])
        entities[1].connections.append(entities[2])
        entities[2].connections.append(entities[0])
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities)

    def test_self_connection(self, test_feature):
        entities = [Entity(), Entity()]
        entities[0].connections.append(entities[0])
        entities[0].connections.append(entities[1])
        assert test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections) == set(entities)

    def test_marked_infected(self, test_feature):
        entities = [Entity(), Entity()]
        entities[0].connections.append(entities[1])

        test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections)

        assert all(infected(test_feature, entities))

    def test_only_current_feature_infecting(self, test_feature):
        entities = [Entity()]
        seperate_feature = feature_infection.CDC.get_infector("seperate")

        test_feature.total_infection(entities, entities[0],
            connections=Entity.get_connections)

        assert not seperate_feature.is_infected(entities[0])


class TestLimitdInfection:
    def test_limited_infection(self, test_feature):
        entities = [Entity(), Entity(), Entity()]
        entities[1].connections.append(entities[2])

        assert test_feature.limited_infection(entities, 1,
            connections=Entity.get_connections) == set([entities[0]])

    def test_single_network(self, test_feature):
        entities = [Entity(), Entity()]
        entities[0].connections.append(entities[1])

        test_feature.limited_infection(entities, 2,
            connections=Entity.get_connections)

        assert all(infected(test_feature, entities))

    def test_single_large_network(self, test_feature):
        entities = [Entity(), Entity()]
        entities[0].connections.append(entities[1])

        test_feature.limited_infection(entities, 1,
            connections=Entity.get_connections)

        assert not any(infected(test_feature, entities))

    def test_multiple_components(self, test_feature):
        entities = [Entity(), Entity(), Entity()]
        entities[1].connections.append(entities[2])

        test_feature.limited_infection(entities, 3,
            connections=Entity.get_connections)

        assert all(infected(test_feature, entities))

    def test_multiple_non_exact(self, test_feature):
        entities = [Entity(), Entity(), Entity(), Entity()]
        entities[1].connections.extend(entities[2:])

        test_feature.limited_infection(entities, 2,
            connections=Entity.get_connections)

        assert test_feature.is_infected(entities[0])

    def test_smaller_network(self, test_feature):
        entities = [Entity()]

        test_feature.limited_infection(entities, 2,
            connections=Entity.get_connections)

        assert all(infected(test_feature, entities))

    def test_only_current_feature_infected(self, test_feature):
        entities = [Entity()]
        seperate_feature = feature_infection.CDC.get_infector("seperate")

        test_feature.limited_infection(entities, 1,
            connections=Entity.get_connections)

        assert not seperate_feature.is_infected(entities[0])

