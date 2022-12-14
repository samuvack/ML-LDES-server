# Note: the module name is psycopg, not psycopg3
import psycopg

# Connect to an existing database
with psycopg.connect("dbname=iow user=postgres") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        cur.fetchone()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            print(record)

        # Make the changes to the database persistent
        conn.commit()

        users = [
            ("James", 25, "male", "USA"),
            ("Leila", 32, "female", "France"),
            ("Brigitte", 35, "female", "England"),
            ("Mike", 40, "male", "Denmark"),
            ("Elizabeth", 21, "female", "Canada"),
            ]

        user_records = ", ".join(["%s"] * len(users))

        insert_query = (
            f"INSERT INTO users (name, age, gender, nationality) VALUES {user_records}"
        )

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(insert_query, users)


