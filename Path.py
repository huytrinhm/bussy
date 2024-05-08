class Path():
  def __init__(self, lat, lng, RouteId, RouteVarId):
    self.lat = lat
    self.lng = lng
    self.RouteId = RouteId
    self.RouteVarId = RouteVarId

  def __repr__(self):
    return f'Path(lat=[{len(self.lat)} value(s)], lng=[{len(self.lng)} value(s)])'

  def to_dict(self):
    return {
      k[1:]: v
      for k, v in self.__dict__.items()
    }

  @property
  def lat(self):
    return self._lat
  @lat.setter
  def lat(self, value):
    self._lat = value

  @property
  def lng(self):
    return self._lng
  @lng.setter
  def lng(self, value):
    self._lng = value

  @property
  def RouteId(self):
    return self._RouteId
  @RouteId.setter
  def RouteId(self, value):
    self._RouteId = value

  @property
  def RouteVarId(self):
    return self._RouteVarId
  @RouteVarId.setter
  def RouteVarId(self, value):
    self._RouteVarId = value
