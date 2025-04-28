from utils import event_cost


from collections import defaultdict
import random
import random

import random

import random

def population_gen(events, characters, size):
    population = []
    max_attempts = size * 100
    attempts = 0

    max_uses = 5  
    max_per_event = 5

    usage_left = {char: max_uses for char in characters}  

    while len(population) < size and attempts < max_attempts:
        attempts += 1
        event_slots = [[] for _ in events]

        available_chars = [char for char in characters if usage_left[char] > 0]
        if not available_chars:
            break  

        total_assignments = [(char, i) for char in available_chars for i in range(usage_left[char])]
        random.shuffle(total_assignments)

        local_usage = {} 

        for char, _ in total_assignments:
            candidate_events = [i for i, team in enumerate(event_slots) if len(team) < max_per_event]
            if not candidate_events:
                break

            empty_events = [i for i in candidate_events if len(event_slots[i]) == 0]
            if empty_events:
                chosen_event = random.choice(empty_events)
            else:
                chosen_event = random.choice(candidate_events)

            event_slots[chosen_event].append(char)
            local_usage[char] = local_usage.get(char, 0) + 1

        if all(len(team) > 0 for team in event_slots):
            if all(usage_left[char] >= local_usage.get(char, 0) for char in local_usage):
                for char in local_usage:
                    usage_left[char] -= local_usage[char]

                individual = [[char.id if hasattr(char, 'id') else char for char in team] for team in event_slots]
                population.append(individual)

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

def select_parents(population, events, tournament_size=3):
    selected_parents = []
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        best_parent = min(tournament, key=lambda solution: fit(solution, events))
        selected_parents.append(best_parent)
    return selected_parents

def crossover(parent1, parent2, max_tries=5):
    for _ in range(max_tries):
        crossover_point1 = random.randint(1, len(parent1) - 2)
        crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

        child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
        child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]

    return child1, child2

def mutate(solution, characters, max_uses=5):
    import random
    from copy import deepcopy
    from collections import Counter

    new_solution = deepcopy(solution)
    usage = Counter()
    for group in new_solution:
        usage.update(group)

    event_idx = random.randint(0, len(new_solution) - 1)
    current_chars = new_solution[event_idx]
    
    valid_chars = [char for char in characters if usage[char.id] < max_uses]
    if not valid_chars:
        return new_solution  

    new_char = random.choice(valid_chars)
    usage[new_char.id] += 1
    for c in current_chars:
        usage[c] -= 1

    new_solution[event_idx] = [new_char.id]
    return new_solution

    

def genetic_algorithm(events, characters, population_size=100, generations=100000):
    population = population_gen(events, characters, population_size)

    best_population = population
    while len(population) < 1000:
        population += population_gen(events, characters, population_size)
        if len(population) > len(best_population):
            best_population = population

    if len(population) < 2:
        raise ValueError("Não foi possível gerar uma população inicial com pelo menos 2 indivíduos válidos.")
    
    print(len(population))

    for generation in range(generations):
        parent1, parent2 = select_parents(population, events)
        child1, child2 = crossover(parent1, parent2)
        mutate(child1, characters)
        mutate(child2, characters)
        population.append(child1)
        population.append(child2)
        population.sort(key=lambda solution: fit(solution, events))
        population = population[:population_size]

    return population[0]
