from Stop import Stop
from DataManager import dump_csv, dump_json_lines

class StopQuery():
  def __init__(self, stops):
    if not isinstance(stops, list):
      raise Exception('stops must be a list of Stop')
    if not all(isinstance(stop, Stop) for stop in stops):
      raise Exception('stops must be a list of Stop')

    self.Stops = stops

  def __repr__(self) -> str:
    return str(self.Stops)

  def __len__(self) -> int:
    return len(self.Stops)

  def __getitem__(self, item):
    return self.Stops[item]

  def searchByAttribute(self, attribute, value, exact_match=True):
    filtered = []
    for stop in self.Stops:
      if not hasattr(stop, attribute):
        raise Exception(f'{attribute} is not valid')
      current_value = getattr(stop, attribute)
      if type(current_value) != type(value) and current_value is not None:
        raise Exception(f'Type mismatch: {current_value} and {value}')

      if (
        current_value == value or
        not exact_match and
        current_value is not None and
        isinstance(value, str) and
        value in current_value
      ):
        filtered.append(stop)
    return StopQuery(filtered)

  def searchByCustomFilter(self, custom_filter):
    if not callable(custom_filter):
      raise Exception('custom_filter must be callable')

    filtered = []
    for stop in self.Stops:
      if custom_filter(stop):
        filtered.append(stop)
    return StopQuery(filtered)
    
  @staticmethod
  def outputAsCSV(stops, path):
    rows = []
    rows.append(['StopId', 'Code', 'Name', 'StopType', 'Zone', 'Ward', 'AddressNo', 'Street', 'SupportDisability', 'Status', 'Lng', 'Lat', 'Search', 'Routes'])
    rows.extend([stop.__dict__.values() for stop in stops])
    dump_csv(rows, path)

  def toCSV(self, path):
    StopQuery.outputAsCSV(self.Stops, path)

  @staticmethod
  def outputAsJSON(stops, path):
    rows = [stop.to_dict() for stop in stops]
    dump_json_lines(rows, path)

  def toJSON(self, path):
    StopQuery.outputAsJSON(self.Stops, path)
