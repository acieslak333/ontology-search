import re
import json
import pronto


def clean_name(name:str):
    name = name.lower()
    name = name.replace('food product', '')
    name = name.replace('food', '')
    name = name.replace('product', '')
    name = re.sub('[^a-z]', ' ', name)
    name = re.sub(' +', ' ', name)
    return name.strip()


def load_and_dump_to_json(path='data/subFood.obo'):
    ont = pronto.Ontology(path)
    data = json.loads(ont.json)
    clean_data = dict()
    
    for key in data.keys():
        clean_data[key] = dict()
        
        for k, v in data[key].items():
            if k in ["id", "relations", "name"]:
                clean_data[key][k] = v

    with open("./data/clean_data.json", "w") as file:
        json.dump(clean_data, file, indent=4)


def check_items(path="./data/clean_data.json"):
    with open(path, "r") as file:
        data = json.load(file)

    is_a_set = set()

    for key in data.keys():
        data[key]['name'] = clean_name(data[key]['name'])
        try:
            for id in data[key]["relations"]["is_a"]:
                is_a_set.add(id)
        except KeyError as ke:
            pass
        
    for key in data.keys():
        if data[key]["id"] in is_a_set:
            data[key]["item"] = False
        else:
            data[key]["item"] = True

    print(f"Length of database: {len(data.keys())}")
    print(f"Length of items: {len([i for i in data.keys() if data[i]['item'] == True])}")

    for k in [i for i in data.keys() if data[i]['item'] == True]:
        print(data[k]["name"])
    
    with open("./data/clean_data.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    pass