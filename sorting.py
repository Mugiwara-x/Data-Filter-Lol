from typing import List, Dict, Any, Callable

def sort_by_field(data: List[Dict[str, Any]], field: str, reverse: bool = False) -> List[Dict[str, Any]]:
    return sorted(data, key=lambda d: d.get(field, 0), reverse=reverse)

def sort_by_custom_key(data: List[Dict[str, Any]], key_func: Callable[[Dict[str, Any]], Any], reverse: bool = False) -> List[Dict[str, Any]]:
    return sorted(data, key=key_func, reverse=reverse)