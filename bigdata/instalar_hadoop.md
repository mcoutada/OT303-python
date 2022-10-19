
# Instalar Hadoop

Yo he seguido principalmente esta guía, consultarla si quieren más detalles pero recomiendo seguir mis comandos ya que facilité algunos pasos.
https://kontext.tech/article/978/install-hadoop-332-in-wsl-on-windows

Primero, actualizar todo nuestro Ubuntu:
```
sudo -- sh -c 'apt-get update; apt-get upgrade -y; apt-get full-upgrade -y; apt-get autoremove -y; apt-get autoclean -y'
```


Correr:
```
sudo apt install -y default-jre
sudo apt install -y openjdk-11-jre-headless
sudo apt install -y openjdk-8-jre-headless
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y ca-certificates
```

Ver última versión y actualizar $HADOOP_VERSION abajo si hace falta:
https://hadoop.apache.org/releases.html

Correr:
```
HADOOP_VERSION=3.3.4
wget https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
mkdir ~/hadoop
tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz -C ~/hadoop
rm -f ~/hadoop-${HADOOP_VERSION}.tar.gz
cd ~/hadoop/hadoop-${HADOOP_VERSION}/
sudo apt install ssh 
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```


Correr:
```
code ~/.bashrc
```

Copiar:
```
HADOOP_HOME=/home/mcoutada/hadoop/hadoop-3.3.4
HADOOP_INSTALL=$HADOOP_HOME
HADOOP_MAPRED_HOME=$HADOOP_HOME
HADOOP_COMMON_HOME=$HADOOP_HOME
HADOOP_HDFS_HOME=$HADOOP_HOME
YARN_HOME=$HADOOP_HOME
HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

Pegar al final...

correr:
```
source ~/.bashrc
```

correr:
```
code $HADOOP_HOME/etc/hadoop/hadoop-env.sh
```

cambiar:
```
# export JAVA_HOME=
```

por
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

o por
```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```
Podemos ver nuestro default java asi
```
readlink -f /usr/bin/java | sed "s:bin/java::"
```

tambien se puede dejar dinamico:
```
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
```

Yo por ahora deje este:
```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

correr:
```
code etc/hadoop/core-site.xml
```

Reemplazar:
```
<configuration>
</configuration>
```

Por:
```
<configuration>
     <property>
         <name>fs.defaultFS</name>
         <value>hdfs://localhost:9000</value>
     </property>
</configuration>
```

correr:
```
HADOOP_VERSION_WO_DOTS=${HADOOP_VERSION//[-._]/}
NAME_DIR=~/hadoop/dfs/name$HADOOP_VERSION_WO_DOTS
DATA_DIR=~/hadoop/dfs/data$HADOOP_VERSION_WO_DOTS
mkdir -p $NAME_DIR
mkdir -p $DATA_DIR
```

Corre esto para ver lo que tienen las variables, lo necesitas en el prox paso:
```
echo $NAME_DIR
echo $DATA_DIR
```

correr:
```
code etc/hadoop/hdfs-site.xml
```

Reemplazar:
```
<configuration>

</configuration>
```

Por (PONE TUS DIRECTORIOS en <value>):

```
<configuration>
     <property>
         <name>dfs.replication</name>
         <value>1</value>
     </property>
     <property>
         <name>dfs.namenode.name.dir</name>
         <value>/home/mcoutada/hadoop/dfs/name334</value>
     </property>
     <property>
         <name>dfs.datanode.data.dir</name>
         <value>/home/mcoutada/hadoop/dfs/data334</value>
     </property>
</configuration>
```

correr:
```
code etc/hadoop/mapred-site.xml
```

Reemplazar:
```
<configuration>

</configuration>
```

Por:

```
<configuration>
     <property>
         <name>mapreduce.framework.name</name>
         <value>yarn</value>
     </property>
     <property>
         <name>mapreduce.application.classpath</name>
         <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
     </property>
</configuration>
```

correr:
```
code etc/hadoop/yarn-site.xml
```


Reemplazar:
```
<configuration>

<!-- Site specific YARN configuration properties -->

</configuration>
```
Por:
```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```

correr:
```
bin/hdfs namenode -format
```

no deberia hacer falta, pero a mi me hzo falta correr:
```
sudo service ssh start
```
y
```
sudo service ssh restart
```

sino me daba bloqueado el puerto 22.

correr:
```
sbin/start-dfs.sh
```

correr:
```
jps
```
esto me devolvio:
```
22296 SecondaryNameNode
22057 DataNode
21913 NameNode
22426 Jps
```

ya podrias entrar aca:
http://localhost:9870/dfshealth.html#tab-overview

---
Esto lo tuviste que hacer por este error:
```
put: File /alkemy/readme.md._COPYING_ could only be written to 0 of the 1 minReplication nodes. There are 0 datanode(s) running and 0 node(s) are excluded in this operation.
```

y efectivamente corrias
```
jps
```
y no aparecia Datanode.

```
sbin/stop-all.sh
# resetear todo (se va a borrar la data que hayas subdio):
rm -Rf /home/mcoutada/hadoop/dfs/data334/*
rm -Rf /home/mcoutada/hadoop/dfs/name334/*
bin/hdfs namenode -format
```



# Correr hadoop:

```
HADOOP_VERSION=3.3.4
cd ~/hadoop/hadoop-${HADOOP_VERSION}/
```

corroborar que no haya nada corriendo:
```
sbin/stop-all.sh
```

```
bin/hdfs namenode -format
```

si te dice que esta bloqueado el puerto 22:
```
sudo service ssh start
sudo service ssh restart
```

```
sbin/start-all.sh
```

ya podrias entrar aca:
```
http://localhost:9870/dfshealth.html#tab-overview
```


Para pararlo:
```
sbin/stop-all.sh
```

para verificar que este corriendo bien:
```
jps
```

tenes que ver algo asi:
```
21186 NameNode
21330 DataNode
22661 Jps
21782 ResourceManager
21562 SecondaryNameNode
21931 NodeManager
```

si alguno de estos no aparece es porque no esta corriendo y hay que arreglarlo

