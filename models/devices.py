import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IDMixin, TimestampsMixin


class DeviceType(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    devices: Mapped['Device'] = relationship(back_populates='device_type')


class DeviceModel(Base, IDMixin):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicemanufacturers.id'), nullable=False)

    manufacturer: Mapped['DeviceManufacturer'] = relationship('DeviceManufacturer', back_populates='models')
    devices: Mapped['Device'] = relationship('Device', back_populates='model')


class DeviceManufacturer(Base, IDMixin):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # убрано model_id, т.к. связь с моделями — одно ко многим
    models: Mapped['DeviceModel'] = relationship('DeviceModel', back_populates='manufacturer', cascade="all, delete-orphan")
    devices: Mapped['Device'] = relationship('Device', back_populates='device_manufacturer')


class Device(Base, IDMixin, TimestampsMixin):

    inventary_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicetypes.id'), nullable=False)
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicemanufacturers.id'), nullable=False)
    model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('devicemodels.id'), nullable=False)
    rtobject_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rtobjects.id'), unique=True, nullable=True) 

    device_type: Mapped['DeviceType'] = relationship(back_populates='devices')
    device_manufacturer: Mapped['DeviceManufacturer'] = relationship(back_populates='devices')
    model: Mapped['DeviceModel'] = relationship(back_populates='devices')
    rtobject: Mapped['RTObject'] = relationship(back_populates='devices', uselist=False)


class RTObject(Base, IDMixin, TimestampsMixin):

    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    devices: Mapped['Device'] = relationship(back_populates='rtobject')
