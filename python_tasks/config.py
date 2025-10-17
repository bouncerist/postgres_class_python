import json
from pathlib import Path
path = Path(__file__).parent.parent / Path("json_files") / Path("config.json")
file = open(path,)
config = json.load(file)
file.close()
database_config = config.get("database")
csv_paths = config.get("csv_paths")
