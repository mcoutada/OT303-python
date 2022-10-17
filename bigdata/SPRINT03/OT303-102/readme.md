
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

<br>
<br>


# Subir archivos
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

### Testear sin hadoop (con un test.xml con un par de lineas de posts.xml):
```
cd /home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102/include
cat test.xml | python3 mapper1.py | python3 reducer1.py
```

### Nos devuelve:
```
1  feature-request     2
2  openid              2
3  status-declined     1
4  login               1
5  google              1
6  search              1
```

### O tambien podemos hacerlo con el posts.xml mas pequeño:
```
xmldir="/mnt/c/Users/asd/Downloads/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow"
xml="$xmldir/posts.xml"
wkdir="/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102/include"
mapper="$wkdir/mapper1.py"
reducer="$wkdir/reducer1.py"
cat $xml | python3 $mapper | python3 $reducer
```


### Nos devuelve:
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
10 questions           354
```

### Ya tenemos todos los archivos y hemos testeado... podemos correr con hadoop. Necesitamos confirmar que tenemos nuestro hadoop streaming jar

```
find ~ | grep --p ".*/lib/.*hadoop.*streaming.*.jar"
```
### Retorna:
```
/home/mcoutada/hadoop/hadoop-3.3.4/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar
```

# Correr Hadoop
### Ahora llamamos al jar pero con nuestro xml subido en hdfs, seteamos las variables necesarias:
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

### Debe retornar todo OK:
```
/home/mcoutada/hadoop/hadoop-3.3.4/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar: OK
/alkemybigdata/Stack_Overflow_11-2010/112010_Meta_Stack_Overflow/posts.xml: OK
/alkemybigdata/Stack_Overflow_11-2010/112010_Stack_Overflow/posts.xml: OK
/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102/mapper1.py: OK
/home/mcoutada/alkemy/OT303-python/bigdata/SPRINT03/OT303-102/reducer1.py: OK
```

### Eliminamos el directorio de salida si existe (Hadoop falla si existe de antemano)
```
hdfs dfs -rm -R -skipTrash $xmldir/output
```

### Corremos Hadoop
```
hadoop jar $hadoopstrjar \
 -input $big_xml \
 -output $xmldir/output \
 -mapper "python3 $mapper" \
 -reducer "python3 $reducer"
