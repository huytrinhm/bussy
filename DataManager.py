import json
import csv
from utils import get_uuid
from RouteVar import RouteVar
from Stop import Stop
from Path import Path
from typing import List, Dict, Tuple

def load_json_lines(path: str) -> List[Dict]:
  data = []
  with open(path, encoding='utf8') as f:
    for line in f:
      json_line = json.loads(line)
      if isinstance(json_line, dict):
        data.append(json_line)
      else:
        data.extend(json_line)
  return data

def dump_csv(rows: list, path: str):
  with open(path, 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
      writer.writerow(row)

def dump_json_lines(rows: List[Dict], path: str):
  with open(path, 'w', encoding='utf8') as f:
    for row in rows:
      f.write(json.dumps(row) + '\n')

def load_data(
  vars_path: str,
  stops_path: str,
  paths_path: str
) -> Tuple[Dict[str, RouteVar], Dict[str, Stop]]:
  route_vars_json = load_json_lines(vars_path)
  stops_json = load_json_lines(stops_path)
  paths_json = load_json_lines(paths_path)

  route_vars = {
    get_uuid(route_var): RouteVar(**route_var)
    for route_var in route_vars_json
  }

  all_stops = {}

  for stops in stops_json:
    uuid = get_uuid(stops)
    route_vars[uuid].Stops = []
    for stop in stops['Stops']:
      route_vars[uuid].Stops.append(stop['StopId'])
      if stop['StopId'] not in all_stops:
        all_stops[stop['StopId']] = Stop(**stop)

  for path in paths_json:
    uuid = get_uuid(path)
    route_vars[uuid].Path = Path(**path)

  return route_vars, all_stops
