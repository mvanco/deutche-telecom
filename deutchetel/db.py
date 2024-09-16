import sqlite3
import click
from flask import current_app, g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("../schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def log_prediction(longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households,
                      median_income, ocean_proximity, y):
    get_db().execute(
        "INSERT INTO prediction (longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population,"
        " households, median_income, ocean_proximity, y)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households,
         median_income, ocean_proximity, y)
    )
    get_db().commit()


def get_history(size: int):
    result = get_db().execute(
        "SELECT *"
        " FROM prediction"
    )
    predictions = list(map(lambda x: list(x), result.fetchall()))
    columns = [desc[0] for desc in result.description]

    # Convert each row to a dictionary
    predictions = [dict(zip(columns, prediction)) for prediction in predictions]
    result = list(predictions)
    result.reverse()
    return result[:size]