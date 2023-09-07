import configparser
import os
import codecs


def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path(name))
    return config

# 读取系统环境变量
def read_env(keyname):
    if keyname in os.environ:
        value = os.environ[keyname]
        return value

def file_path(name):
    # 获取当前文件所在的根路径
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, name)
    return file_path

# def read_file(filename):
#     lines = []
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#     print('root_dir:' + root_dir)
#     print('filename:' + filename)
#     if not os.path.exists(root_dir+'/'+filename):
#         print('file not exist')
#         return []
#     with open(root_dir+'/'+filename, 'r') as file:
#         for line in file:
#             lines.append(line.replace("\n",""))
#     return lines

def read_file(filename, encoding='utf-8'):
    lines = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print('root_dir:' + root_dir)
    print('filename:' + filename)
    if not os.path.exists(root_dir+'/'+filename):
        print('file not exist')
        return []
    # with codecs.open(root_dir+'/'+filename, 'r', encoding=encoding) as file:
    #     for line in file:
    #         lines.append(line.replace("\n",""))
    # return lines
    with open(root_dir+'/'+filename, 'r', encoding=encoding) as file:
        for line in file:
            lines.append(line.replace("\n",""))
    return lines

def write_file(prefix, finename, lines, encoding):
    print('写入文件:', finename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir+'/output/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + prefix+finename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'w').close()
    with open(dir_file_path, 'w', encoding=encoding) as f:
        for m in lines:
            f.write(m+'\n')