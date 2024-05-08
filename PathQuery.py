from Path import Path
from DataManager import dump_csv, dump_json_lines

class PathQuery():
  def __init__(self, paths):
    if not isinstance(paths, list):
      raise Exception('paths must be a list of Path')
    if not all(isinstance(path, Path) for path in paths):
      raise Exception('paths must be a list of Path')

    self.Paths = paths

  def searchByAttribute(self, attribute, value):
    filtered = []
    for path in self.Paths:
      if not hasattr(path, attribute):
        raise Exception(f'{attribute} is not valid')
      current_value = getattr(path, attribute)
      if type(current_value) != type(value):
        raise Exception(f'Type mismatch: {current_value} and {value}')

      if current_value == value:
        filtered.append(path)
    return PathQuery(filtered)

  def searchByCustomFilter(self, custom_filter):
    if not callable(custom_filter):
      raise Exception('custom_filter must be callable')

    filtered = []
    for path in self.Paths:
      if custom_filter(path):
        filtered.append(path)
    return PathQuery(filtered)
    
  @staticmethod
  def outputAsCSV(paths, file_path):
    rows = []
    rows.append(['lat', 'lng', 'RouteId', 'RouteVarId'])
    rows.extend([path.__dict__.values() for path in paths])
    dump_csv(rows, file_path)

  def toCSV(self, path):
    PathQuery.outputAsCSV(self.Paths, path)

  @staticmethod
  def outputAsJSON(paths, file_path):
    rows = [path.to_dict() for path in paths]
    dump_json_lines(rows, file_path)

  def toJSON(self, path):
    PathQuery.outputAsJSON(self.Paths, path)
