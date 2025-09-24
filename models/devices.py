import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IDMixin, TimestampsMixin


class DeviceType(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Вариант ИИ
    # devices: Mapped['Device'] = relationship('Device', back_populates='device_type', viewonly=True)  # Через модель не напрямую?
    models: Mapped['DeviceModel'] = relationship('DeviceModel', back_populates='device_type')


class DeviceManufacturer(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Вариант ИИ
    # devices: Mapped['Device'] = relationship('Device', back_populates='device_manufacturer', viewonly=True)  # Через модель не напрямую?
    models: Mapped['DeviceModel'] = relationship('DeviceModel', back_populates='manufacturer')


class DeviceModel(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)   
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicemanufacturers.id'), nullable=True)
    device_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicetypes.id'), nullable=True)
    
    manufacturer: Mapped['DeviceManufacturer'] = relationship('DeviceManufacturer', back_populates='models')
    device_type: Mapped['DeviceType'] = relationship('DeviceType', back_populates='models')
    devices: Mapped['Device'] = relationship('Device', back_populates='model')
    


class Device(Base, IDMixin, TimestampsMixin):

    inventary_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicemodels.id'), nullable=False)
    rtobject_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rtobjects.id'), nullable=True) 

    model: Mapped['DeviceModel'] = relationship('DeviceModel', back_populates='devices')
    rtobject: Mapped['RTObject'] = relationship('RTObject', back_populates='devices', uselist=True)

    @property
    def device_type(self) -> 'DeviceType | None':
        return self.model.device_type if self.model else None

    @property
    def device_manufacturer(self) -> 'DeviceManufacturer | None':
        return self.model.device_manufacturer if self.model else None


class RTObject(Base, IDMixin, TimestampsMixin):

    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    devices: Mapped['Device'] = relationship(back_populates='rtobject')
