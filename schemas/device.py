from typing import Optional
import uuid
from pydantic import BaseModel


class DeviceModelBase(BaseModel):
    name: str



class DeviceModelCreate(DeviceModelBase):
    pass


class DeviceModelUpdate(DeviceModelBase):
    pass


class DeviceModelRead(DeviceModelBase):
    pass

    class Config:
        orm_mode = True


class DeviceTypeBase(BaseModel):
    name: str


class DeviceTypeRead(DeviceTypeBase):
    id: uuid.UUID
    device_model: DeviceModelRead

    class Config:
        orm_mode = True


class DeviceTypeCreate(DeviceTypeBase):
     device_model: DeviceModelRead


class DeviceTypeUpdate(DeviceTypeBase):
     device_model: DeviceModelRead


class DeviceManufacturerBase(BaseModel):
    device_manufacturer: str


class DeviceManufacturerRead(DeviceManufacturerBase):
    id: uuid.UUID
    inventary_number: str

    class Config:
        orm_mode = True


class DeviceManufacturerCreate(DeviceManufacturerBase):
     pass


class DeviceManufacturerUpdate(DeviceManufacturerBase):
     pass


class DeviceBase(BaseModel):
    device_type: DeviceTypeRead
    device_manufacturer: str
    device_model: DeviceModelRead
    inventary_number: Optional[str] | None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: uuid.UUID

    class Config:
        orm_mode = True