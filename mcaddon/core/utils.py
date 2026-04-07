__all__ = ["namespaced", "get_folder_size", "limit_lines", "convert_sets"]

from typing import Any
import os


def namespaced(value, discriminator: str = "type"):
    if isinstance(value, dict):
        t = value.get(discriminator)
        if t and ":" not in t:
            value = dict(value)
            value[discriminator] = f"minecraft:{t}"
        return value

    value = str(value)
    return value if ":" in value else f"minecraft:{value}"


def get_folder_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            if not os.path.islink(file_path):
                total += os.path.getsize(file_path)
    return total / (1024 * 1024)


def limit_lines(text: str, n: int) -> str:
    return "\n".join(text.splitlines()[:n])


def convert_sets(obj: Any) -> Any:
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_sets(v) for v in obj]
    return obj
