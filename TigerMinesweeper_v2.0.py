#! /usr/bin/python3

import tkinter as tk
from random import sample
from time import time

#弹窗类
class MyDialog(tk.Toplevel):
    def __init__(self, t = None): 
        super().__init__()
        self.grab_set()   #确保鼠标或者键盘事件不会被发送到错误的窗口
        if t: self.result_UI(t)
        else: self.setup_UI()
    #自定义弹窗
    def setup_UI(self):
        self.title('游戏设置')
        #第一行
        row1 = tk.Frame(self)
        row1.pack(fill = 'x')
        tk.Label(row1, text = '宽度：', width = 8).pack(side = tk.LEFT)
        self.width = tk.IntVar()
        tk.Entry(row1, textvariable = self.width, width = 20).pack(side = tk.LEFT) 
        #第二行
        row2 = tk.Frame(self)
        row2.pack(fill = 'x')
        tk.Label(row2, text = '高度：', width = 8).pack(side = tk.LEFT)
        self.height = tk.IntVar()
        tk.Entry(row2, textvariable = self.height, width = 20).pack(side = tk.LEFT) 
        #第三行
        row3 = tk.Frame(self)
        row3.pack(fill = 'x')
        tk.Label(row3, text = '雷数：', width = 8).pack(side = tk.LEFT)
        self.xnum = tk.IntVar()
        tk.Entry(row3, textvariable = self.xnum, width = 20).pack(side = tk.LEFT) 
        #第三行
        row4 = tk.Frame(self)
        row4.pack()
        tk.Button(row4, text = '确定', command = self.ok, default = tk.ACTIVE).pack(side = tk.LEFT)
        tk.Button(row4, text = '取消', command = self.cancel).pack(side = tk.LEFT)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
    #游戏结果弹窗
    def result_UI(self, t):
        self.title('游戏结果')
        row1 = tk.Frame(self)
        row1.pack(fill = 'x')
        ms = tk.Label(row1, text = t)
        ms.pack()
        row2= tk.Frame(self)
        row2.pack(fill = 'x')
        bt = tk.Button(row2, text='确定', command = self.destroy)
        bt.pack()
    #确定按钮点击事件
    def ok(self, event=None):
        flage = (self.height.get() > 0 and self.width.get() > 0 and 
                 self.height.get() * self.width.get() > self.xnum.get() > 0)
        if flage:
            self.Checker_info = [self.height.get(), self.width.get(), self.xnum.get()]
            self.destroy()
    #取消按钮点击事件
    def cancel(self, event=None):
        self.Checker_info = None
        self.destroy()

