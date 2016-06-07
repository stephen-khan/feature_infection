import infection
import random
import networkx as nx

def create_random_users(size, density):
    users = [infection.User() for _ in xrange(size)]
    for user in users:
        for _ in xrange(random.randint(0, density)):
            j = random.randint(0, len(users) - 1)
            if users[j] != user:
                user.connections.append(users[j])
    return users

def create_user_from_model(size, p_teacher = .4, num_coach = 1, p_student_coach = .3):
    users = []
    teachers = []
    students = []
    for _ in xrange(size):
        user = infection.User()
        is_student = random.random() > p_teacher
        if is_student:
            students.append(user)
        else:
            teachers.append(user)
    for student in students:
        for _ in xrange(random.randint(1, 2 * num_coach)):
            is_student_coach = random.random() <= p_student_coach
            if is_student_coach and students:
                i = random.randint(0, len(students) - 1)
                student.connections.append(students[i])
            elif teachers:
                i = random.randint(0, len(teachers) - 1)
                student.connections.append(teachers[i])
    #print "model data", len(teachers), len(students)
    return teachers + students

def generate_connection_graph(users):
    user_graph = nx.Graph()
    for user in users:
        user_graph.add_node(user)
        for coached_student in user.connections:
            user_graph.add_edge(user, coached_student)
    return user_graph

def trial(generator):
    users = generator()
    users_graph = generate_connection_graph(users)
    components = [len(g) for g in nx.connected_components(users_graph)]
    #print components
    return len(components), max(components)

def run_trials(generator, trials):
    data = [trial(generator) for _ in xrange(trials)]
    number = sum(d[0] for d in data) / trials
    size = sum(d[1] for d in data) / trials
    print number, size
    #print data

if __name__ == '__main__':
    size = 10
    trials = 10
    density = 3

    import sys
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    if len(sys.argv) > 2:
        trials = int(sys.argv[2])

    #print "Random Model"
    #run_trials(lambda: create_random_users(size,density), trials)

    print

    print "User Model"
    run_trials(lambda: create_user_from_model(size), trials)

    import infection
    users = create_user_from_model(size)
    target = .1 * len(users)
    infected = infection.limited_infection(users, target)
    actual = sum(len(g) for g in infected)
    print "target:", target, "-> actual:", actual, " (", actual/float(target), ")"
