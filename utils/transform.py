import pandas as pd


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

    df['email'] = df['email'].str.lower()
    df['email'] = df['email'].replace(
        re_underscore, ' ').replace(re_whitespace, ' ').str.strip()

    return df
