# Notes



## Object Relational Mapper(ORM)
- **Traditional way** : Fastapi can directly talks to DB using SQL
- **ORM** : 
    - Fastapi talks to ORM using Python
    - ORM talks to DB using SQL
### How do ORMs work?
- We can define our tables in our python code as models rather than doing it manually within postgres
- Queries are done via python code by calling corresponding methods and so no SQL is needed
- **Sqlalchemy** is one of the most popular python ORMS. Its a standalone library and it can be used with any python web frameworks or any python based application
## SQLAlchemy
### Steps
- Setup the unique URL to connect to the database. Every database has a specific type for it and it just a string
- Example connection string(URL) for postgres which needs to be passed to sqlalchemy
    - `SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'`