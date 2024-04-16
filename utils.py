import configparser
import os


def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path(name))
    return config

def write_config(config, name):
    # 将修改后的配置写回文件
    config_path = file_path(name)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

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


def intercept(func):
    def wrapper(*args, **kwargs):
        # print('拦截方法:', func.__name__)
        res = func(*args, **kwargs)
        result = []
        for r in res:
            if r == '.DS_Store':
                continue
            result.append(r)
        return result

    return wrapper

@intercept
def read_tras():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/resource/' + NAMESPACE
    return os.listdir(path+'/tra')

@intercept
def read_dir(dir):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/resource/' + NAMESPACE
    return os.listdir(path + '/' + dir)

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
    path = root_dir + '/resource/' + NAMESPACE
    if not os.path.exists(path+'/'+filename):
        print(filename+' file not exist')
        return []
    with open(path+'/'+filename, 'r', encoding=encoding) as file:
        for line in file:
            lines.append(line.replace("\n",""))
    return lines

# 以覆盖的方式写入
def write_file(prefix, filename, lines, encoding='utf-8'):
    print('写入文件:', filename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/resource/' + NAMESPACE +'/output/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + prefix+filename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'w').close()
    with open(dir_file_path, 'w', encoding=encoding) as f:
        for m in lines:
            f.write(m+'\n')

# 以追加的方式写入
def write_line_in_append(prefix, filename, lines, encoding='utf-8'):
    print('写入文件:', filename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir + '/resource/' + NAMESPACE+'/output/'
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + prefix+filename
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
    dir_file_path = path + '/resource/' + NAMESPACE + '/readlog.txt'
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'a').close()
    with open(dir_file_path, 'a', encoding=encoding) as f:
        for m in lines:
            f.write(m + '\n')

def to_upper(lines):
    for line in lines:
        print(line.upper())

def get_enzh_files(path_prefix):
    en_file_list = list_files('resource/'+NAMESPACE+'/'+path_prefix+'/orig/')
    zh_file_list = list_files('resource/'+NAMESPACE+'/'+path_prefix)
    return (en_file_list, zh_file_list)

def list_files(startpath):
    res = []
    print(startpath)
    for root, _, filenames in os.walk(startpath):
        for filename in filenames:
            s = os.path.join(root, filename)
            print(s)
            res.append(s)
        print('-' * 20)
    return res


NAMESPACE = read_config('appconf.ini')['mod']['namespace']


# list_files('resource/Imoen-romance/output')