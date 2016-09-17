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

Install a new dependency (`SQLAlchemy` in this example):

```
pip install SQLAlchemy
pip freeze > requirements.txt
```
