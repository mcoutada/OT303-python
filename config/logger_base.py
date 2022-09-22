import logging as log

# Haciendo las configuraciones del log para usarlo en el DAG.
log.basicConfig(level = log.DEBUG, 
                format = '%(asctime)s: %(levelname)s [%(filename)s: %(lineno)s] %(message)s',
                datefmt = '%Y-%m-%d %I:%M:%S %p')
