# solr-manual
安装solr的流程和相关配置

# 安装前的准备
* 操作系统CentOS 7
* java 1.8.*
```bash
# install java 1.8.*
$ yum search java | grep java-
$ sudo yum install java-1.8.0*
```
* wget
```bash
# install wget
$ sudo yum install wget
```

# 安装
[solr v5.5.3](http://apache.fayea.com/lucene/solr/5.5.3/solr-5.5.3.tgz)

[zookeeper v3.4.8](http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz)

## zookeeper
```shell
$ test -d downloads || mkdir downloads && cd downloads
$ wget http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz
$ tar xzf zookeeper-3.4.8.tar.gz
$ # 创建3个zookeeper实例,这里3个实例都在一台服务器上,也可以分别建在不同的服务器上
$ cp cp zookeeper-3.4.8/ /opt/zookeeper-node-01/ #zookeeper 第一个实例,等第一个实例创建好之后再进行复制
$ # 配置实例01
$ cd /opt/zookeeper-node-01/
$ cp conf/zoo_sample.cfg conf/zoo.cfg
$ # 开始编辑配置
$ # 这里主要编辑如下几个属性:dataDir,clientPort,server,如zoo.cfg示例
$ # 配置好后开始创建实例01的数据文件夹
$ cd /var/lib
$ mkdir zookeeper-node-01
$ # 创建实例id,此id和server.1这里的1保持一致
$ cd zookeeper-node-01
$ vi myid # 由于目前id=1 所以这里写1即可保存
$ # 至此实例01创建完成,开始创建实例02,03
$ cd /opt
$ cp -r zookeeper-node-01 zookeeper-node-02 && cp -r zookeeper-node-01 zookeeper-node-03
$ # 分别修改实例02,03的配置文件,dataDir和clientPort,server都是一样的,无需修改
$ # 实例02:dataDir=/var/lib/zookeeper-node-02;clientPort=2182
$ # 实例03:dataDir=/var/lib/zookeeper-node-03;clientPort=2183
$ # 和实例01一样创建其对应的数据文件夹
$ # 至此所有实例创建完成
$ # 启动3个实例,最好一起启动,每个实例启动的间隔不要太久
$ zookeeper-node-01/bin/zkServer.sh start && zookeeper-node-02/bin/zkServer.sh start && zookeeper-node-03/bin/zkServer.sh start
$ # 启动完成后可以查看起状态
$ zookeeper-node-01/bin/zkServer.sh status && zookeeper-node-02/bin/zkServer.sh status && zookeeper-node-03/bin/zkServer.sh status
$ # 至此zookeeper配置完成

```
zoo.cfg示例
```text
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/var/lib/zookeeper-node-01
# the port at which the clients will connect
clientPort=2181
server.1=127.0.0.1:2881:3881
server.2=127.0.0.1:2882:3882
server.3=127.0.0.1:2883:3883
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
```
## zookeeperCLI
从安装到配置一步到位
```bash
$ sudo python zookeeperCLI.py install
```
第一参数可以缺省,如果缺省是查看zookeeper的status,zookeeper的所有命令都支持,包括如下值(不仅限于此):
* install
* start
* stop
* status
* restart

### 参数说明
名称|说明|默认值
----|----|----
--package|可以是url,也可以是本地已下载好的包|http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz
--path| |/opt/zookeeper
--port| |2181
--dataDir| |/var/lib/zookeeper
--server| |
--id| |1

# 安装solr
```bash
$ # install
$ sudo python src/installSolr.py
$ # uninstall
$ sudo python src/uninstallSolr.py
```
## 参数说明
名称|说明|默认值
----|----|----
--package|可以是url,也可以是本地已下载好的包|http://apache.fayea.com/lucene/solr/5.5.3/solr-5.5.3.tgz
--path| |/opt/solr



