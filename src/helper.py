# -*- coding: UTF-8 -*-
import sys
import os
import urllib
from ConfigParser import ConfigParser

configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.conf')


def getConfigValue(sectionName, key, path=configPath):
    cfg = ConfigParser()
    cfg.read(path)
    return cfg.get(sectionName, key)


def setConfigValue(sectionName, key, value, path=configPath):
    cfg = ConfigParser()
    cfg.read(path)
    try:
        cfg.options(sectionName)
    except:
        cfg.add_section(sectionName)
    cfg.set(sectionName, key, value)
    cfg.write(open(path, 'w'))


def downloadFile(url, saveFilePath):
    print('开始下载:' + url)
    print('下载文件保存至:' + saveFilePath)
    file = urllib.URLopener()

    def progress(count, blockSize, totalSize):
        percent = int(count * blockSize * 100 / totalSize)
        sys.stdout.write("\r%2d%%" % percent)
        sys.stdout.flush()

    try:
        file.retrieve(url, saveFilePath, reporthook=progress)
    except Exception, e:
        print('下载失败', e)
        os.remove(saveFilePath)
        raise
