import os
import shutil
import time
from bcoding import bencode, bdecode
from seed_extract import Parser

#os.chdir(r'E:\qBittorrent')
#filePath = input('文件名称列表')  # 用于获取文件名称列表
#old_path = r'C:\Users\1\AppData\Local\qBittorrent\BT_backup'  # 源文件夹
#new_path = r'C:\Users\1\AppData\Local\qBittorrent\BT_temp'  # 目标文件夹


def parserInfoPrint(file,lang='Eng'):
    parser = Parser(file)
    parserInfoList=[]
    parserChiList = ['大小','创建时间', '编码', '创建', '私有', '信息哈希v1', '名称', 'Tacker', '备注']
    parserEngList = ['Size', 'Creation Date', 'Encoding', 'Created By', 'Private', 'Info Hash v1', 'Name', 'Announce', 'Comment']
    if lang=='Chi':
        parserLangList=parserChiList
    elif lang=='Eng':
        parserLangList=parserEngList
    #parserInfoList.append(parser.getStruct())
    parserInfoList.append(parser.getLength())
    parserInfoList.append(parser.getCreationDate())
    parserInfoList.append(parser.getEncoding())
    parserInfoList.append(parser.getCreatedBy())
    parserInfoList.append(parser.getInfoPrivate())
    parserInfoList.append(parser.getHash1())
    parserInfoList.append(parser.getName())
    parserInfoList.append(parser.getAnnounce())
    parserInfoList.append(parser.getComments())
    for i in range(len(parserInfoList)):
        parserInfoList.append(parserLangList[i]+':'+parserInfoList[i])

    #parserInfoList.append(parser.getInfo())
    #parserInfoList.append(parser.checkType())

    return parserInfoList

def parserFilePrint(file):
    parser = Parser(file)

    return parser.getInfoFiles()




