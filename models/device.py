import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IDMixin, TimestampsMixin


class DeviceType(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    device: Mapped['Device'] = relationship(
        back_populates='device_type'
    )


class DeviceModel(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    model: Mapped['DeviceManufacturer'] = relationship(
        back_populates='model',
    )


class DeviceManufacturer(Base, IDMixin):

    manufacturer: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    model_id: Mapped['DeviceModel'] = mapped_column(ForeignKey('devicemodels.id'))

    device: Mapped['Device'] = relationship(
        back_populates='device_manufacturer'
    )
    model: Mapped['DeviceModel'] = relationship(back_populates='model')


class Device(Base, IDMixin, TimestampsMixin):

    device_manufacturer: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    inventary_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    type_id: Mapped['DeviceType'] = mapped_column(ForeignKey('devicetypes.id'), nullable=False)
    manufacturer_id: Mapped['DeviceManufacturer'] = mapped_column(ForeignKey('devicemanufacturers.id'))
    

    device_type: Mapped['DeviceType'] = relationship(back_populates='device')
    device_manufacturer: Mapped['DeviceManufacturer'] = relationship(back_populates='device')
   