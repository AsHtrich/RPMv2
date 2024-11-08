import datetime as _dt
from typing import Optional
import pydantic as _pyd
from typing import List

class _UserBase(_pyd.BaseModel):
    email: str
    # name: str
    class Config:
        from_attributes =True
        

class UserCreate(_UserBase):
    hashed_password: str
    

    class Config:
        from_attributes =True
        

class User(_UserBase):
    uid: int
    

    class Config:
        from_attributes =True
        

# ---------------------------------------------

class _PatientBase(_pyd.BaseModel):
    patID: int
    docID: int
    deviceID: int
    name: str
    address: str
    email: str
    pno: int
    Relname: str
    Relpno: int
    desc: str
    age: int

class PatientCreate(_PatientBase):
    pass

class Patient(_PatientBase):
    pass

    class Config:
        from_attributes = True


# ---------------------------------------------

class _RelativeBase(_pyd.BaseModel):
    relID: int
    patID: int
    name: str
    address: str
    email: str
    pno: str

class RelativeCreate(_RelativeBase):
    pass

class Relatives(_RelativeBase):
    pass

    class Config:
        from_attributes = True


# ---------------------------------------------

class _DeviceBase(_pyd.BaseModel):
    deviceID: int
    patID: int
    battery: int
    status: str
    name: str

class DeviceCreate(_DeviceBase):
    pass

class Device(_DeviceBase):
    pass

    class Config:
        from_attributes = True


# ---------------------------------------------

class _SensorBase(_pyd.BaseModel):
    deviceID: int
    entryID: int
    timestamp: _dt.datetime
    hr: int
    temp: int

class SensorCreate(_SensorBase):
    pass

class Sensor(_SensorBase):
    pass

    class Config:
        from_attributes = True


# ---------------------------------------------

class _AlarmBase(_pyd.BaseModel):
    desc: str
    deviceID: int
    entryID: int
    alarmID: Optional[int]
    timestamp : _dt.datetime

class AlarmCreate(_AlarmBase):
    pass

class Alarms(_AlarmBase):
    pass
    
    class Config:
        from_attributes =True

# ---------------------------------------------

class _PrescBase(_pyd.BaseModel):
    patID: str
    date: str
    medication: str
    frequency: str
    dosage: str
    form: str  # form of medication (e.g., tablet, syrup)
    instructions: Optional[str] = None  # special instructions
    duration: str

    class Config:
        from_attributes = True

class PrescCreate(_PrescBase):
    pass

class Presc(_PrescBase):
    pid: int

    class Config:
        from_attributes = True

# ----------------------------------------------------------------------------------------------

class _RequestBase(_pyd.BaseModel):
    report: str
    

class RequestCreate(_RequestBase):
    pass

class Requests(_RequestBase):
    pass
    
    class Config:
        from_attributes =True

# -------------------------------------------------------------------------------------------------

class _AlertBase(_pyd.BaseModel):
    aid: int
    timestamp: _dt.datetime
    prediction: int
    values: List[float] 
    

class AlertCreate(_AlertBase):
    pass

class Alerts(_AlertBase):
    pass
    
    class Config:
        from_attributes =True