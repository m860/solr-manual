# -*- coding: UTF-8 -*-

from optparse import OptionParser
import sys
import os
import urllib
from helper import downloadFile

parser = OptionParser()
parser.add_option("--package", help="solr的下载地址或者是本地包的地址",
                  default='http://apache.fayea.com/lucene/solr/5.5.3/solr-5.5.3.tgz')
parser.add_option("--path", help="solr的安装位置", default='/opt/solr')

(options, args) = parser.parse_args()

saveFilePath = os.path.join(options.path, os.path.basename(options.package))

solrRealPath = os.path.splitext(saveFilePath)[0]

solrCLICfg = os.path.join(options.path, 'solr.cli.cfg')

