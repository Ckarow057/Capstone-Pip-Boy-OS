def get_player_stats_data():
    return {
        "name": "VAULT DWELLER",
        "level": 1,
        "hp": 200,
        "max_hp": 200,
        "ap": 80,
        "max_ap": 80,
        "rads": 12,
        "xp": 10,
        "next_level": 200,
        "caps": 542,
        "condition": 85,
        "effects": 0
    }


def get_inventory_data():
    return [
        {"name": "Stimpak", "count": 5, "hotkey": "S"},
        {"name": "Doctor's Bag", "count": 3, "hotkey": "E"}
    ]


def get_special_stats_data():
    return {
        "S": 7,
        "P": 6,
        "E": 5,
        "C": 4,
        "I": 8,
        "A": 6,
        "L": 5
    }


def get_body_parts_data():
    return {
        "head": 100,
        "torso": 85,
        "left_arm": 90,
        "right_arm": 100,
        "left_leg": 75,
        "right_leg": 80
    }