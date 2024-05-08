class Stop():
  def __init__(
    self, StopId, Code, Name, StopType, Zone, Ward, AddressNo,
    Street, SupportDisability, Status, Lng, Lat, Search, Routes
  ):
    self.StopId = StopId
    self.Code = Code
    self.Name = Name
    self.StopType = StopType
    self.Zone = Zone
    self.Ward = Ward
    self.AddressNo = AddressNo
    self.Street = Street
    self.SupportDisability = SupportDisability
    self.Status = Status
    self.Lng = Lng
    self.Lat = Lat
    self.Search = Search
    self.Routes = Routes

  def __repr__(self):
    s = ''
    s += 'Stop(\n'
    s += f'  StopId={self.StopId!r}\n'
    s += f'  Code={self.Code!r}\n'
    s += f'  Name={self.Name!r}\n'
    s += f'  StopType={self.StopType!r}\n'
    s += f'  Zone={self.Zone!r}\n'
    s += f'  Ward={self.Ward!r}\n'
    s += f'  AddressNo={self.AddressNo!r}\n'
    s += f'  Street={self.Street!r}\n'
    s += f'  SupportDisability={self.SupportDisability!r}\n'
    s += f'  Status={self.Status!r}\n'
    s += f'  Lng={self.Lng!r}\n'
    s += f'  Lat={self.Lat!r}\n'
    s += f'  Search={self.Search!r}\n'
    s += f'  Routes={self.Routes!r}\n'
    s += ')'

    return s
  
  def __hash__(self):
    payload = (
      self.StopId,
      self.Code,
      self.Name,
      self.StopType,
      self.Zone,
      self.Ward,
      self.AddressNo,
      self.Street,
      self.SupportDisability,
      self.Status,
      self.Lng,
      self.Lat,
      self.Search,
      self.Routes,
    )
    return hash(payload)
  
  def to_dict(self):
    return {
      k[1:]: v
      for k, v in self.__dict__.items()
    }

  @property
  def StopId(self):
    return self._StopId
  @StopId.setter
  def StopId(self, value):
    self._StopId = value

  @property
  def Code(self):
    return self._Code
  @Code.setter
  def Code(self, value):
    self._Code = value

  @property
  def Name(self):
    return self._Name
  @Name.setter
  def Name(self, value):
    self._Name = value

  @property
  def StopType(self):
    return self._StopType
  @StopType.setter
  def StopType(self, value):
    self._StopType = value

  @property
  def Zone(self):
    return self._Zone
  @Zone.setter
  def Zone(self, value):
    self._Zone = value

  @property
  def Ward(self):
    return self._Ward
  @Ward.setter
  def Ward(self, value):
    self._Ward = value

  @property
  def AddressNo(self):
    return self._AddressNo
  @AddressNo.setter
  def AddressNo(self, value):
    self._AddressNo = value

  @property
  def Street(self):
    return self._Street
  @Street.setter
  def Street(self, value):
    self._Street = value

  @property
  def SupportDisability(self):
    return self._SupportDisability
  @SupportDisability.setter
  def SupportDisability(self, value):
    self._SupportDisability = value

  @property
  def Status(self):
    return self._Status
  @Status.setter
  def Status(self, value):
    self._Status = value

  @property
  def Lng(self):
    return self._Lng
  @Lng.setter
  def Lng(self, value):
    self._Lng = value

  @property
  def Lat(self):
    return self._Lat
  @Lat.setter
  def Lat(self, value):
    self._Lat = value

  @property
  def Search(self):
    return self._Search
  @Search.setter
  def Search(self, value):
    self._Search = value

  @property
  def Routes(self):
    return self._Routes
  @Routes.setter
  def Routes(self, value):
    self._Routes = value
