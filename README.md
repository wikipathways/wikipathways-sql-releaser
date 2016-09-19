# wikipathways-sql-releaser

Python library to generate SQLite database for versioned WikiPathways data releases.

Get library:

```
git clone https://github.com/wikipathways/wikipathways-sql-releaser.git
cd wikipathways-api-client-py
```

Isolate environment:

```
workon wikipathways-sql-releaser
```

Install dependencies:

```
pip install -e .
```

Run (this isn't done, and it expects pathways.db not to already exist):

```
python wikipathways_sql_releaser/extract.py 
```

How to install a new dependency (`SQLAlchemy` in this example):

```
pip install SQLAlchemy
pip freeze > requirements.txt
```
