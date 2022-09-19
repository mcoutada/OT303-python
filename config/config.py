from decouple import config

# Datos para la conexión a la base de datos.
USER = config('USER')
PASSWORD = config('PASSWORD')
HOST = config('SERVER')
PORT = config('PORT')
DB_NAME = config('DB_NAME')
