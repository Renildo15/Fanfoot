import csv
import json
import os
from typing import Any, Dict, List, Union


class FileService:
    def get_csv(self, path: str) -> List[Dict[str, str]]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                csv_reader = csv.DictReader(f)
                return list(csv_reader)

        except Exception as e:
            raise ValueError(f"Erro ao ler CSV: {e}")

    def get_json(self, path: str) -> Union[Dict[str, Any], List[Any]]:

        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido em {path}: {e}")
