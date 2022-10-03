from decouple import config

# Datos para la conexión a la base de datos.
DB_USER = config('DB_USER')
PASSWORD = config('PASSWORD')
HOST = config('HOST')
PORT = config('PORT')
DB_NAME = config('DB_NAME')

# Datos de S3
CONNECTION = config('CONNECTION')
BUCKET_NAME = config('BUCKET_NAME')
