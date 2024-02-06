import os

from dotenv import load_dotenv
import psycopg


load_dotenv()


async def get_conn():
    with psycopg.connect(
        conninfo=os.environ["POSTGRES_INFO"],
    ) as conn:
        yield conn
        conn.close()
