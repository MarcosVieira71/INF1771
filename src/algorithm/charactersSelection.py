from utils import event_cost


def population_gen(events, characters, size):
    import random


    population = []
    for _ in range(size):
        lives = {i: 5 for i in characters}
        solution = []
        
        for event in events:
            try:

                validChars = [char for char in lives.keys() if lives[char] > 0]
                assigned_characters = random.sample(validChars, random.randint(1, len(validChars)))
                for char in assigned_characters:
                    lives[char] -= 1
                solution.append([i.id for i in assigned_characters])
            except:
                break

        population.append(solution)
        

    return population 

def fit(solution, events):
    total_cost = 0
    for i, event in enumerate(events):
        assigned_characters = solution[i]
        total_cost += event_cost(event, assigned_characters)
    character_usage = {}
    for assigned_characters in solution:
        for char in assigned_characters:
            if char not in character_usage:
                character_usage[char] = 0
            character_usage[char] += 1
    

    for char in character_usage:
        if character_usage[char] > 5:
            return float("inf")

    alive_characters = [char for char, usage in character_usage.items() if usage < 5]
    if len(alive_characters) < 1:
        return float("inf")

    return total_cost

def select_parents(population, events, characters):
    population.sort(key=lambda solution: fit(solution, events))
    return population[:2]

def crossover(parent1, parent2):
    import random
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point]  + parent2[crossover_point:]
    child2 = parent1[crossover_point:]  + parent2[:crossover_point]
    return child1, child2

def mutate(solution, characters):
    import random
    event_idx = random.randint(0, len(solution) - 1)
    new_character = random.choice(characters)
    solution[event_idx] = [new_character.id]
    

def genetic_algorithm(events, characters, population_size=1000, generations= 100):
    population = population_gen(events, characters, population_size)
    for generation in range(generations):
        parent1, parent2 = select_parents(population, events, characters)
        child1, child2 = crossover(parent1, parent2)
        mutate(child1, characters)
        mutate(child2, characters)
        population.append(child1)
        population.append(child2)
        population.sort(key=lambda solution: fit(solution, events))
        population = population[:population_size]
    return population[0]


 