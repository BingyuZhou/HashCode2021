from utils import readIn, writeOut
import numpy as np
import os


def getTeams(a: int, b: int, c: int) -> list:
    result = []
    for i in range(c):
        result.append(4)
    for i in range(b):
        result.append(3)
    for i in range(a):
        result.append(2)
    return result


def getDeliveries(num_pizzas, teams: list) -> list:
    """
    return: 
        list[list[team_size]]
    order of groups
    [[4, 4, 2],
    [2, 2]]
    """
    deliveries = []
    if num_pizzas == 1:
        return []
    if num_pizzas == 2:
        return [2]
    if num_pizzas == 3:
        return [3]
    if num_pizzas == 4:
        return [[4], [2, 2]]
    for c in range(teams[2], -1, -1):
        for b in range(teams[1], -1, -1):
            for a in range(teams[0], -1, -1):
                if 2 * a + 3 * b + 4 * c <= num_pizzas and 2 * a + 3 * b + 4 * c > 0:
                    deliveries.append(getTeams(a, b, c))

    if teams[0] > 3 and teams[1] > 3 and teams[2] > 3:
        for c in range(teams[2], teams[2] - 2, -1):
            for b in range(teams[1], teams[1] - 2, -1):
                for a in range(teams[0], teams[0] - 2, -1):
                    if (
                        2 * a + 3 * b + 4 * c <= num_pizzas
                        and 2 * a + 3 * b + 4 * c > 0
                    ):
                        deliveries.append(getTeams(a, b, c))

    return deliveries


def cpmparePizza(pizza_a: list, pizza_b: list) -> int:
    """
    return:
        num_unique_ingredients: int
    """
    return len(set(pizza_a) | set(pizza_b))


def compare(pizzas, selected_indx, is_reverse=False):
    overall = set()
    if is_reverse:
        for i, pizza in enumerate(pizzas):
            if i not in selected_indx:
                overall = set(pizza) | set(overall)
    else:
        for i, pizza in enumerate(pizzas):
            if i in selected_indx:
                overall = set(pizza) | set(overall)
    return len(overall), overall


def computeTable(
    pizzas: list, picked_pizza_idx: list, picked_pizza_in_this_team
) -> dict:
    """
    line: 3 onion pepper olive

    {pizza_index: sum_unique}
    """
    _, pizza_pool = compare(pizzas, picked_pizza_in_this_team)

    num_pizzas: int = len(pizzas)

    result = {}
    for i in range(num_pizzas):
        if i not in picked_pizza_idx:
            new_ingre = len(set(pizzas[i]) - pizza_pool)
            result[i] = new_ingre

    # num_pizzas: int = len(pizzas)
    # result = {}
    # for i in range(num_pizzas):
    #     if i not in picked_pizza_idx:
    #         sum = 0
    #         for j in range(num_pizzas):
    #             if j != i and j not in picked_pizza_idx:
    #                 sum += cpmparePizza(pizzas[i], pizzas[j])
    #         result[i] = sum
    return result


def solve(filename):
    pizzas, teams = readIn(filename)
    num_pizzas = len(pizzas)

    # compute how many number of deliveries
    # 2a+3b+4c<=M
    candidates = getDeliveries(num_pizzas, teams)

    # for each a,b,c, diliver pizza
    # calculate 2D table
    max_score = 0
    best_delivers = []
    # O(n*m*4)
    for candidate in candidates:
        picked_pizza = []
        delivers = [[] for _ in range(len(candidate))]
        score = []

        for i, team_size in enumerate(candidate):
            for _ in range(team_size):
                value_table = computeTable(pizzas, picked_pizza, delivers[i])

                if len(value_table) > 1:
                    max_val = 0
                    for (key, val) in value_table.items():
                        if val > max_val:
                            max_val = val
                            max_val_pizza = key
                    picked_pizza.append(max_val_pizza)
                    delivers[i].append(max_val_pizza)
                else:
                    picked_pizza.append(list(value_table.keys())[0])
                    delivers[i].append(list(value_table.keys())[0])
            unique_ingre, _ = compare(pizzas, delivers[i])
            score.append(unique_ingre)

        score = np.sum(np.array(score) ** 2)
        if score > max_score:
            max_score = score
            best_delivers = delivers

    writeOut(filename, best_delivers)


if __name__ == "__main__":

    for _, _, files in os.walk("."):
        for file in files:
            if file == "b_little_bit_of_everything.in":
                print("running on ", file, "...")
                solve(file)
            file.close()
