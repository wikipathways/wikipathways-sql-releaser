import os.path
# import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
# from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.sql import text


# create or get
def init_pathways_engine():
    location = 'pathways.db'
    connection_string = 'sqlite:///' + location
    engine = create_engine(connection_string)

    if os.path.isfile(location):
        return engine

    metadata = MetaData()
    Table('nodes', metadata,
          Column('id', String, primary_key=True),
          Column('label', String),
          Column('source', String),
          )
    Table('edges', metadata,
          Column('id', String, primary_key=True),
          Column('source_id', String, ForeignKey('nodes.id')),
          Column('target_id', String, ForeignKey('nodes.id')),
          )
    metadata.create_all(engine)
    # keeping this here in case I need it again
    inspector = inspect(engine)
    print inspector.get_columns('edges')
    return engine


def load(data):
    print 'data'
    print data
    engine = init_pathways_engine()
    with engine.connect() as con:
        statement = text('''INSERT INTO nodes(id, label, source)
                            VALUES(:id, :label, :source)''')

        for line in data:
            con.execute(statement, **line)

        rs = con.execute('SELECT * FROM nodes')

        for row in rs:
            print row


# data = ({'id': 'http://identifiers.org/cas/6912-68-1',
#          'label': 'b-Alanine',
#          'source': 'Enzyme Nomenclature'},
#         {'id': 'http://identifiers.org/ec-code/2.1.3.2',
#          'label': '2.1.3.2',
#          'source': 'Enzyme Nomenclature'},
#         )
# load(data)
