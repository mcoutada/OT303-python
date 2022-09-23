import pandas as pd
'''
TASK ID: OT303-61

COMO: Analista de datos
QUIERO: Crear una función Python con Pandas para cada universidad
PARA: poder normalizar los datos de las mismas

Criterios de aceptación: 
Una funcion que devuelva un txt para cada una de las siguientes universidades con los datos normalizados:
Universidad De Flores
Universidad Nacional De Villa María

Datos Finales:
university: str minúsculas, sin espacios extras, ni guiones
career: str minúsculas, sin espacios extras, ni guiones
inscription_date: str %Y-%m-%d format
first_name: str minúscula y sin espacios, ni guiones
last_name: str minúscula y sin espacios, ni guiones
gender: str choice(male, female)
age: int
postal_code: str
location: str minúscula sin espacios extras, ni guiones
email: str minúsculas, sin espacios extras, ni guiones

Aclaraciones:
Para calcular codigo postal o locación se va a utilizar el .csv que se encuentra en el repo.
La edad se debe calcular en todos los casos

Las aclaraciones se tuvieron en cuenta en las consultas sql.
'''
# Aclaración: ambas universidades tienen el mismo formato, la edad y la localidad/codigo postal
# fueron calculadas mediante la query.


def normalize_data(df: pd.DataFrame):
    """Normalize data from pandas dataframe.

    Args:
        df (pd.DataFrame): input dataframe.

    Returns:
        pd.DataFrame: clear dataframe.
    """
    # Regular expressions.
    # strip() remove white spaces at end or beginning.
    # lower() string to lowercase.
    # r"\s+" Pattern whitespace
    re_underscore = r'(_|-)'
    re_whitespace = r'\s+'

    # University
    df['university'] = df['university'].str.lower()
    df['university'] = df['university'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()
    # Career
    df['career'] = df['career'].str.lower()
    df['career'] = df['career'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()
    # Inscription Date.
    # The date is in the correct format. Meanwhile, the correct way to format is:
    # Convert object to datetime.
    df['inscription_date'] = pd.to_datetime(df['inscription_date'])
    df['inscription_date'] = df['inscription_date'].dt.strftime('%Y-%m-%d')
    # First name.
    df['first_name'] = df['first_name'].str.lower()
    df['first_name'] = df['first_name'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()
    # Last name.
    df['last_name'] = df['last_name'].str.lower()
    df['last_name'] = df['last_name'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()
    # Gender.
    df['gender'] = df['gender'].replace(['F', 'M'], ['female', 'male'])
    # Age. #np.int8 or np.int16 less memory usage.
    df['age'] = df['age'].astype(dtype=np.int16)
    # Postal code.
    df['postal_code'] = df['postal_code'].astype('str')
    # Location.
    df['location'] = df['location'].str.lower()
    df['location'] = df['location'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()
    # Email.
    df['email'] = df['email'].str.lower()
    df['email'] = df['email'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()

    return df
