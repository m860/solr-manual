# -*- coding: UTF-8 -*-
"""

install
--package http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz zookeeper下载地址/也可以是本地包
--path /opt/zookeeper zookeeper安装位置
--port 2181 端口
--dataDir /var/lib/zookeeper
--servers server.1=127.0.0.1:2881:3881,

start

stop

status

"""

from optparse import OptionParser
import sys
import os
import urllib

parser = OptionParser()
parser.add_option("--package", help="zookeeper的下载地址,或者是本地包的位置",
                  default='http://mirrors.cnnic.cn/apache/zookeeper/zookeeper-3.4.8/zookeeper-3.4.8.tar.gz')
parser.add_option("--path", help="zookeeper的安装位置", default='/opt/zookeeper')
parser.add_option("--port", help="zookeeper的运行端口", default='2181')
parser.add_option("--dataDir", help="zookeeper数据存放位置", default='/var/lib/zookeeper')
parser.add_option("--server", help="需要进行数据同步的server,如果有多个以','分割", default='')
parser.add_option("--id", help="需要进行数据同步的server,如果有多个以','分割", default='1')

(options, args) = parser.parse_args()

action = ''
if len(sys.argv) > 1:
    action = sys.argv[1].lower()

zkinstances = '/opt/zk-instances'


def getFileName(path):
    return os.path.basename(path)


def downloadFile(url):
    filename = getFileName(url)
    savepath = os.path.join(options.path, filename)
    file = urllib.URLopener()

    def progress(count, blockSize, totalSize):
        percent = int(count * blockSize * 100 / totalSize)
        sys.stdout.write("\r%2d%%" % percent)
        sys.stdout.flush()

    try:
        file.retrieve(url, savepath, reporthook=progress)
    except:
        print('下载失败')
        os.remove(savepath)


def createzk(path):
    filename = getFileName(path)
    dir = filename.replace('.tar.gz', '')
    inspath = os.path.join(options.path, dir)
    if not os.path.exists(inspath):
        print('解压' + filename)
        os.system('tar xzf ' + path + ' -C ' + options.path)
    print ('生成默认配置文件')
    zooCfg = os.path.join(inspath, "conf/zoo.cfg")
    zooSampleCfg = os.path.join(inspath, "conf/zoo_sample.cfg")
    with open(zooSampleCfg) as o:
        with open(zooCfg, "w+") as zoo:
            for line in o:
                if line.startswith("dataDir"):
                    zoo.write('dataDir=' + options.dataDir + '\n')
                if line.startswith("clientPort"):
                    zoo.write('clientPort=' + options.port + '\n')
                    if options.server:
                        for server in options.server.split(","):
                            zoo.write(server + '\n')
                else:
                    zoo.write(line)
    print ('生成数据文件')
    if not os.path.exists(options.dataDir):
        os.makedirs(options.dataDir)
    with open(os.path.join(options.dataDir, 'myid'), 'w+') as myid:
        myid.write(options.id)
    # 生成缓存数据
    with open(zkinstances, 'r+') as zk:
        text = zk.read()
        zkserverpath = inspath + '/bin/zkServer.sh\n'
        if zkserverpath not in text:
            zk.write(inspath + '/bin/zkServer.sh\n')
    print ('创建完成')


def zkserver(type='status'):
    with open(zkinstances) as ins:
        for i in ins:
            cmd = i.strip('\n') + " " + type
            os.system(cmd)


def getDataDir(cfgpath):
    with open(cfgpath) as cfg:
        for line in cfg:
            if line.startswith("dataDir"):
                return line.strip('dataDir=').strip('\n')
    return ''


def getCfgPath(zk):
    dn = os.path.dirname(zk)
    return os.path.join(dn, '../conf/zoo.cfg')


def getInsDir(zk):
    dn = os.path.dirname(zk)
    return os.path.join(dn, '../..')


if action == "install":
    if not os.path.exists(zkinstances):
        open(zkinstances,'w+').close()
    if not os.path.exists(options.path):
        os.makedirs(options.path)
    fileName = getFileName(options.package)
    packagePath = os.path.join(options.path, fileName)
    if os.path.isfile(packagePath):
        createzk(packagePath)
    else:
        if options.package.startswith("http"):
            # download
            print ('下载' + fileName)
            downloadFile(options.package)
            createzk(packagePath)
        else:
            print ('拷贝' + fileName)
            os.system('cp ' + options.package + ' ' + options.path)
            createzk(packagePath)
# elif action == "uninstall":
#     # 停止服务
#     zkserver('stop')
#     # 根据配置文件删除数据文件
#     with open(zkinstances) as ins:
#         for line in ins:
#             dd = getDataDir(getCfgPath(line))
#             os.system('rm -r '+dd)
#             # 删除zookeeper
#             insd = getInsDir(line)
#             os.system('rm -r '+insd)
#     os.system('rm -r '+zkinstances)
else:
    zkserver(action)
