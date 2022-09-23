from decouple import config

# Datos para la conexión a la base de datos.
USER = config('alkymer2')
PASSWORD = config('Alkemy23')
HOST = config('training-main.cghe7e6sfljt.us-east-1.rds.amazonaws.com')
PORT = config('5432')
DB_NAME = config('training')