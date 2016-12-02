# -*- coding: UTF-8 -*-

from optparse import OptionParser
import sys
import os
import urllib
from helper import downloadFile, getConfigValue
from stopSolr import stop

solrCLICfg = getConfigValue('cli', 'confPath')

# stop all solr server
stop()

# rm solr
solrDir=getConfigValue('solr','dir',solrCLICfg)
os.system('rm -fr '+solrDir)
os.system('rm -f '+solrCLICfg)
