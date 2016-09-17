import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

metadata = MetaData()
nodes = Table('nodes', metadata,
              Column('id', String, primary_key=True),
              Column('label', String),
              Column('source', String),
              )

engine = create_engine('sqlite:///pathways.db')
metadata.create_all(engine)

inspector = inspect(engine)
# print inspector.get_columns('nodes')

with engine.connect() as con:
    data = ({'id': 'http://identifiers.org/cas/6912-68-1',
             'label': 'b-Alanine',
             'source': 'Enzyme Nomenclature'},
            {'id': 'http://identifiers.org/ec-code/2.1.3.2',
             'label': '2.1.3.2',
             'source': 'Enzyme Nomenclature'},
            )

    statement = text('''INSERT INTO nodes(id, label, source) VALUES(:id, :label, :source)''')

    for line in data:
        con.execute(statement, **line)

    rs = con.execute('SELECT * FROM nodes')

    for row in rs:
        print row