#主窗口
class MyApp(tk.Tk):
    time_go = True
    #获取一个方格周围的方格，并返回其列表
    around_checker= ((-1,-1), (-1,0), (-1,1),
                     (0, -1),         (0, 1),
                     (1, -1), (1, 0), (1, 1))
    #方格类
    class Checker:
        flage = False
        def __init__(self,x,y):
            self.cstatus = False   #状态True为打开，False为未打开
            self.cnumber = 0       #该方格附近雷的个数,-1表示为雷
            self.__x = x
            self.__y = y
        def get_x(self):
            return self.__x
        def get_y(self):
            return self.__y
        def get_cstatus(self):
            return self.cstatus
        def set_cstatus(self, cstatus):
            self.cstatus = cstatus
            if self.cnumber == -1: 
                self.cbutton.config(fg = '#e62')
            if self.cstatus:
                self.cbutton.config(command = tk.DISABLED, relief = 'flat', bg = '#eee', 
                                text =  'x' if self.cnumber == -1 else str(self.cnumber or ' '))
                self.cbutton.bind("<Button-3>", lambda even = None:... )
        def get_cnumber(self):
            return self.cnumber
        def set_cnumber(self, cnumber):
            self.cnumber = cnumber
        def get_cbutton(self):
            return self.cbutton
        def set_cbutton(self, cbutton):
            self.cbutton = cbutton
        def click_command(self, other):
            return lambda:other.click(self.__y, self.__x)
        def set_flage(self, even = None):
            if self.flage:
                self.flage = False
                self.cbutton.config(text = '　')
            else:
                self.flage = True
                self.cbutton.config(text = "?")

    def __init__(self):
        super().__init__()
        self.title('扫雷游戏')
        self.height = self.width = 8
        self.xnum = 10
        self.put_xxx()
        self.cnums()
        self.t_frame = tk.Frame(self)
        self.t_frame.pack(pady = 7)
        b1 = tk.Button(self.t_frame, text = '自定义游戏', command = self.setup_config, padx = 5, pady = 3)
        b1.bind("<Return>", self.setup_config)
        b1.pack(side = tk.LEFT)
        self.label = tk.Label(self.t_frame, text = '00:00')
        self.label.pack(side = tk.LEFT, padx = 15, pady = 3)
        b2 = tk.Button(self.t_frame, text = ' 再来一局 ', command = self.setup_UI, padx = 5, pady = 3)
        b2.bind("<Return>", self.setup_UI)
        b2.pack(side = tk.RIGHT)
        start_time = 0
        self.setup_UI(0)
        self.mainloop()

    def setup_UI(self, flage = 1):
        def get_box(self):
            self.put_xxx()
            self.cnums()
            box_frame = tk.Frame(self)
            for x, i in enumerate(self.clist):
                frame = tk.Frame(box_frame)
                for y, j in enumerate(i):
                    b = tk.Button(frame,width=3,height=2,activebackground='#eee',bg='#ccc',command=j.click_command(self))
                    b.bind("<Button-3>", j.set_flage)
                    j.set_cbutton(b)
                    j.get_cbutton().pack(side = tk.LEFT)
                frame.pack()
            return box_frame
        if flage:
            self.box_frame.destroy()
            self.box_frame = get_box(self)
        else:self.box_frame = get_box(self)
        self.box_frame.pack()
        self.start_time = 0
        self.time_go = True
        self.update_clock()
    #自定义游戏弹窗
    def setup_config(self, event = None):
        res = self.ask_checker_info()
        # print(res)
        if res is None:return
        self.height, self.width, self.xnum = res
        self.setup_UI()

    #计算方块的数字
    def cnums(self):
        def cnum(a, b):
            number = 0
            for (i, j) in self.around_checker:
                flage = -1 < a+i < self.height and -1 < b+j < self.width and (self.clist[a+i][b+j].get_cnumber() == -1)
                number += 1 if flage else 0
            return number
        for i in range(self.height):
            for j in range(self.width):
                if self.clist[i][j].get_cnumber() != -1: self.clist[i][j].set_cnumber(cnum(i, j))

    #随机分布雷
    def put_xxx(self):
        self.clist = [] 
        for i in range(self.height):
            l = []
            for j in range(self.width):
                l.append(self.Checker(j,i))
            self.clist.append(l)
        xl = sample([x for i in self.clist for x in i], self.xnum)
        for i in xl:
            i.set_cnumber(-1)

    #点击事件
    def click(self, x, y):        
        if not self.start_time: self.start_time = time()
        def is_end(self, x, y):
            #全部显示
            def show_all(self, info):
                for i in self.clist:
                    for j in i:
                        j.cbutton.config(command = tk.DISABLED)
                        if j.get_cnumber() == -1: j.cbutton.config(text =  'x')
                self.time_go = False
                self.wait_window(MyDialog(info))
            #判断是否失败
            fail = self.clist[x][y].get_cnumber() == -1
            if fail:
                info = 'GAME OVER!\n游戏结束'
                show_all(self, info)
            #判断是否成功
            success = True
            for i in self.clist:
                for j in i:
                    if not j.get_cstatus() and j.get_cnumber() != -1: success = False
            if success:
                show_all(self, 'YOU WIN!\n恭喜通关')
            return fail or success
        if self.clist[x][y].flage: return
        #点击事件            
        self.clist[x][y].set_cstatus(True)
        if is_end(self, x, y): return
        if self.clist[x][y].get_cnumber(): return
        for (i, j) in self.around_checker:
            if -1 < x + i < self.height and -1 < y + j < self.width:
                if not self.clist[x+i][y+j].get_cstatus(): self.click(x+i, y+j)
                if self.clist[x+i][y+j].get_cnumber() == -1: return
    #获取弹窗中的内容
    def ask_checker_info(self):
        inputDialog = MyDialog()
        self.wait_window(inputDialog)
        return inputDialog.Checker_info
    #计时功能
    def update_clock(self):        
        if self.start_time: 
            T = time() - self.start_time
            h = T // 3600
            m = T // 60 % 60
            s = T % 60
            if h:   info = '{:0>2.0f}:{:0>2.0f}:{:0>2.0f}'.format(h, m, s)
            else: info = '{:0>2.0f}:{:0>2.0f}'.format(m, s)
            self.label.config(text = info)
        else: self.label.config(text = '00:00')
        if self.time_go: self.after(self.time_go, self.update_clock)

if __name__ == '__main__':MyApp() 