# -*- coding: UTF-8 -*-

from optparse import OptionParser
import sys
import os
import urllib
from helper import downloadFile, getConfigValue

solrCLICfg = getConfigValue('cli', 'confPath')
solrDir = getConfigValue('solr', 'dir', solrCLICfg)
solr = os.path.join(solrDir, 'bin/solr')

# stop all solr server
os.system(solr + ' stop')

# rm solr
solrDir = getConfigValue('solr', 'dir', solrCLICfg)
os.system('rm -fr ' + solrDir)
os.system('rm -f ' + solrCLICfg)
