jujuy_utn_df=pd.read_csv('UTN.csv')
jujuy_utn_df= normalize_data('UTN.csv')

create_txt(jujuy_utn_df, "universidad tecnologica nacional")
df.show()

tres_de_febrero_df = pd.read_csv('universidad tres de febrero')
tres_de_febrero_df =normalize_data('universidad tres de febrero')
df.show()

create_txt(tres_de_febrero_df,"universidad tres de febrero")