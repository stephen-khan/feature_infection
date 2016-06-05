from .context import infection

User = infection.User

class TestTotalInfection:
    def test_no_users(self):
        users = []
        assert infection.total_infection(users, None) == []

    def test_single_user(self):
        users = [User()]
        assert infection.total_infection(users, users[0]) == users

    def test_disconnected_user(self):
        users = [User(), User()]
        assert infection.total_infection(users, users[0]) == users[0:1]

    def test_connected_users(self):
        user1 = User()
        user2 = User()
        user1.connections.append(user2)
        users = [user1, user2]
        assert sorted(infection.total_infection(users, user1)) == sorted(users)
        assert sorted(infection.total_infection(users, user2)) == sorted(users)

    def test_disjoint_connected_groups(self):
        users = [User(), User(), User(), User()]
        users[0].connections.append(users[1])
        users[2].connections.append(users[3])
        assert sorted(infection.total_infection(users, users[0])) == sorted(users[:2])
        assert sorted(infection.total_infection(users, users[2])) == sorted(users[2:])

    def test_transitive_connection(self):
        users = [User(), User(), User()]
        users[0].connections.append(users[1])
        users[1].connections.append(users[2])
        assert sorted(infection.total_infection(users, users[0])) == sorted(users)

    def test_connection_cycle(self):
        users = [User(), User(), User()]
        users[0].connections.append(users[1])
        users[1].connections.append(users[2])
        users[2].connections.append(users[0])
        assert sorted(infection.total_infection(users, users[0])) == sorted(users)

class TestLimitdInfection:
    def test_limited_infection(self):
        users = [User(), User(), User()]
        users[1].connections.append(users[2])
        assert infection.limited_infection(users, 1) == [set([users[0]])]
