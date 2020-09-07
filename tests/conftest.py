import os
import json
from pathlib import Path
from typing import List, Dict


def load_seed(file):
    current_folder = os.path.dirname(__file__)
    data = Path(os.path.join(current_folder, file)).read_text()
    return json.loads(data)


def mapbit(length: int, trues: List = [], falses: List = []):
    def _value(key: int):
        if trues:
            return key in trues
        if falses:
            return key not in falses
        return True

    return {i + 1: _value(i + 1) for i in range(length)}


def mapbit_from_dict(length: int, trues: Dict) -> Dict[int, bool]:
    trues = [int(i) for i, _ in trues.items()]
    return mapbit(length or len(trues), trues=trues)
