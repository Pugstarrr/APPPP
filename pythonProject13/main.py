from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, nullable=False)

engine = create_engine('sqlite:///inventory.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
