import random
import string

def generate_random_object(depth=0, max_depth=4):
    if depth >= max_depth:
        return random.choice([
            random.randint(-1000, 1000),
            random.uniform(-1000, 1000),
            random.choice([True, False]),
            ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10))),
            None
        ])

    simple_types = ["int", "float", "str", "bool", "None"]
    complex_types = ["list", "dict", "tuple", "set"]
    obj_type = random.choices(simple_types + complex_types,
                              weights=[8]*len(simple_types) + [1]*len(complex_types), k=1)[0]

    if obj_type == "int":
        return random.randint(-1000, 1000)
    elif obj_type == "float":
        return random.uniform(-1000, 1000)
    elif obj_type == "str":
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))
    elif obj_type == "bool":
        return random.choice([True, False])
    elif obj_type == "None":
        return None
    elif obj_type == "list":
        return [generate_random_object(depth + 1, max_depth) for _ in range(random.randint(0, 5))]
    elif obj_type == "dict":
        return {str(i): generate_random_object(depth + 1, max_depth) for i in range(random.randint(0, 5))}
    elif obj_type == "tuple":
        return tuple(generate_random_object(depth + 1, max_depth) for _ in range(random.randint(0, 5)))
    elif obj_type == "set":
        items = []
        for _ in range(random.randint(0, 5)):
            item = generate_random_object(depth + 1, max_depth)
            try:
                hash(item)
                items.append(item)
            except TypeError:
                continue
        return set(items)