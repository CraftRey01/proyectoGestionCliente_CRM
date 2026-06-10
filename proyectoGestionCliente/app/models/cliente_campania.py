from app.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class ClienteCampania(Base):
    __tablename__ = "cliente_campania"

    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), primary_key=True)
    id_campania = Column(Integer, ForeignKey("campania.id_campania"), primary_key=True)

    cliente = relationship("Cliente", back_populates="campanias")
    campania = relationship("Campania", back_populates="clientes")
