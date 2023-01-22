import json
import random
import numpy as np
from jellyfish import jaro_winkler_similarity


def name_similarity(name_1, name_2):
    return jaro_winkler_similarity(name_1, name_2)


def tree_similarity(data, id_1, id_2):
    is_a_union_1 = set()
    is_a_union_2 = set()
    queue_1 = []
    queue_2 = []
    success = False
    similarity_level = 1
    main_id_1_relations = [i for i in data[id_1]["relations"]["is_a"]] 
    main_id_2_relations = [i for i in data[id_2]["relations"]["is_a"]]
    is_a_union_1.add(id_1)
    is_a_union_2.add(id_2)

    for id in main_id_1_relations:
        is_a_union_1.add(id)
    for id in main_id_2_relations:
        is_a_union_2.add(id)

    queue_1.append([id_1])
    queue_2.append([id_2])

    while queue_1 or queue_2:
        print(queue_1)
        print(queue_2)
        
        if is_a_union_1.intersection(is_a_union_2):
            success = True
            break

        try:
            ids_to_check = queue_1.pop(0)
            ids_to_queue = []
            
            for id in ids_to_check:
                item = data[id]

                try:
                    for i in item["relations"]["is_a"]:
                        is_a_union_1.add(i)
                        ids_to_queue.append(i)
                except Exception as e:
                    pass
            
            if ids_to_queue:
                queue_1.append(ids_to_queue)
        
        except Exception as e:
            pass

        try:
            ids_to_check = queue_2.pop(0)
            ids_to_queue = []
            
            for id in ids_to_check:
                item = data[id]

                try:
                    for i in item["relations"]["is_a"]:
                        is_a_union_2.add(i)
                        ids_to_queue.append(i)
                except Exception as e:
                    pass
            
            if ids_to_queue:
                queue_2.append(ids_to_queue)
        
        except Exception as e:
            pass

        similarity_level += 1

    return success, similarity_level


def calculate_total_similarity(name_sim, tree_sim, tree_sim_suc):
    if not tree_sim_suc:
        return 0
    
    return name_sim / np.sqrt(tree_sim)

    
def main(path="./data/clean_data.json"):
    with open(path, "r") as file:
        data = json.load(file)

    items = [data[k] for k in data.keys() if data[k]["item"] == True]
    idx_1 = random.randint(0, len(items) - 1)
    idx_2 = random.randint(0, len(items) - 1)

    name_1 = items[idx_1]["name"]
    name_2 = items[idx_2]["name"]
    id_1 = items[idx_1]["id"]
    id_2 = items[idx_2]["id"]

    print(f"name 1: {name_1}")
    print(f"name 2: {name_2}\n")

    name_sim = name_similarity(name_1, name_2)
    tree_sim_suc, tree_sim = tree_similarity(data, id_1, id_2)
    total_sim = calculate_total_similarity(name_sim, tree_sim, tree_sim_suc)

    print(f"name similarity: {name_sim}")
    print(f"tree similarity: {tree_sim}, tree success: {tree_sim_suc}")
    print(f"total similarity: {total_sim}")
    print("\n")


if __name__ == '__main__':
    main()