```

### Ejemplo de log:
```
packageJobJar: [/tmp/hadoop-unjar3674033946199609670/] [] /tmp/streamjob6990383775878498805.jar tmpDir=null
2022-10-16 20:36:43,532 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at /0.0.0.0:8032
2022-10-16 20:36:43,695 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at /0.0.0.0:8032
2022-10-16 20:36:43,917 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/mcoutada/.staging/job_1665599427989_0013
2022-10-16 20:36:44,136 INFO mapred.FileInputFormat: Total input files to process : 1
2022-10-16 20:36:44,221 INFO mapreduce.JobSubmitter: number of splits:31
2022-10-16 20:36:44,347 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1665599427989_0013
2022-10-16 20:36:44,347 INFO mapreduce.JobSubmitter: Executing with tokens: []
2022-10-16 20:36:44,510 INFO conf.Configuration: resource-types.xml not found
2022-10-16 20:36:44,510 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2022-10-16 20:36:44,580 INFO impl.YarnClientImpl: Submitted application application_1665599427989_0013
2022-10-16 20:36:44,626 INFO mapreduce.Job: The url to track the job: http://DESKTOP-02T1JP6.localdomain:8088/proxy/application_1665599427989_0013/
2022-10-16 20:36:44,627 INFO mapreduce.Job: Running job: job_1665599427989_0013
2022-10-16 20:36:50,705 INFO mapreduce.Job: Job job_1665599427989_0013 running in uber mode : false
2022-10-16 20:36:50,706 INFO mapreduce.Job:  map 0% reduce 0%
2022-10-16 20:37:00,869 INFO mapreduce.Job:  map 10% reduce 0%
2022-10-16 20:37:01,876 INFO mapreduce.Job:  map 19% reduce 0%
2022-10-16 20:37:09,985 INFO mapreduce.Job:  map 26% reduce 0%
2022-10-16 20:37:10,995 INFO mapreduce.Job:  map 32% reduce 0%
2022-10-16 20:37:12,018 INFO mapreduce.Job:  map 35% reduce 0%
2022-10-16 20:37:13,028 INFO mapreduce.Job:  map 39% reduce 0%
2022-10-16 20:37:19,090 INFO mapreduce.Job:  map 45% reduce 0%
2022-10-16 20:37:20,099 INFO mapreduce.Job:  map 48% reduce 0%
2022-10-16 20:37:21,111 INFO mapreduce.Job:  map 52% reduce 0%
2022-10-16 20:37:22,121 INFO mapreduce.Job:  map 55% reduce 0%
2022-10-16 20:37:27,162 INFO mapreduce.Job:  map 55% reduce 18%
2022-10-16 20:37:28,170 INFO mapreduce.Job:  map 65% reduce 18%
2022-10-16 20:37:31,188 INFO mapreduce.Job:  map 71% reduce 18%
2022-10-16 20:37:33,205 INFO mapreduce.Job:  map 71% reduce 24%
2022-10-16 20:37:36,230 INFO mapreduce.Job:  map 74% reduce 24%
2022-10-16 20:37:37,237 INFO mapreduce.Job:  map 81% reduce 24%
2022-10-16 20:37:38,243 INFO mapreduce.Job:  map 84% reduce 24%
2022-10-16 20:37:39,258 INFO mapreduce.Job:  map 87% reduce 28%
2022-10-16 20:37:43,292 INFO mapreduce.Job:  map 90% reduce 28%
2022-10-16 20:37:44,298 INFO mapreduce.Job:  map 94% reduce 28%
2022-10-16 20:37:45,303 INFO mapreduce.Job:  map 100% reduce 31%
2022-10-16 20:37:47,314 INFO mapreduce.Job:  map 100% reduce 100%
2022-10-16 20:37:48,328 INFO mapreduce.Job: Job job_1665599427989_0013 completed successfully
2022-10-16 20:37:48,449 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=12711072
                FILE: Number of bytes written=34320338
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=4085209361
                HDFS: Number of bytes written=300
                HDFS: Number of read operations=98
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters 
                Launched map tasks=31
                Launched reduce tasks=1
                Data-local map tasks=31
                Total time spent by all maps in occupied slots (ms)=246646
                Total time spent by all reduces in occupied slots (ms)=35838
                Total time spent by all map tasks (ms)=246646
                Total time spent by all reduce tasks (ms)=35838
                Total vcore-milliseconds taken by all map tasks=246646
                Total vcore-milliseconds taken by all reduce tasks=35838
                Total megabyte-milliseconds taken by all map tasks=252565504
                Total megabyte-milliseconds taken by all reduce tasks=36698112
        Map-Reduce Framework
                Map input records=3675852
                Map output records=1093439
                Map output bytes=10524188
                Map output materialized bytes=12711252
                Input split bytes=4402
                Combine input records=0
                Combine output records=0
                Reduce input groups=22992
                Reduce shuffle bytes=12711252
                Reduce input records=1093439
                Reduce output records=10
                Spilled Records=2186878
                Shuffled Maps =31
                Failed Shuffles=0
                Merged Map outputs=31
                GC time elapsed (ms)=5043
                CPU time spent (ms)=118050
                Physical memory (bytes) snapshot=11422498816
                Virtual memory (bytes) snapshot=81911959552
                Total committed heap usage (bytes)=10849615872
                Peak Map Physical memory (bytes)=381530112
                Peak Map Virtual memory (bytes)=2563854336
                Peak Reduce Physical memory (bytes)=301531136
                Peak Reduce Virtual memory (bytes)=2564349952
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters 
                Bytes Read=4085204959
        File Output Format Counters 
                Bytes Written=300
2022-10-16 20:37:48,449 INFO streaming.StreamJob: Output directory: /alkemybigdata/Stack_Overflow_11-2010/output
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
10 questions           354
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

### Ya tenemos todo para automatizarlo en un script python.
```
python3 main.py
```

### Y sus resultados se guardan en el log, se ha dejado el siguiente a modo de ejemplo.

```
/logs/OT303-102.log_ejemplo
```
---

 otros, mas adelante...


sprint3 86 94 y 102
sprint4 110 118 y 126