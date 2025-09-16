from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.mixins import IDMixin, TimestampsMixin


class DeviceType(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    devices: Mapped['Device'] = relationship(
        back_populates='device_type'
    )


class DeviceModel(Base, IDMixin):

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    devices: Mapped['Device'] = relationship(
        back_populates='device_model',
    )


class DeviceManufacturer(Base, IDMixin):

    manufacturer: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class Device(Base, IDMixin, TimestampsMixin):

    device_manufacturer: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    inventary_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)

    type_id: Mapped['DeviceType'] = mapped_column(Integer, ForeignKey('devicetypes.id'), nullable=False)
    manufacturer_id: Mapped['DeviceManufacturer'] = mapped_column(Integer, ForeignKey('devicemanufacturers.id'))
    model_id: Mapped['DeviceModel'] = mapped_column(Integer, ForeignKey('devicemodels.id'), nullable=False)

    device_type: Mapped['DeviceType'] = relationship(back_populates='devices')
    device_manufacturer: Mapped['DeviceManufacturer'] = relationship(back_populates='manufacturer')
    device_model: Mapped['DeviceModel'] = relationship(back_populates='devices')