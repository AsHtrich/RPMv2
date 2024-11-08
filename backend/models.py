import passlib.hash as _hash
from datetime import datetime as _dt
import sqlalchemy as _sql
import database as _database

# Users Table
class Users(_database.Base):
    __tablename__ = "users"
    uid = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    hashed_password = _sql.Column(_sql.String)
    # name = _sql.Column(_sql.String)
    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


# Patients Table
class Patients(_database.Base):
    __tablename__ = "patients"
    patID = _sql.Column(_sql.Integer, primary_key=True, unique=True)
    docID = _sql.Column(_sql.Integer, _sql.ForeignKey("users.uid"), index=True)
    deviceID = _sql.Column(_sql.Integer, _sql.ForeignKey("devices.deviceID"), index=True)
    name = _sql.Column(_sql.String)
    address = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String)
    pno = _sql.Column(_sql.Integer)
    Relname = _sql.Column(_sql.String)
    Relpno = _sql.Column(_sql.Integer)
    desc = _sql.Column(_sql.String)
    age = _sql.Column(_sql.Integer)



# Devices Table
class Devices(_database.Base):
    __tablename__ = "devices"
    deviceID = _sql.Column(_sql.Integer, primary_key=True, unique=True)
    patID = _sql.Column(_sql.Integer, _sql.ForeignKey("patients.patID"), index=True)
    battery = _sql.Column(_sql.Integer)
    status = _sql.Column(_sql.String)
    name = _sql.Column(_sql.String)


# Sensors Table
class Sensors(_database.Base):
    __tablename__ = "sensors"
    entryID = _sql.Column(_sql.Integer, primary_key=True, unique=True)
    deviceID = _sql.Column(_sql.Integer, _sql.ForeignKey("devices.deviceID"), index=True)
    timestamp = _sql.Column(_sql.DateTime, default=_dt.now().isoformat())
    hr = _sql.Column(_sql.Integer)  # heart rate
    temp = _sql.Column(_sql.Integer)  # temperature


# Alarms Table
class Alarms(_database.Base):
    __tablename__ = "alarms"
    alarmID = _sql.Column(_sql.Integer, primary_key=True, unique=True)
    deviceID = _sql.Column(_sql.Integer, _sql.ForeignKey("devices.deviceID"), index=True)
    entryID = _sql.Column(_sql.Integer, _sql.ForeignKey("sensors.entryID"), index=True)
    desc = _sql.Column(_sql.String)
    timestamp = _sql.Column(_sql.DateTime, default=_dt.now().isoformat())

# Prescription Table
class Prescs(_database.Base):
    __tablename__ = "prescriptions"
    pid = _sql.Column(_sql.Integer, primary_key=True, index=True)
    patID = _sql.Column(_sql.String,index=True)
    date = _sql.Column(_sql.String)
    medication = _sql.Column(_sql.String)
    frequency = _sql.Column(_sql.String)
    dosage = _sql.Column(_sql.String)
    form = _sql.Column(_sql.String)  
    instructions = _sql.Column(_sql.String)  
    duration = _sql.Column(_sql.String)  

# Requests Table
class Requests(_database.Base):
    __tablename__ = "requests"
    report = _sql.Column(_sql.String, primary_key=True, index=True)

class Alerts(_database.Base):
    __tablename__ = "alerts"
    aid = _sql.Column(_sql.Integer, primary_key=True, index=True)
    timestamp = _sql.Column(_sql.DateTime, default=_dt.now().isoformat())
    prediction = _sql.Column(_sql.Integer)
    values = _sql.Column(_sql.JSON) 
