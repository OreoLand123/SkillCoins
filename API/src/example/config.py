import os

user = 'postgres'
password = '1913131'
host = 'postgres'
database = 'example'
port = '5432'

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
