# %%
from sqlalchemy import create_engine
from sqlalchemy import text


# connection to database
# %%
user = 'user_group2'
password = 'n8RqKtxMFauVYD^u'
host = "37.32.5.76:3306"
db = 'group2'
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db}")
connection = engine.connect() 


# %%
with engine.connect().execution_options(compiled_cache=None) as conn:
    conn.execute(Place.select())
# %%
# select and use group2 database
connection.execute(text('use group2'))

tables = connection.execute(text('show tables;'))
tables.all()
# %%

from sqlalchemy import create_engine, Column, Integer, Unicode, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Place(Base):
    __tablename__ = 'Place'
    id = Column(Integer, primary_key=True)
    web_id = Column(Unicode(50))
    name = Column(Unicode(50))

class Locations(Base):
    __tablename__ = 'Locations'
    id = Column(Integer, primary_key=True)
    web_id = Column(Unicode(50))
    place_id = Column(Integer, ForeignKey('Place.id'))
    price_grade = Column(Integer)
    rating = Column(Integer)
    work_hour = Column(Integer)
    phone = Column(Integer)
    address = Column(String(255))
    latitude = Column(Integer)
    longtitude = Column(Integer)
    Place = relationship("Place", back_populates="Locations")


Place.Locations = relationship("Locations", order_by=Locations.id, back_populates="Place")

class Services(Base):
    __tablename__ = 'Services'
    id = Column(Integer, primary_key=True)
    web_id = Column(Unicode(50))
    name = Column(Unicode(50))

class Types(Base):
    __tablename__ = 'Types'
    id = Column(Integer, primary_key=True)
    web_id = Column(Unicode(50))
    name = Column(Unicode(50))

class Style(Base):
    __tablename__ = 'Style'
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('Types.id'))
    name = Column(Unicode(50))
    Type = relationship("Types", back_populates="Style")


Types.Style = relationship("Style", order_by=Style.id, back_populates="Types")

class menuItems(Base):
    __tablename__ = 'menuItems'
    id = Column(Integer, primary_key=True)
    web_id = Column(Unicode(50))
    name = Column(Unicode(50))


class places_menuItems (Base):
    __tablename__ = 'places_menuItems'
    id = Column(Integer, primary_key=True)
    places_menuItems_id = Column(Integer, ForeignKey('menuItems.id'))
    category = Column(Unicode(50))
    price = Column(Integer)
    menuItems = relationship("menuItems", back_populates="places_menuItems")

menuItems.places_menuItems = relationship("places_menuItems", order_by=Style.id, back_populates="menuItems")


class places_services (Base):
    __tablename__ = 'places_services'
    id = Column(Integer, primary_key=True)
    Services_id = Column(Integer, ForeignKey('Services.id'))

Services.places_services = relationship("places_services", order_by=Style.id, back_populates="Services")


class places_types_styles(Base):
    __tablename__ = 'places_types_styles'
    id = Column(Integer, primary_key=True)
    place_id = Column(Integer, ForeignKey('Place.id'))
    type_id = Column(Integer, ForeignKey('Types.id'))
    style_id = Column(Integer, ForeignKey('Style.id'))
    
    Place = relationship("Place", back_populates="places_types_styles")
    Types = relationship("Types", back_populates="places_types_styles")
    Style = relationship("Style", back_populates="places_types_styles")

Place.Types = relationship("Types", back_populates="Place")
Place.places_types_styles = relationship("places_types_styles", back_populates="Place")
Style.places_types_styles = relationship("places_types_styles",  back_populates="Style")
Types.places_types_styles = relationship("places_types_styles",  back_populates="Types")


Base.metadata.create_all(engine)

# %%
for table_name in Base.metadata.tables:
    print(table_name)



# %%
#Load data file and insert into database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String ,MetaData
import pandas as pd 

Session = sessionmaker(bind=engine)
session = Session()
# %%
with engine.connect().execution_options(compiled_cache=None) as conn:
    conn.execute(table.select())

# %%
# load data for Places table and insert into database
df = pd.read_csv('places.csv')

metadata = MetaData()
metadata.reflect(bind=engine)
Place = metadata.tables['Place']

# connection.execute(Place.insert().values(name=df['name']))

for index, row in df.iterrows():
    connection.execute(Place.insert().values(web_id=row['id'], name=row['name']))

# df[['id', 'name']].to_sql('Place', con=engine, if_exists='append', index=False)

# %%
result = session.query(Place).all()
for row in result:
    print(row)
# %%
import mysql.connector

mydb = mysql.connector.connect(
  host="37.32.5.76",
  user='user_group2',
  password='n8RqKtxMFauVYD^u',
  database='group2'
)

# %%
my = mydb.cursor()

my.execute("select * from Place")

myresult = my.fetchall()

for x in myresult:

    print(x)
# %%
metadata = MetaData()
metadata.reflect(bind=engine)
Place = metadata.tables['Place']

connection.execute(Place.insert().values(web_id="ali", name="123"))
# %%
