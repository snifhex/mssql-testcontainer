# mssql-testcontainer

The `mssql-testcontainer` package provides a simple and convenient way to spin up a SQL Server container for testing purposes. It utilizes the docker library and PyODBC to create and manage the container, allowing you to connect to the SQL Server instance within your Python tests.

## Installation

You can install `mssql-testcontainer` using `pip`:

```bash
pip install mssql-testcontainer
```

## Usage

The package exposes the `SQLServerContainer` class, which you can use as a context manager to automatically manage the lifecycle of the SQL Server container. Here's an example of how to use it:

### Simple Usage with Context Manager

```python
import sqlalchemy
from mssql_testcontainer import SQLServerContainer

with SqlServerContainer() as mssql:
    engine = sqlalchemy.create_engine(mssql.get_connection_url())
    with engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("select @@VERSION"))
        print(result)

# The container will be automatically stopped and removed after the 'with' block

```

### Usage with Pytest Fixtures

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mssql_testcontainer import SQLServerContainer

@pytest.fixture(scope="session")
def session():
    with SQLServerContainer() as mssql:
        engine = create_engine(mssql.get_connection_url(), fast_executemany=True)
        YourModel.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        with Session() as session:
            yield session
```
