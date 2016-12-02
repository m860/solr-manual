# -*- coding: UTF-8 -*-

from optparse import OptionParser
import sys
import os
import urllib
from helper import downloadFile, getConfigValue, setConfigValue

parser = OptionParser()
parser.add_option("--package", help="solr的下载地址或者是本地包的地址",
                  default='http://apache.fayea.com/lucene/solr/5.5.3/solr-5.5.3.tgz')
parser.add_option("--path", help="solr的安装位置", default='/opt/solr')

(options, args) = parser.parse_args()

saveFilePath = os.path.join(options.path, os.path.basename(options.package))

solrRealPath = os.path.splitext(saveFilePath)[0]

solrCLICfg = getConfigValue('cli', 'confPath')

if not os.path.exists(solrCLICfg):
    print('create ' + solrCLICfg)
    os.system('touch ' + solrCLICfg)

if not os.path.exists(options.path):
    os.makedirs(options.path)

# download
if not os.path.exists(saveFilePath):
    if options.package.startswith('http'):
        # download from url
        print('download solr from ' + options.package)
        downloadFile(options.package, saveFilePath)
        pass
    else:
        # copy from path
        print('copy solr form ' + options.package)
        os.system('cp ' + options.package + ' ' + saveFilePath)
        pass

# unzip
print('unzip solr')
os.system('tar xzf ' + saveFilePath + ' -C ' + options.path)

setConfigValue('solr', 'dir', solrRealPath, solrCLICfg)

print('solr install success')
