import hashlib
import os
import pickle
import socket
from subprocess import Popen

import pandas as pd

HOST_IP = "10.18.103.150"
# HOST_IP     = socket.gethostname()
HOST_PORT = 10009

CODE_END = "__uploadCode end\n"
DATA_END = "__uploadData end\n"

# 错误码
NO_ERR = 0

WARNNING = 10
WARN_DATA_SER_VACANCY = 11

ERRNO_START = 100
ERR_SUBMIT_REPEATEDLY = 100
ERR_CLASS_NAME_REPEATEDLY = 101
ERR_DATA_TYPE = 200
ERR_DATA_DICT_VALUE_SER = 210
ERR_DATA_DICT_VALUE_INDX = 211
ERR_DATA_DICT_KEY = 212
ERR_DATA_SER_CLASS_INHERITANCE = 220
ERR_DATA_SER_INDEX = 221
ERR_CODE_CLASS_NAME = 300
ERR_FEATURE_WRONG = 400
ERR_FEATURE_EXISTS = 401
ERR_FEATURE_COPY_WRONG = 402
ERR_FEATURE_NO_CLASS = 403

ERR_END = 999


class SubmitFeature:
    """ Client for submiting feature to server

        提交数据格式如下：
        |----------------------------------------------------------------------------------------------------
        |          ||                         |     |          ||                         |     |          ||
        |file name ||          code           | md5 | CODE_END ||            data         | md5 | DATA_END ||
        |          ||                         |     |          ||                         |     |          ||
        |____________________________________________________________________________________________________

        注：
        1) 双竖线'||'表示等待服务器确认，单竖线'|'表示数据分割（无实际意义）
        2) md5长32个字符
        3) 全部数据发送完毕后，等待服务器检验，接收服务器发来的错误码

    """

    def __init__(self, filename, data=dict()):
        self.__fileName = os.path.basename(filename)
        self.__file = open(filename, "r")
        self.__code = ''.join(self.__file.readlines())
        self.__dataset = data
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.__code)

    def submitFeature(self):
        self.__initSocket()

        errno = self.__uploadFileName()
        if errno >= ERRNO_START:
            self.__catchError(errno)
            return

        errno = self.__uploadCode()
        if errno >= ERRNO_START:
            self.__catchError(errno)
            return

        errno = self.__uploadData()
        if errno >= ERRNO_START:
            self.__catchError(errno)
            return

        errno = self.__listenError()
        if errno >= ERRNO_START:
            self.__catchError(errno)
            return

        self.__file.close()
        self.__sock.close()
        print("上传成功！")

    def __initSocket(self):
        try:
            self.__sock.connect((HOST_IP, HOST_PORT))
        except socket.error as e:
            print("Connect server failed: %s" % (e))
            self.__sock.close()
            raise
        else:
            print("sock connect succeed")

    def __uploadFileName(self):
        errno = NO_ERR
        codeMd5 = hashlib.md5(self.__code.encode('utf-8'))
        sendCodeMd5 = codeMd5.hexdigest() + '\n'

        sendStr = self.__fileName + '\n'
        self.__sock.sendall(sendStr.encode('utf-8'))
        self.__sock.sendall(sendCodeMd5.encode('utf-8'))
        confirmEnd = self.__sock.recv(1024)
        print(confirmEnd)
        if confirmEnd != "done".encode('utf-8'):
            errno = int.from_bytes(confirmEnd, 'big')
            print("errno = %d" % (errno))

        return errno

    def __uploadCode(self):
        codeBytes = self.__code.encode('utf-8')
        md5 = hashlib.md5(codeBytes)
        confirmEnd = b''

        while not "done".encode() in confirmEnd:
            self.__sock.sendall(codeBytes)
            self.__sock.sendall(md5.hexdigest().encode('utf-8'))
            self.__sock.sendall("__uploadCode end\n".encode('utf-8'))
            confirmEnd = self.__sock.recv(1024)
            print("----------------------------------------------------")
            print(codeBytes)
            print("----------------------------------------------------")
            print(md5.hexdigest())
            print(confirmEnd)

        return NO_ERR

    def __uploadData(self):
        if isinstance(self.__dataset, dict):
            print("__data is dict")
            errno = self.__checkDict()
            if errno == NO_ERR:
                self.__sendDict()
            else:
                return errno

        elif type(self.__dataset) == pd.core.series.Series:
            print("__data is serials")
            errno = self.__checkSerials()
            if errno == NO_ERR:
                self.__sendSer()
            else:
                return errno

        else:
            return ERR_DATA_TYPE

        return NO_ERR

        # totalData = ""
        # for string in self.__dataset:
        #     print(string)
        #     self.__sock.sendall(string.encode('utf-8'))
        #     totalData = totalData + string
        # md5 = hashlib.md5(totalData.encode(encoding='utf8'))
        # print(md5.hexdigest())
        # self.__sock.sendall("__uploadData end\n".encode('utf-8'))
        # self.__sock.sendall(md5.hexdigest().encode('utf-8'))
        # confirmEnd = self.__sock.recv(1024)
        # print(confirmEnd)

    def __checkDict(self):
        # 若为空，则无需检查
        if not self.__dataset:
            return NO_ERR

        # 若为dict，key是股票代码，value是数据内容<pandas.Series>，股票的key满足格式<CN_STK_SH600000>
        keys = self.__dataset.keys()
        values = self.__dataset.values()
        for key in keys:
            keySection = key.split('_')
            if len(keySection) != 3:
                return ERR_DATA_DICT_KEY

        for value in values:
            if type(value) != pd.core.series.Series:
                return ERR_DATA_DICT_VALUE_SER
            # 每个<pandas.Series>对应的index为<pandas.DatetimeIndex>
            if type(value.index) != pd.core.indexes.datetimes.DatetimeIndex:
                return ERR_DATA_DICT_VALUE_INDX

            # 检查series是否有空值，报warning让用户确认后执行
            if value.hasnans:
                confirmInput = ''
                while confirmInput != 'y' or confirmInput != 'n':
                    confirmInput = input("警告：数据中有空值，请确认是否继续: y/n")
                    if confirmInput == 'y':
                        print("继续上传...")
                    elif confirmInput == 'n':
                        print("终止本次上传")
                        return WARN_DATA_SER_VACANCY
                    else:
                        print("错误：请输入 y 或 n")

                        # TODO: index周期应该和Feature类里面的granularity(默认为day)相同

        return NO_ERR

    def __checkSerials(self):
        errno = NO_ERR

        # 每个<pandas.Series>对应的index为<pandas.DatetimeIndex>
        if type(self.__dataset.index) != pd.core.indexes.datetimes.DatetimeIndex:
            print(type(self.__dataset.index))
            return ERR_DATA_SER_INDEX

            # TODO: index周期应该和Feature类里面的granularity(默认为day)相同

        # 检查series是否有空值，报warning让用户确认后执行
        if self.__dataset.hasnans:
            confirmInput = ''
            while confirmInput != 'y' or confirmInput != 'n':
                confirmInput = input("警告：数据中有空值，请确认是否继续: y/n")
                if confirmInput == 'y':
                    print("继续上传...")
                elif confirmInput == 'n':
                    print("终止本次上传")
                    return WARN_DATA_SER_VACANCY
                else:
                    print("错误：请输入 y 或 n")

        # TODO: 若为<pandas.Series>，需要检查class继承了InstrumentIDUnrelated类
        tmpFileName = self.__fileName[:-3] + "__test_tmp.py"
        tmpFile = open(tmpFileName, "w+")
        tmpFile.write(self.__code + '\n')
        tmpFile.write("parent = " + self.__fileName[:-3] + ".__base__\n")
        tmpFile.write("if parent == PersistentFeature:\n")
        tmpFile.write("    print('NO_ERR')\n")
        tmpFile.write("    exit(0)\n")
        tmpFile.write("else:\n")
        tmpFile.write("    print('ERR_DATA_SER_CLASS_INHERITANCE')\n")
        tmpFile.write("    exit(255)\n")
        tmpFile.close()
        # ifError = os.system("python3 " + tmpFileName);
        subProc = Popen("python3 " + tmpFileName, shell=True);
        subProc.wait()
        if subProc.returncode == 255:
            errno = ERR_DATA_SER_CLASS_INHERITANCE
        elif subProc.returncode == 0:
            errno = NO_ERR
        # out = ifError.readlines();
        # for string in out:
        #     if string == "NO_ERROR\n":
        #         print(string)
        #         errno = NO_ERR
        #         break
        #     if string == "ERR_DATA_SER_CLASS_INHERITANCE\n":
        #         print(string)
        #         errno = ERR_DATA_SER_CLASS_INHERITANCE
        #         break
        # ifError.close()

        return errno

    def __sendDict(self):
        json_bytes = pickle.dumps(self.__dataset)
        md5 = hashlib.md5(json_bytes)
        confirmEnd = b''

        while not "done".encode() in confirmEnd:
            self.__sock.sendall(json_bytes)
            self.__sock.sendall(md5.hexdigest().encode('utf-8'))
            self.__sock.sendall("__uploadData end\n".encode('utf-8'))
            confirmEnd = self.__sock.recv(1024)
            print(confirmEnd)

    def __sendSer(self):
        bytes_data = pickle.dumps(self.__dataset)
        md5 = hashlib.md5(bytes_data)
        confirmEnd = b''

        while not "done".encode() in confirmEnd:
            self.__sock.sendall(bytes_data)
            self.__sock.sendall(md5.hexdigest().encode('utf-8'))
            self.__sock.sendall("__uploadData end\n".encode('utf-8'))
            confirmEnd = self.__sock.recv(1024)
            print(confirmEnd)

    def __listenError(self):
        print("__listenError start")
        totalData = ""

        while 1:
            acceptData = str(self.__sock.recv(1), encoding='utf8')
            if '\n' in acceptData:
                break
            totalData = totalData + acceptData
        errno = totalData.split()[-1]
        errno = int(errno)
        print("errno: %s" % (errno))

        return errno

    def __catchError(self, errno):
        print("errno = %d" % (errno))
        assert errno >= ERRNO_START

        if errno == ERR_SUBMIT_REPEATEDLY:
            print("ERROR: 重复上传")

        elif errno == ERR_CLASS_NAME_REPEATEDLY:
            print("ERROR: feature已存在，请重命名Feature或增加版本号")

        elif errno == ERR_DATA_TYPE:
            print("ERROR: data类型错误，只接受dict或pandas.Series")

        elif errno == ERR_DATA_DICT_VALUE_SER:
            print("ERROR: data类型错误，dict.value的类型必须为pandas.Series")

        elif errno == ERR_DATA_DICT_VALUE_INDX:
            print("ERROR: data类型错误，dict.value.index的类型必须为pandas.DatetccjimeIndex")

        elif errno == ERR_DATA_DICT_KEY:
            print("ERROR: data类型错误，dict.key必须是满足格式要求的股票代码")

        elif errno == ERR_DATA_SER_CLASS_INHERITANCE:
            print("ERROR: 当data类型为pandas.Series时，class必须继承InstrumentIDUnrelated类")

        elif errno == ERR_DATA_SER_INDEX:
            print("ERROR: data类型错误，Series.index的类型必须为pandas.DatetimeIndex")

        elif errno == ERR_FEATURE_WRONG:
            print("ERROR: feature在服务器端测试运行时，未能返回数据")

        elif errno == ERR_FEATURE_EXISTS:
            print("ERROR: feature数据已存在于服务器端")

        elif errno == ERR_FEATURE_COPY_WRONG:
            print("ERROR: feature数据上传至服务器端时出错")

        elif errno == ERR_FEATURE_NO_CLASS:
            print("ERROR: feature必须是一个类")

        elif errno == ERR_END:
            print("ERROR: 未知错误")

        else:
            print("ERROR: Unknown error type!")
            print("ERROR: 未知错误类型")
