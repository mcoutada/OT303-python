
---
---

# Correr hadoop:
```
HADOOP_VERSION=3.3.4
cd ~/hadoop/hadoop-${HADOOP_VERSION}/
```

### Corroborar que no haya nada corriendo:
```
sbin/stop-all.sh
bin/hdfs namenode -format
```

### Si te dice que esta bloqueado el puerto 22:
```
sudo service ssh start
sudo service ssh restart
sbin/start-all.sh
```
### Ya podrias entrar aca:
http://localhost:9870/dfshealth.html#tab-overview

### Para pararlo:
```
sbin/stop-all.sh
```

### Para verificar que este corriendo bien:
```
jps
```
### Tenes que ver algo asi:
```
21186 NameNode
21330 DataNode
22661 Jps
21782 ResourceManager
21562 SecondaryNameNode
21931 NodeManager
```

### Si alguno de estos no aparece es porque no esta corriendo y hay que arreglarlo

---
---
 Correr Hadoop - Fin 
 
---
---

### Probamos subir un archivo de prueba a la raiz de nuestro hdfs:
```
hdfs dfs -put /mnt/c/Users/mcoutada/Downloads/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow/license.txt /
```
### Creamos un directorio
```
hdfs dfs -mkdir -p /alkemybigdata
```
### Ver los todo lo subido a hdfs:
```
hadoop fs -ls -R /
```
### Vemos:
```
drwxr-xr-x   - mcoutada supergroup          0 2022-10-12 15:37 /alkemybigdata
-rw-r--r--   1 mcoutada supergroup       1731 2022-10-12 15:33 /license.txt
```
### Vemos las primeras 5 lineas de nuestro archivo:
```
hdfs dfs -cat /license.txt | head -5
```

### Subimos todos los archivos de bigdata (podes subir solo "posts.xml", es el unico que se necesita)
```
winfold="/mnt/c/Users/asd/Downloads/Stack_Overflow_11-2010"
hdfs dfs -put $winfold /alkemybigdata
```

### Verificamos que esten:
```
hadoop fs -ls -R /alkemybigdata
```

### Vemos:
```
drwxr-xr-x   - mcoutada supergroup          0 2022-10-14 13:26 /alkemybigdata/Stack_Overflow_11-2010
drwxr-xr-x   - mcoutada supergroup          0 2022-10-14 13:26 /alkemybigdata/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow
-rw-r--r--   1 mcoutada supergroup   54792981 2022-10-14 13:26 /alkemybigdata/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow/posts.xml
drwxr-xr-x   - mcoutada supergroup          0 2022-10-14 13:30 /alkemybigdata/Stack_Overflow_11-2010/112010_Stack_Overflow
-rw-r--r--   1 mcoutada supergroup 4085073887 2022-10-14 13:30 /alkemybigdata/Stack_Overflow_11-2010/112010_Stack_Overflow/posts.xml
```
### Si quisieramos eliminar todo en el hdfs:
```
hdfs dfs -rm -R -skipTrash /alkemybigdata/*
```

### Testear sin hadoop (crear un test.xml con un par de lineas de posts.xml):
```
cd /home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102
cat test.xml | python3 mapper.py | python3 reducer.py
```

### O tambien:
```
xmldir="/mnt/c/Users/mcoutada/Downloads/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow"
xml="$xmldir/posts.xml"
wkdir="/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102"
mapper="$wkdir/mapper3.py"
reducer="$wkdir/reducer3.py"
cat $xml | python3 $mapper | python3 $reducer
```

### Ya tenemos todos los archivos y hemos testeado... podemos correr con hadoop. Necesitamos confirmar que tenemos nuestro hadoop streaming jar

```
find ~ | grep --p ".*/lib/.*hadoop.*streaming.*.jar"
```

### Ahora llamamos al jar pero con nuestro xml subido en hdfs
```
hadoopstrjar=$(find ~ | grep --p ".*/lib/.*hadoop.*streaming.*.jar")
xmldir="/alkemybigdata/Stack_Overflow_11-2010"
small_xml="$xmldir/112010_Meta_Stack_Overflow/posts.xml"
big_xml="$xmldir/112010_Stack_Overflow/posts.xml"
wkdir="/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102"
mapper="$wkdir/mapper1.py"
reducer="$wkdir/reducer1.py"
```

### Verificamos si las variables estan bien asignadas
```
if [ -f $hadoopstrjar ]; then echo $hadoopstrjar: OK; else echo $hadoopstrjar: NOT FOUND; fi
if hdfs dfs -test -f $small_xml; then echo $small_xml: OK; else echo $small_xml: NOT FOUND; fi
if hdfs dfs -test -f $big_xml; then echo $big_xml: OK; else echo $big_xml: NOT FOUND; fi
if [ -f $mapper ]; then echo $mapper: OK; else echo $mapper: NOT FOUND; fi
if [ -f $reducer ]; then echo $reducer: OK; else echo $reducer: NOT FOUND; fi
```

### Eliminamos el archivo de salida si existe
```
hdfs dfs -rm -R -skipTrash $xmldir/output
```

### Corremos Hadoop
```
hadoop jar $hadoopstrjar \
 -input $big_xml \
 -output $xmldir/output \
 -mapper "python $mapper" \
 -reducer "python $reducer"
```

### Chequeamos el contenido
```
hdfs dfs -cat $xmldir/output/part-00000 | head -10
```


### Small file:
```
1  discussion          2912
2  feature-request     2814
3  bug                 1396
4  support             1261
5  stackoverflow       848
6  status-completed    647
7  tags                524
8  reputation          426
9  area51              372
10 questions           354`
```

### Big file:
```
1  c#                  35996
2  java                26921
3  iphone              23215
4  php                 21418
5  asp.net             20252
6  javascript          19320
7  .net                17249
8  jquery              15376
9  android             13132
10 c++                 12856
```

---
---

 otros, mas adelante...


sprint3 86 94 y 102
sprint4 110 118 y 126