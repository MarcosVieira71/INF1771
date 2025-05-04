from utils import event_cost


import random
from copy import deepcopy
from collections import Counter




def population_gen(events, characters, size):
    population = []
    unique_representations = set()
    max_attempts = size * 10000
    attempts = 0

    max_uses = 5
    max_per_event = 5

    while len(population) < size and attempts < max_attempts:
        attempts += 1

        usage_left = {char: max_uses for char in characters}
        individual = try_generate_individual(events, characters, usage_left, max_per_event)

        if individual:
            repr_individual = tuple(tuple(sorted(team)) for team in individual)

            if repr_individual not in unique_representations:
                population.append(individual)
                unique_representations.add(repr_individual)

    if len(population) < 2:
        raise ValueError("Não foi possível gerar pelo menos 2 indivíduos válidos com as restrições.")
    return population

def try_generate_individual(events, characters, usage_left, max_per_event):
    event_slots = [[] for _ in events]
    local_usage = {}

    available_chars = [char for char in characters if usage_left[char] > 0]
    total_assignments = [(char, i) for char in available_chars for i in range(usage_left[char])]
    random.shuffle(total_assignments)

    event_indices = list(range(len(events)))
    random.shuffle(event_indices)

    for char, _ in total_assignments:
        candidate_events = [i for i in event_indices if len(event_slots[i]) < max_per_event]
        if not candidate_events:
            break

        empty_events = [i for i in candidate_events if len(event_slots[i]) == 0]
        chosen_event = random.choice(empty_events) if empty_events else random.choice(candidate_events)

        if char not in event_slots[chosen_event]:
            event_slots[chosen_event].append(char)
        local_usage[char] = local_usage.get(char, 0) + 1

    if all(len(team) > 0 for team in event_slots):
        return [[char.id if hasattr(char, 'id') else char for char in team] for team in event_slots]
    return None


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
    
    penalty = 0
    for char, count in character_usage.items():
        if count > 5:
            penalty += (count - 5) * 50 

    if len([c for c in character_usage if character_usage[c] < 5]) < 1:
        penalty += 1000

    return total_cost + penalty

def select_parents(population, events, tournament_size=7):
    def soft_tournament():
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda s: fit(s, events))
        weights = [0.5 ** i for i in range(len(tournament))]
        total = sum(weights)
        probs = [w / total for w in weights]
        return random.choices(tournament, weights=probs, k=1)[0]

    return [soft_tournament(), soft_tournament()]


def crossover(parent1, parent2, events, max_tries=30, min_segment_ratio=0.25):
    best_child1 = None
    best_child2 = None
    best_cost1 = float("inf")
    best_cost2 = float("inf")
    length = len(parent1)
    min_segment = int(length * min_segment_ratio)


    for _ in range(max_tries):
        crossover_point1 = random.randint(1, len(parent1) - 2)
        crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)

        if crossover_point2 - crossover_point1 < min_segment:
            continue

        child1 = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
        child2 = parent2[:crossover_point1] + parent1[crossover_point1:crossover_point2] + parent2[crossover_point2:]

        cost1 = fit(child1, events)
        cost2 = fit(child2, events)

        if cost1 < best_cost1:
            best_child1 = child1
            best_cost1 = cost1
        if cost2 < best_cost2:
            best_child2 = child2
            best_cost2 = cost2

    return best_child1, best_child2



def mutate(solution, characters, max_uses=5, max_tries=20):
    new_solution = deepcopy(solution)
    usage = Counter(char for team in new_solution for char in team)

    non_empty_indices = [i for i, team in enumerate(new_solution) if team]
    if not non_empty_indices:
        return new_solution

    for _ in range(max_tries):
        event_idx = random.choice(non_empty_indices)
        team = new_solution[event_idx]

        remove_idx = random.randint(0, len(team) - 1)
        old_char = team[remove_idx]
        usage[old_char] -= 1

        valid_chars = [char for char in characters if usage[char.id] < max_uses and char.id != old_char]
        if not valid_chars:
            continue

        new_char = random.choice(valid_chars)
        if new_char.id != old_char and new_char.id not in team:
            team[remove_idx] = new_char.id
            return new_solution

    return solution

    

    
def genetic_algorithm(events, characters, population_size=3000, generations=300, elitism=10):
    population = population_gen(events, characters, population_size)
    global_best = population[0]
    generations_without_better_one = 0
    for generation in range(generations):
        population.sort(key=lambda solution: fit(solution, events))
        current_best = population[0]
        new_population = population[:elitism]


        if fit(current_best, events) < fit(global_best, events):
            iterations_new = max(20,generations_without_better_one)
            generations_without_better_one = 0
            global_best = current_best
            global_best = iterated_local_search(global_best, events, characters, iterations_new)
            print("Achou um novo melhor global!")

        else:
            generations_without_better_one+=1

        if generations_without_better_one >= 40:
            random_part = population_gen(events, characters, population_size)
            new_population = population[:elitism] + random_part
            generations_without_better_one = 0


        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, events)
            child1, child2 = crossover(parent1, parent2, events)
            child1 = mutate(child1, characters)
            child2 = mutate(child2, characters)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population
    return global_best

def iterated_local_search(solution, events, characters, max_uses=5, iterations=5):
    best = deepcopy(solution)
    best_cost = fit(best, events)

    for _ in range(iterations):
        candidate = local_perturbation(deepcopy(best), characters, max_uses)
        candidate = local_improvement(candidate, events, characters, max_uses)
        candidate_cost = fit(candidate, events)

        if candidate_cost < best_cost:
            best = candidate
            best_cost = candidate_cost

    return best

def local_perturbation(solution, characters, max_uses):
    usage = Counter(c for team in solution for c in team)

    for _ in range(random.randint(3, 6)):
        event_idx = random.randint(0, len(solution) - 1)
        team = solution[event_idx]

        if not team:
            continue

        remove_idx = random.randint(0, len(team) - 1)
        removed = team.pop(remove_idx)
        usage[removed] -= 1

        valid_chars = [c.id for c in characters if usage[c.id] < max_uses and c.id not in team]
        if valid_chars:
            new_char = random.choice(valid_chars)
            team.append(new_char)
            usage[new_char] += 1

    return solution

def local_improvement(solution, events, characters, max_uses):
    usage = Counter(c for team in solution for c in team)

    for i, team in enumerate(solution):
        for j in range(len(team)):
            original = team[j]
            best_char = original
            best_cost = fit(solution, events)

            for char in characters:
                char_id = char.id
                if usage[char_id] >= max_uses or char_id == original or char_id in team:
                    continue

                team[j] = char_id
                new_cost = fit(solution, events)

                if new_cost < best_cost:
                    best_char = char_id
                    best_cost = new_cost

                team[j] = original 

            if best_char != original:
                usage[original] -= 1
                usage[best_char] += 1
            team[j] = best_char

    return solution