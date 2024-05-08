from RouteVar import RouteVar
from DataManager import dump_csv, dump_json_lines

class RouteVarQuery():
  def __init__(self, route_vars):
    if not isinstance(route_vars, list):
      raise Exception('route_vars must be a list of RouteVar')
    if not all(isinstance(var, RouteVar) for var in route_vars):
      raise Exception('route_vars must be a list of RouteVar')

    self.RouteVars = route_vars

  def __repr__(self) -> str:
    return str(self.RouteVars)

  def searchByAttribute(self, attribute, value, exact_match=True):
    filtered = []
    for var in self.RouteVars:
      if not hasattr(var, attribute):
        raise Exception(f'{attribute} is not valid')
      current_value = getattr(var, attribute)
      if type(current_value) != type(value):
        raise Exception(f'Type mismatch: {current_value} and {value}')

      if (
        current_value == value or
        not exact_match and
        isinstance(value, str) and
        value in current_value
      ):
        filtered.append(var)
    return RouteVarQuery(filtered)

  def searchByCustomFilter(self, custom_filter):
    if not callable(custom_filter):
      raise Exception('custom_filter must be callable')

    filtered = []
    for var in self.RouteVars:
      if custom_filter(var):
        filtered.append(var)
    return RouteVarQuery(filtered)
    
  @staticmethod
  def outputAsCSV(route_vars, path):
    rows = []
    rows.append(['RouteId', 'RouteVarId', 'RouteVarName', 'RouteVarShortName', 'RouteNo', 'StartStop', 'EndStop', 'Distance', 'Outbound', 'RunningTime'])
    rows.extend([
      [
        v
        for k, v in var.__dict__.items()
        if k not in ['_Stops', '_Path']
      ]
      for var in route_vars
    ])
    dump_csv(rows, path)

  def toCSV(self, path):
    RouteVarQuery.outputAsCSV(self.RouteVars, path)

  @staticmethod
  def outputAsJSON(route_vars, path):
    rows = [var.to_dict() for var in route_vars]
    dump_json_lines(rows, path)

  def toJSON(self, path):
    RouteVarQuery.outputAsJSON(self.RouteVars, path)
