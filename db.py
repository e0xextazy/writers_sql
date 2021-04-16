import json
import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE writer (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) UNIQUE NOT NULL
        )
        """,
        """ CREATE TABLE book (
                id SERIAL PRIMARY KEY,
                author_id INTEGER NOT NULL,
                name VARCHAR(50) UNIQUE NOT NULL,
                FOREIGN KEY (author_id)
                    REFERENCES writer (id)
                )
        """)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def fill_tables():
    """ fill the table with initial data """
    commands = (
        """
        INSERT INTO writer(name)
	    VALUES('Толстой, Лев');
        """,
        """
        INSERT INTO writer(name)
	    VALUES('Пушкин, Александр');
        """,
        """
        INSERT INTO writer(name)
	    VALUES('Блок, Александр');
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Война и мир' FROM writer WHERE "name"='Толстой, Лев';
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Анна Каренина' FROM writer WHERE "name"='Толстой, Лев';
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Воскресение' FROM writer WHERE "name"='Толстой, Лев';
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Моцарт и Сальери ' FROM writer WHERE "name"='Пушкин, Александр';
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Пир во время чумы' FROM writer WHERE "name"='Пушкин, Александр';
        """,
        """
        INSERT INTO book (author_id, name)
	    SELECT "id", 'Роза и Крест' FROM writer WHERE "name"='Блок, Александр';
        """)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_writer_info(writer_id):
    """ get all info about writer """
    command = ("""
        SELECT
            w.name,
            b.id,
            b.name
        FROM
            writer w 
            JOIN book b ON w.id = b.author_id
        WHERE w.id = %s
        """)
    conn = None
    json_file = {}
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command, (writer_id,))
        data = cur.fetchall()
        if data:
            dic = {
                'id': writer_id,
                'name': data[0][0],
                'books': [{'id': book[1], 'name': book[2]} for book in data]
            }
            json_file = json.dumps(dic, ensure_ascii=False)
        else:
            json_file = json.dumps({'Error': 'Нет подходящих авторов!'}, ensure_ascii=False)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return json_file
