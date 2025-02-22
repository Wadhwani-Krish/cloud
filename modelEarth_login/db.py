from flask_sqlalchemy import SQLAlchemy

import pymysql
import click
from flask import current_app, g
db = SQLAlchemy()
def get_db():
    """Get a connection to the MySQL database."""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
        )
    return g.db

def close_db(e=None):
    """Close the MySQL database connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initialize the database by executing schema.sql."""
    connection = get_db()
    with current_app.open_resource('schema.sql') as f:
        sql_script = f.read().decode('utf8')
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
            for statement in sql_script.split(';'):  # Split script into individual statements
                statement = statement.strip()
                if statement:  # Skip empty statements
                    cursor.execute(statement)
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Re-enable foreign key checks
        connection.commit()
@click.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
