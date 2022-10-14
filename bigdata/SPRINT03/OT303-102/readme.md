
################################ Coorer Hadoop - Inicio ################################

# correr hadoop:

HADOOP_VERSION=3.3.4

cd ~/hadoop/hadoop-${HADOOP_VERSION}/

# corroborar que no haya nada corriendo:
sbin/stop-all.sh

bin/hdfs namenode -format

# si te dice que esta bloqueado el puerto 22:
sudo service ssh start

sudo service ssh restart

sbin/start-all.sh

# ya podrias entrar aca:
http://localhost:9870/dfshealth.html#tab-overview

# para pararlo:
sbin/stop-all.sh

# para verificar que este corriendo bien:
jps

# tenes que ver algo asi:
21186 NameNode

21330 DataNode

22661 Jps

21782 ResourceManager

21562 SecondaryNameNode

21931 NodeManager

# si alguno de estos no aparece es porque no esta corriendo y hay que arreglarlo

################################ Correr Hadoop - Fin ################################

# probamos subir un archivo de prueba a la raiz de nuestro hdfs:
hdfs dfs -put /mnt/c/Users/mcoutada/Downloads/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow/license.txt /

# creamos un directorio
hdfs dfs -mkdir -p /alkemybigdata

# ver los todo lo subido a hdfs:
hadoop fs -ls -R /alkemybigdata

# vemos:
drwxr-xr-x   - mcoutada supergroup          0 2022-10-12 15:37 /alkemybigdata

-rw-r--r--   1 mcoutada supergroup       1731 2022-10-12 15:33 /license.txt

# Vemos las primeras 5 lineas de nuestro archivo:
hdfs dfs -cat /license.txt | head -5

# subimos todos los archivos de bigdata (podes subir solo "posts.xml", es el unico que se necesita)

winfold="/mnt/c/Users/mcoutada/Downloads/Stack_Overflow_11-2010"

hdfs dfs -put $winfold /alkemybigdata


# verificamos que esten:
hadoop fs -ls -R /alkemybigdata

vemos:

drwxr-xr-x   - mcoutada supergroup          0 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow

-rw-r--r--   1 mcoutada supergroup    3498440 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/badges.xml

-rw-r--r--   1 mcoutada supergroup   30849022 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/comments.xml

-rw-r--r--   1 mcoutada supergroup       1731 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/license.txt

-rw-r--r--   1 mcoutada supergroup   89837591 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/posthistory.xml

-rw-r--r--   1 mcoutada supergroup   54792981 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/posts.xml

-rw-r--r--   1 mcoutada supergroup       4678 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/readme.txt

-rw-r--r--   1 mcoutada supergroup    7435967 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/users.xml

-rw-r--r--   1 mcoutada supergroup   27409310 2022-10-12 15:48 /alkemybigdata/112010_Meta_Stack_Overflow/votes.xml



# para eliminar todo en el hdfs:
hdfs dfs -rm -R -skipTrash /alkemybigdata/*


# testear sin hadoop:
cd /home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102

cat test.xml | ./mapper.py | ./reducer.py



# o tambien:

xmldir="/mnt/c/Users/mcoutada/Downloads/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow"

xml="$xmldir/posts.xml"

wkdir="/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102"

mapper="$wkdir/mapper3.py"

reducer="$wkdir/reducer3.py"

cat $xml | python $mapper | python $reducer






################ otros, mas adelante... ################

find ~ | grep --p "hadoop-streaming-$HADOOP_VERSION.jar"

find ~ | grep --p ".*hadoop.*streaming.*.jar"

HADOOPSTRJAR=/home/mcoutada/hadoop/hadoop-3.3.4/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar

hadoop jar $HADOOPSTRJAR \
    -input /alkemybigdata/posts.xml \
    -output /alkemybigdata/out.txt \
    -file mapper.py \
    -file reducer.py \
    -mapper ./mapper.py \
    -reducer ./reducer.py



sprint3 86 94 y 102
sprint4 110 118 y 126



from readme.txt:

   - **posts**.xml
       - Id
       - PostTypeId
          - 1: Question
          - 2: Answer
       - ParentID (only present if PostTypeId is 2)
       - AcceptedAnswerId (only present if PostTypeId is 1)
       - CreationDate
       - Score
       - ViewCount
       - Body
       - OwnerUserId
       - LastEditorUserId
       - LastEditorDisplayName="Jeff Atwood"
       - LastEditDate="2009-03-05T22:28:34.823"
       - LastActivityDate="2009-03-11T12:51:01.480"
       - CommunityOwnedDate="2009-03-11T12:51:01.480"
       - ClosedDate="2009-03-11T12:51:01.480"
       - Title=
       - Tags=
       - AnswerCount
       - CommentCount
       - FavoriteCount
