from typing import Optional
import uuid
from pydantic import BaseModel


# Схемы для работы с DeviceModel

class DeviceModelBase(BaseModel):
    name: str
    manufacturer_id: uuid.UUID

class DeviceModelCreate(DeviceModelBase):
    pass

class DeviceModelUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer_id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True

class DeviceModelResponse(DeviceModelBase):
    id: uuid.UUID
    manufacturer: Optional['DeviceManufacturerResponse']  # вложенный объект

    class Config:
        orm_mode = True

# Схемы для работы с DeviceType

class DeviceTypeBase(BaseModel):
    name: str

class DeviceTypeCreate(DeviceTypeBase):
    pass

class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True

class DeviceTypeResponse(DeviceTypeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
     


# Схема для работы с DeviceManufacturer

class DeviceManufacturerBase(BaseModel):
    name: str

class DeviceManufacturerCreate(DeviceManufacturerBase):
    pass

class DeviceManufacturerUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True

class DeviceManufacturerResponse(DeviceManufacturerBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# Схемы для работы с Device

class DeviceBase(BaseModel):
    inventary_number: str
    type_id: uuid.UUID
    manufacturer_id: uuid.UUID
    model_id: uuid.UUID
    rtobject_id: Optional[uuid.UUID] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    inventary_number: Optional[str] = None
    type_id: Optional[uuid.UUID] = None
    manufacturer_id: Optional[uuid.UUID] = None
    model_id: Optional[uuid.UUID] = None
    rtobject_id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True

class DeviceResponse(DeviceBase):
    id: uuid.UUID
    device_type: Optional[DeviceTypeResponse]
    manufacturer: Optional[DeviceManufacturerResponse]
    model: Optional[DeviceModelResponse]
    rtobject: Optional['RTObjectResponse']

    class Config:
        orm_mode = True


# Схемы для работы с RTObject

class RTObjectBase(BaseModel):
    number: int
    address: str

class RTObjectCreate(RTObjectBase):
    pass

class RTObjectUpdate(BaseModel):
    number: Optional[int] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True

class RTObjectResponse(RTObjectBase):
    id: uuid.UUID
    number: int
    address: str
    # devices: Optional[list] = []  # Можно указать список устройств

    class Config:
        orm_mode = True