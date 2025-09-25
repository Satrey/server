from typing import Optional, List
import uuid
from pydantic import BaseModel


# Схемы для работы с DeviceModel

class DeviceModelBase(BaseModel):
    name: str


class DeviceModelCreate(DeviceModelBase):
    manufacturer_id: uuid.UUID
    device_type_id: uuid.UUID

class DeviceModelUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer_id: Optional[uuid.UUID] = None
    device_type_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes=True

class DeviceModelResponse(DeviceModelBase):
    id: uuid.UUID
    manufacturer_id: uuid.UUID  # вложенный объект
    device_type_id: uuid.UUID

    class Config:
        from_attributes=True

# Схемы для работы с DeviceType

class DeviceTypeBase(BaseModel):
    name: str

class DeviceTypeCreate(DeviceTypeBase):
    pass

class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes=True

class DeviceTypeResponse(DeviceTypeBase):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes=True
     


# Схема для работы с DeviceManufacturer

class DeviceManufacturerBase(BaseModel):
    name: str

class DeviceManufacturerCreate(DeviceManufacturerBase):
    pass

class DeviceManufacturerUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes=True

class DeviceManufacturerResponse(DeviceManufacturerBase):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes=True


# Схемы для работы с Device

class DeviceBase(BaseModel):
    inventary_number: str
    model_id: uuid.UUID
    rtobject_id: Optional[uuid.UUID] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    inventary_number: Optional[str] = None
    model_id: Optional[uuid.UUID] = None
    rtobject_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes=True

class DeviceResponse(DeviceBase):
    id: uuid.UUID
    inventary_number: str
    model: Optional[DeviceModelResponse]

    class Config:
        from_attributes=True


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
        from_attributes=True

class RTObjectResponse(RTObjectBase):
    id: uuid.UUID
    devices: Optional[list[DeviceResponse]]

    class Config:
        from_attributes=True