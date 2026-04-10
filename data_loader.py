import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "pip_boy_data.json")
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        with open(_DATA_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def get_player_stats_data() -> dict:
    return _load()["player_stats"]


def get_inventory_data() -> list:
    return _load()["inventory"]


def get_special_stats_data() -> dict:
    return _load()["special"]


def get_body_parts_data() -> dict:
    return _load()["body_parts"]


def get_quests_data() -> list:
    return _load()["quests"]


def get_map_data() -> dict:
    return _load()["map"]


def get_radio_data() -> dict:
    return _load()["radio"]


def get_themes_data() -> list:
    return _load()["themes"]
