#! /usr/bin/python3

import sys
from random import sample
from time import time

#方格类
class Checker:
    __slots__ = ['cstatus', 'cnumber']
    def __init__(self):
        self.cstatus = False   #状态True为打开，False为未打开
        self.cnumber = 0       #该方格附近雷的个数,-1表示为雷
    def get_cstatus(self):
        return self.cstatus
    def set_cstatus(self, cstatus):
        self.cstatus = cstatus
    def get_cnumber(self):
        return self.cnumber
    def set_cnumber(self, cnumber):
        self.cnumber = cnumber

#获取一个方格周围的方格，并返回其列表
around_checker= ((-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1))

#计算方块的数字
def cnums(l, height, width):
    def cnum(a, b):
        number = 0
        for (i, j) in around_checker:
            flage = -1 < a+i < height and -1 < b+j < width and (l[a+i][b+j].get_cnumber() == -1)
            number += 1 if flage else 0
        return number
    for i in range(height):
        for j in range(width):
            if l[i][j].get_cnumber() != -1: l[i][j].set_cnumber(cnum(i, j))

#随机分布雷
def put_xxx(width, height, xnum):
    clist = [] 
    for i in range(height):
        l = []
        for j in range(width):
            l.append(Checker())
        clist.append(l)
    xl = sample([x for i in clist for x in i], xnum)
    for i in xl:
        i.set_cnumber(-1)
    return clist

#显示界面
def show_checker_list(l, height, width):
    length = 4 * width +1
    print('     ', end=' ')
    for i in range(width):print('{:^3d} '.format(i + 1), end='')
    print('\n     '+'-' * length)
    for y, i in enumerate(l, 1):
        print('{:>4d} |'.format(y), end='')
        for j in i:
            s = 'x' if (j.get_cnumber() == -1) else j.get_cnumber()
            print((' {} |'.format(s)) if j.get_cstatus() else '   |', end = '')
        print('', end='\n     ')
        print('-' * length)

#点击事件
def click(l, x, y, height, width):
    l[x][y].set_cstatus(True)
    if l[x][y].get_cnumber() == -1:
        show_checker_list(l, height, width)
        print('GAME OVER!游戏结束')
        sys.exit()
    success = True
    for i in l:
        for j in i:
            if not j.get_cstatus() and j.get_cnumber() != -1: success = False
    if success:
        show_checker_list(l, height, width)
        print('恭喜通关!', end=' ')
        T = time() - t
        h = T // 3600
        m = T // 60 % 60
        s = T % 60
        if h:   print('用时 {:.0f} 时 {:.0f} 分 {:.0f} 秒'.format(h, m, s))
        elif m: print('用时 {:.0f} 分 {:.0f} 秒'.format(m, s))
        else:   print('用时 {:.0f} 秒'.format(s))
        sys.exit()

    if l[x][y].get_cnumber(): return
    for (i, j) in around_checker:
        if -1 < x + i < height and -1 < y + j < width:
            if not l[x+i][y+j].get_cstatus(): click(l, x+i, y+j, height, width)
            if l[x+i][y+j].get_cnumber() == -1: return

def main():
    try:
        height = int(input('请输入高度：'))
        width = int(input('请输入宽度：'))
        xxxnum = int(input('请输入雷数：') or height * width * 0.15625)
        if not 0 < xxxnum < height * width: raise ValueError()
    except ValueError:
        print('输入错误！程序结束')
        sys.exit()
    checker_list = put_xxx(width, height, xxxnum)
    cnums(checker_list, height, width)
    show_checker_list(checker_list, height, width)
    global t
    t = time()
    while True: 
        try:
            y = int(input('请输入坐标x：'))
            x = int(input('请输入坐标y：'))
            if not 0 < x <= height or not 0 < y <= width: raise ValueError()
        except ValueError:
            print('输入错误！请重新输入')
            continue
        click(checker_list, x-1, y-1, height, width)
        show_checker_list(checker_list, height, width)


if __name__ == '__main__':main()
