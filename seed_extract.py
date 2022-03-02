# -*- coding:utf-8 -*-
import hashlib
import time
from bcoding import bencode, bdecode


class Parser(object):

    def __init__(self, filePath):
        self.path = filePath
        metainfo_file = open(str(self.path), 'rb')
        self.metainfo = bdecode(metainfo_file.read())
        self.info = self.metainfo['info']

        metainfo_file.close()

    def getStruct(self):
        return self.metainfo.keys()

    def getAnnounce(self):
        if 'announce' in self.metainfo:
            return self.metainfo['announce']
        elif 'announce-list' in self.metainfo:
            return self.metainfo['announce-list']
        else:
            return 'N/A'

    def getLength(self):
        if 'length' in self.metainfo['info']:
            return str(self.metainfo['info']['length'])
        else:
            return ''

    # 如果是单文件就返回：0
    # 如果是多文件就返回:1
    def checkType(self):
        if 'files' in self.metainfo['info']:
            return 1
        else:
            return 0

    def getCreationDate(self):
        if 'creation date' in self.metainfo:
            return time.strftime('%Y-%m-%d', time.localtime(self.metainfo['creation date']))
        else:
            return 'N/A'

    def getInfo(self):
        return self.metainfo['info'].keys()

    # 获得哈希id
    def getHash1(self):
        raw_info_hash = bencode(self.metainfo['info'])
        hash = hashlib.sha1(raw_info_hash).hexdigest()
        return hash

    # 获得文件名
    def getName(self):
        if 'name.utf-8' in self.info:
            filename = self.info['name.utf-8']
        else:
            filename = self.info['name']

        for c in filename:
            if c == "'":
                filename = filename.replace(c, "\\\'")
        return filename

    # 多文件的情况下，获得所有文件，返回为:dic
    def getInfoFiles(self):
        if 'files' in self.info:
            return self.info['files']
        elif 'name.utf-8' in self.info:
            filename = self.info['name.utf-8']
        else:
            filename = self.info['name']
        for c in filename:
            if c == "'":
                filename = filename.replace(c, "\\\'")
        fileNameDict = [{'length': self.info['length'], 'path': [filename]}]
        return fileNameDict

    def getInfoPrivate(self):
        if 'private' in self.metainfo['info']:
            if self.metainfo['info']['private'] == 1:
                return 'Y'
            elif self.metainfo['info']['private'] == 0:
                return 'N'
            else:
                return str(self.metainfo['info']['private'])
        else:
            return 'N/A'

    # 返回创建时间
    def getCreatedBy(self):
        if 'created by' in self.metainfo:
            return self.metainfo['created by']
        else:
            return ''

    # 获得编码方式
    def getEncoding(self):
        if 'encoding' in self.metainfo:
            return self.metainfo['encoding']
        return ""

    def getComments(self):

        if 'comment.utf-8' in self.metainfo:
            comment = self.metainfo['comment.utf-8']
            return comment
        else:
            return 'N/A'
