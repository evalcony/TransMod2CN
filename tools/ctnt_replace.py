# import sys
#
# sys.path.append("..")
# import utils


# 文件内容替换
# 作为零碎内容的处理


# class ReplUnit:
#     def __init__(self, origin, target, num_order, offset, repl_mode):
#         self.origin = origin
#         self.target = target
#         self.num_order = num_order
#         self.offset = offset
#
#         # repl_mode:
#         #     single: 单行替换
#         #     block: 块替换，此时 target就是一个line
#         self.repl_mode = repl_mode
#
# def str_replace(master, repunit_list):
#
#     m_lines = utils.read_file(master)
#     for unit in repunit_list:
#         search_target_line(m_lines, unit.num_order, unit.offset)
#
#
#
#     True
#
# def search_target_line()
