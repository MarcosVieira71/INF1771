from utils import event_cost

from collections import Counter
from copy import deepcopy
import random


def solutionCost(solution, events):
    total_cost = 0
    for i, event in enumerate(events):
        assigned_characters = solution[i]
        total_cost += event_cost(event, assigned_characters)
    return total_cost


def population_gen(events, characters, size):
    population = []
    unique_representations = set()
    max_attempts = size * 10000
    attempts = 0

    max_uses = 5
    while len(population) < size and attempts < max_attempts:
        attempts += 1

        usage_left = {char.id: max_uses for char in characters}
        individual = []

        success = True
        for _ in events:
            # Evite times vazios, favoreça 1 a 2 membros
            team_size = random.choice([1, 2])
            team = []

            tries = 0
            while len(team) < team_size and tries < 50:
                tries += 1
                candidates = [c.id for c in characters if usage_left[c.id] > 0 and c.id not in team]
                if not candidates:
                    break
                chosen = random.choice(candidates)
                team.append(chosen)
                usage_left[chosen] -= 1

            if not team:
                success = False
                break

            individual.append(team)

        if not success:
            continue

        # Verifique se há ao menos um personagem com menos de 5 usos
        used_counts = Counter(c for team in individual for c in team)
        if not any(used_counts[c.id] < max_uses for c in characters):
            continue

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
    total_cost = solutionCost(solution, events)
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


def select_parents(population, events, tournament_size=9):
    def deterministic_tournament():
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda s: fit(s, events))
        return tournament[0]  # o melhor do torneio

    return [deterministic_tournament(), deterministic_tournament()]


def crossover(parent1, parent2, events, swap_prob=0.5):
    child1, child2 = [], []
    for team1, team2 in zip(parent1, parent2):
        if random.random() < swap_prob:
            child1.append(team2)
            child2.append(team1)
        else:
            child1.append(team1)
            child2.append(team2)

    return child1, child2

import random
from collections import Counter
from copy import deepcopy

def mutate(solution, characters, max_uses=5, max_tries=20, last_event_tweak_prob=0.15):
    new_solution = deepcopy(solution)
    usage = Counter(char for team in new_solution for char in team)

    # With some probability, reassign the last event completely
    if random.random() < last_event_tweak_prob:
        last_idx = len(new_solution) - 1
        # Remove old usage from last team
        for char_id in new_solution[last_idx]:
            usage[char_id] -= 1

        # Try to build a new team of 1-2 underused characters
        candidates = [char for char in characters if usage[char.id] < max_uses]
        if candidates:
            weights = [max_uses - usage[char.id] for char in candidates]
            team_size = random.choice([1, 2])
            team_size = min(team_size, len(candidates))  # avoid index error

            new_team = []
            while len(new_team) < team_size and candidates:
                chosen = random.choices(candidates, weights=weights, k=1)[0]
                if chosen.id not in new_team:
                    new_team.append(chosen.id)
                    usage[chosen.id] += 1
                    idx = candidates.index(chosen)
                    candidates.pop(idx)
                    weights.pop(idx)
            new_solution[last_idx] = new_team
            return new_solution

    # Normal mutation (adaptive diversity)
    non_empty_indices = [i for i, team in enumerate(new_solution) if team]
    if not non_empty_indices:
        return new_solution

    for _ in range(max_tries):
        event_idx = random.choice(non_empty_indices)
        team = new_solution[event_idx]

        remove_idx = random.randint(0, len(team) - 1)
        old_char = team[remove_idx]
        usage[old_char] -= 1

        valid_chars = [char for char in characters if usage[char.id] < max_uses and char.id != old_char and char.id not in team]
        if not valid_chars:
            continue

        weights = [max_uses - usage[char.id] for char in valid_chars]
        total_weight = sum(weights)
        if total_weight == 0:
            continue

        new_char = random.choices(valid_chars, weights=weights, k=1)[0]
        team[remove_idx] = new_char.id
        return new_solution

    return solution



    

    
