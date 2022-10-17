import pandas as pd
import io
#nombre y archivo que deseo extraer con pandas
jujuy_utn_df=pd.read_csv('UTN .csv')
jujuy_utn_df= normalize_data('UTN .csv')

#creo un archivo txt sobre ambas universidades

create_txt(jujuy_utn_df, "universidad tecnologica nacional")
df.show()

tres_de_febrero_df = pd.read_csv('universidad de tres de febrero result')
tres_de_febrero_df =normalize_data('universidad de tres de febrero result')
df.show()
#archivos ya creados en txt
create_txt(tres_de_febrero_df,"universidad tres de febrero")
create_txt(jujuy_utn_df,"universidad tecnologica nacional")