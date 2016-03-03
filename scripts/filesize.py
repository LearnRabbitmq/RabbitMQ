
#coding:utf-8

import datetime,glob,sys,commands
from os.path import getsize

date = datetime.datetime.now().strftime('%Y%m%d')
arg1 = sys.argv[1]

files_list = glob.glob(arg1 + date + '*')
files_str = ''.join(files_list)
if files_str:
    # 统计文件的大小单位是B
    #files_size = getsize(files_str)
    # 统计文件占用磁盘空间单位是KB
    cmd = 'du -sh %s' %(files_str)
    files_size = commands.getoutput(cmd)
    print files_size
else:
    print 0

