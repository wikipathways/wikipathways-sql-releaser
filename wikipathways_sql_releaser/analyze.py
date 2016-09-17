from sqlalchemy import create_engine

engine = create_engine('sqlite:///pathways.db')

with engine.connect() as con:
    rs = con.execute('SELECT * FROM nodes')

    for row in rs:
        print row
