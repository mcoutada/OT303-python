"""
https://alkemy-labs.atlassian.net/browse/OT303-38

COMO: Analista de datos
QUIERO: Configurar los log
PARA: Mostrarlos en consola

Criterios de aceptación:

Configurar logs para Univ. Nacional Del Comahue

Configurar logs para Universidad del Salvador

Utilizar la librería de Loggin de python: https://docs.python.org/3/howto/logging.html

Realizar un log al empezar cada DAG con el nombre del logger

Formato del log: %Y-%m-%d - nombre_logger - mensaje
Aclaración:
Deben dejar la configuración lista para que se pueda incluir dentro de las funciones futuras. No es necesario empezar a escribir logs.
"""
import sys

import include.logger as logger


def main(args):

    # Set the logger's log level
    logger.debug_flg = True if args[0:1] == ["DEBUG"] else False
    # Set the logger for this file
    log = logger.set_logger(logger_name=logger.get_rel_path(__file__))

    log.info(f"Start {log.name}")

    # This is left on purpose to test the additional functionality of logging
    # an error
    a = 1 / 0


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
