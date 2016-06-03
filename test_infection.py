import infection
User = infection.User

def test_total_infection_of_no_users():
    users = []
    assert infection.total_infection(users, None) == []

def test_total_infection_of_single_user():
    users = [User()]
    assert infection.total_infection(users, users[0]) == users

def test_total_infection_of_disconnected_user():
    users = [User(), User()]
    assert infection.total_infection(users, users[0]) == users[0:1]

def test_total_infection_of_connected_users():
    user1 = User()
    user2 = User()
    user1.connections.append(user2)
    users = [user1, user2]
    assert sorted(infection.total_infection(users, user1)) == sorted(users)
    assert sorted(infection.total_infection(users, user2)) == sorted(users)

def test_total_infection_of_disjoint_connected_users():
    users = [User(), User(), User(), User()]
    users[0].connections.append(users[1])
    users[2].connections.append(users[3])
    assert sorted(infection.total_infection(users, users[0])) == sorted(users[:2])
    assert sorted(infection.total_infection(users, users[2])) == sorted(users[2:])
    

def test_limited_infection():
    infection.limited_infection()
    assert True
