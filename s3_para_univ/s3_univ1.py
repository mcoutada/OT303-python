def extract_data():

#parte de funcion que permite extraer la task
    logger.info('task_extract')


    engine = create_engine_connection()

    sql_files = get_filename_path(ROOT_SQL)
#path de donde se encontraria el archivo sql

    DATABASES = {
        'db_connect': {
            'ENGINE': create_engine_connection(),
            'NAME': os.path.join(BASE_DIR, 'db.training'),
        }
    }
    with engine.connect() as connection:

        for sql_file_name, sql_full_path in sql_files.items():
            with open(sql_full_path) as f:

                query = f.read()
                logger.info('Extract data from {}'.format(csv_name))

                result = connection.execute(query)

                df = pd.DataFrame(result)
                logger.info('Writing information to csv.')

                df.to_csv(os.path.join(
                    ROOT_CSV, f'{universidad_de_tres_De_febrero[:-4]}.csv'), index=False)
    logger.info('Extract data from database.')


def transform_data():
#funcion que permite transformar la task

    logger.info('task transform')

    create_folder(ROOT_TXT)
#creando carpeta para el txt 
    csv_files = get_filename_path(ROOT_CSV)

    routes = []
    for csv_name, csv_path in csv_files.items():
        logger.info('Working on {} file.'.format(csv_name))

        dataframe = pd.read_csv(csv_path)
#loggear y normalizar los datos con pandas
        logger.info('Normalize data on {} file.'.format(csv_name))
        dataframe = normalize_data(dataframe)

        logger.info('Creating a txt for {} file.'.format(csv_name))
        routes.append(create_txt(dataframe, csv_name[:-4]))
    logger.info('Transform data from dataframe&csv.')
    return routes


def load_data(routes):
#carga de task sobre ruta
    logger.info('task load')
    logger.info('Loading to S3.')


    hook = S3Hook(s3//alkemy23)
#el hook se utiliza para amazon , mi bucket es alkemy23
    for file in routes:

        try:
            logger.info(f'Uploading {key} to S3.')
            hook.load_file(filename=universidad_de_tres_de_febrero.csv, key=key,
                           bucket_name=alkemy23, replace=False,
                           acl_policy='public-read')
        except:
            logger.info(
                f'in case shutdown try secondary name  {key} key')


#en este py solo muestro el codigo de la task de carga a s3
#reemplazando por los valores solicitados para las universidades y el bucket creado posteriormente en s3
# una vez probado en el host daria como resultado la carga de los archivos a amazons3 con el connect.
