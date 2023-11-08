import configparser
import os


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

def read_tras(prefix=''):
    path = prefix + NAMESPACE + '/tra'
    print(path)
    return os.listdir(path)

def read_dict(filename, encoding='utf-8'):
    lines = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir
    if not os.path.exists(path + '/' + filename):
        print(filename + ' file not exist')
        return []
    with open(path + '/' + filename, 'r', encoding=encoding) as file:
        for line in file:
            lines.append(line.replace("\n", ""))
    return lines

def read_file(filename, encoding='utf-8'):
    lines = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/' + NAMESPACE
    if not os.path.exists(path+'/'+filename):
        print(filename+' file not exist')
        return []
    with open(path+'/'+filename, 'r', encoding=encoding) as file:
        for line in file:
            lines.append(line.replace("\n",""))
    return lines

def write_file(prefix, filename, lines, encoding='utf-8'):
    print('写入文件:', filename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/' + NAMESPACE +'/output/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + prefix+filename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'w').close()
    with open(dir_file_path, 'w', encoding=encoding) as f:
        for m in lines:
            f.write(m+'\n')

def write_line_in_append(prefix, filename, lines, encoding='utf-8'):
    print('写入文件:', filename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/' + NAMESPACE+'/output/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + NAMESPACE + '/' + prefix+filename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'a').close()
    with open(dir_file_path, 'a', encoding=encoding) as f:
        for m in lines:
            f.write(m + '\n')

# 将文件记录写入 readlog.txt 中
def write_logs(lines, encoding='utf-8'):
    print('写入文件:readlog.txt')
    print('')
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + NAMESPACE + '/readlog.txt'
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'a').close()
    with open(dir_file_path, 'a', encoding=encoding) as f:
        for m in lines:
            f.write(m + '\n')

def to_upper(lines):
    for line in lines:
        print(line.upper())

# 构造文件名列表，就不需要每次都手动填了
def all_files(path_prefix):
    file_list = []
    for i in range(1, 96):
        file_list.append(path_prefix + '/sod_' + str(i) + '.tra')
    return file_list

def get_enzh_files(path_prefix):
    en_file_list = []
    zh_file_list = []
    for i in range(1, 96):
        # 英文源文件
        en_file_list.append(path_prefix + '/orig/sod_'+str(i)+'_orig.tra')
        # 汉化文件
        zh_file_list.append(path_prefix + '/sod_'+str(i)+'.tra')
    return (en_file_list, zh_file_list)

NAMESPACE = read_config('appconf.ini')['mod']['namespace']
print('namespace='+NAMESPACE)