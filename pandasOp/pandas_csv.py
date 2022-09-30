import pandas as pd
import io

jujuy_utn_df=pd.read_csv('UTN .csv')
jujuy_utn_df= normalize_data('UTN .csv')

create_txt(jujuy_utn_df, "universidad tecnologica nacional")
df.show()

tres_de_febrero_df = pd.read_csv('universidad de tres de febrero result')
tres_de_febrero_df =normalize_data('universidad de tres de febrero result')
df.show()

create_txt(tres_de_febrero_df,"universidad tres de febrero")