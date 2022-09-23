"""
https://alkemy-labs.atlassian.net/browse/OT303-46

Description

COMO: Analista de datos
QUIERO: Implementar SQL Operator
PARA: tomar los datos de las bases de datos en el DAG

Criterios de aceptación:
Configurar un Python Operators, para que extraiga información de la base de datos utilizando el .sql disponible en el repositorio base de las siguientes universidades:

Univ. Nacional Del Comahue

Universidad Del Salvador
Dejar la información en un archivo .csv dentro de la carpeta files.
"""
import sys

import include.logger as logger


def main(args):

    # Set the logger's log level
    logger.debug_flg = True if args[0:1] == ["DEBUG"] else False
    # Set the logger for this file
    log = logger.set_logger(logger_name=logger.get_rel_path(__file__))

    log.info("Start Main")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