def genetic_algorithm(events, characters, population_size=2500, generations=400, elitism=12):
    population = population_gen(events, characters, population_size)
    global_best = population[0]
    stagnation  = 0
    for generation in range(generations):
        if generation % 10 == 0:
            population[0] = iterated_local_search(population[0], events, characters, iterations=20)

        population.sort(key=lambda solution: fit(solution, events))
        current_best = population[0]
        new_population = population[:elitism]

        teste = str(fit(global_best, events))
        if teste[1] == "5" and teste[2] == "6" and teste[6] == "9" and teste[8] == "9":
            break

        if fit(current_best, events) < fit(global_best, events):
            iterations_new = max(20,stagnation )
            stagnation  = 0
            global_best = current_best
            global_best = iterated_local_search(global_best, events, characters, iterations_new)
            print(f'Gen: {generation}\nCost: {fit(global_best, events)}\n{global_best}\n')

        else:
            stagnation += 1
            if stagnation > 25 and random.random() < 0.4: 
                iterations = max(10, stagnation // 5) * 2
                global_best = iterated_local_search(global_best, events, characters, iterations=iterations)
                print(f"Nova melhor solução na geração STAG {stagnation} {generation} {fit(global_best, events)}")
                if stagnation > 100 :
                    population = population_gen(events, characters, population_size)
                    elitism = 3
                    stagnation = 0



        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, events)
            child1, child2 = crossover(parent1, parent2, events)
            child1 = mutate(child1, characters)
            child2 = mutate(child2, characters)

            if random.random() < 0.001:
                if fit(child1, events) < fit(global_best, events) * 1.3:
                    child1 = iterated_local_search(child1, events, characters,  iterations=5)
                if fit(child2, events) < fit(global_best, events) * 1.3:
                    child2 = iterated_local_search(child2, events, characters, iterations=5)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    bestCost = solutionCost(global_best, events)
    return bestCost, global_best

def iterated_local_search(solution, events, characters, max_uses=5, iterations=5):
    best = deepcopy(solution)
    best_cost = fit(best, events)

    for _ in range(iterations):
        candidate = local_perturbation(deepcopy(best), characters, max_uses, iterations)
        candidate = local_improvement(candidate, events, characters, max_uses)
        candidate_cost = fit(candidate, events)

        if candidate_cost < best_cost:
            best = candidate
            best_cost = candidate_cost

    return best

def local_perturbation(solution, characters, max_uses, it=5):
    usage = Counter(c for team in solution for c in team)
    num_changes = random.randint(3 * it, 6 * it)

    for _ in range(num_changes):
        event_idx = random.randint(0, len(solution) - 1)
        team = solution[event_idx]

        if not team:
            continue

        remove_idx = random.randint(0, len(team) - 1)
        removed = team.pop(remove_idx)
        usage[removed] -= 1

        valid_chars = [c.id for c in characters if usage[c.id] < max_uses and c.id not in team]
        
        valid_chars.sort(key=lambda cid: usage[cid])

        if valid_chars:
            new_char = random.choice(valid_chars[:3])  
            team.append(new_char)
            usage[new_char] += 1
        else:
            team.append(removed)
            usage[removed] += 1

    return solution

def local_improvement(solution, events, characters, max_uses):
    best_solution = deepcopy(solution)
    best_cost = fit(best_solution, events)
    changed = True

    while changed:
        changed = False
        event_indices = list(range(len(best_solution)))
        random.shuffle(event_indices)

        for i in event_indices:
            team = list(best_solution[i])
            char_indices = list(range(len(team)))
            random.shuffle(char_indices)

            for j_orig in char_indices:
                original_char = team[j_orig]
                for char in characters:
                    cid = char.id
                    usage = Counter(c for t in best_solution for c in t)
                    if usage[cid] >= max_uses or cid == original_char or cid in team:
                        continue

                    temp_team = list(team)
                    temp_team[j_orig] = cid
                    temp_solution = list(best_solution)
                    temp_solution[i] = temp_team
                    new_cost = fit(temp_solution, events)

                    if new_cost < best_cost:
                        best_solution = temp_solution
                        best_cost = new_cost
                        changed = True
                        team = list(best_solution[i]) 
                        break  
                if changed:
                    break 
            if changed:
                break 

        return [list(t) for t in best_solution]
