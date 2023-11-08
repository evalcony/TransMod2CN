import argparse
import utils

def update(update_param):
    # 解析参数
    key_end_pos = update_param.find('=')
    arg_left = update_param[:key_end_pos]
    arg_right = update_param[key_end_pos + 1:]
    key_arr = arg_left.split('.')

    section = key_arr[0]
    option = key_arr[1]
    value = arg_right

    config = utils.read_config('appconf.ini')
    config.set(section, option, value)

    utils.write_config(config, 'appconf.ini')

def show():
    config = utils.read_config('appconf.ini')
    for section in config.sections():
        print(f"[Section: {section}]")
        for option, value in config.items(section):
            print(f"{option} = {value}")
        print('')

def work(args):
    if args.u != '':
        update(args.u)
    elif args.show:
        show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, default='', help='update config的参数。遵循section.option.value 的写法')
    parser.add_argument('-show', action='store_true', help='print config')
    args = parser.parse_args()

    work(args)
