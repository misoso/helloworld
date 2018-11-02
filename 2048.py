#! /usr/bin/python3
from __future__ import unicode_literals
# coding=utf-8

import pandas as pd
import random


class Game(object):

    def __init__(self, l):
        level = {0: 1024, 1: 2048, 2: 4096, 3: 8192}
        self.level = level[l]
        self.index = ((0, 0), (0, 1), (0, 2), (0, 3),
                      (1, 0), (1, 1), (1, 2), (1, 3),
                      (2, 0), (2, 1), (2, 2), (2, 3),
                      (3, 0), (3, 1), (3, 2), (3, 3))
        self.wasd = {'w': self.up, 'a': self.left,
                     's': self.down, 'd': self.right}
        self.data = [0] * 16
        self.game = pd.Series(data=self.data)
        self.game.index = self.index
        # print(self.game)
        self.setnum(2)
        self.data = '游戏退出'
        self.play()

    def setnum(self, n=1):
        n -= 1
        flage = True
        for i in self.game:
            if i == self.level:
                self.data = '达成目标'
                return True
            if i == 0:
                flage = False
        if flage:
            self.data = '你输了！'
            return True

        while True:
            index = random.randrange(0, 16)
            if self.game[index] == 0:
                break
        self.game[index] = random.randrange(2, 5, 2)

        for _ in range(n):
            self.setnum()

    def out(self):
        for x, y in self.game.index:
            print(self.game[(x, y)], end='\t')
            if y == 3:
                print()

    def __del__(self):
        print(self.data)

    def play(self):
        while True:
            self.out()
            try:
                i = input('>>>')
            except:
                break
            if i == 'q':
                break
            dirct = self.wasd.get(i, None)
            if dirct:
                dirct()
                if self.setnum():
                    break

    def left(self):
        for x, y in self.index:
            if y == 3:
                continue
            index = 4 * x + y
            if index >= 15:
                break
            if self.game.get(index, 0) == 0:
                for i in range(1, 4 - y):
                    if self.game.get(index + i, 0):
                        self.game[index], self.game[
                            index + i] = self.game[index + i], self.game[index]
                        break
        for x in range(4):
            for y in range(3):
                index = 4 * x + y
                if self.game.get(index + 1, 0) == self.game.get(index, 0):
                    self.game[index] *= 2
                    self.game[index + 1] = 0
                    break
        for x, y in self.index:
            if y == 3:
                continue
            index = 4 * x + y
            if index >= 15:
                break
            if self.game.get(index, 0) == 0:
                for i in range(1, 4 - y):
                    if self.game.get(index + i, 0):
                        self.game[index], self.game[
                            index + i] = self.game[index + i], self.game[index]
                        break

    def right(self):
        for x in range(4):
            self.game[4 * x], \
                self.game[4 * x + 1], \
                self.game[4 * x + 2], \
                self.game[4 * x + 3] = \
                self.game[4 * x + 3], \
                self.game[4 * x + 2], \
                self.game[4 * x + 1], \
                self.game[4 * x]
        self.left()
        for x in range(4):
            self.game[4 * x], \
                self.game[4 * x + 1], \
                self.game[4 * x + 2], \
                self.game[4 * x + 3] = \
                self.game[4 * x + 3], \
                self.game[4 * x + 2], \
                self.game[4 * x + 1], \
                self.game[4 * x]

    def up(self):
        for x, y in self.index:
            if x == 3:
                continue
            index = 4 * x + y
            if index >= 15:
                break
            if self.game.get(index, 0) == 0:
                for i in range(1, 4 - x):
                    i *= 4
                    if self.game.get(index + i, 0):
                        self.game[index], self.game[
                            index + i] = self.game[index + i], self.game[index]
                        break
        for y in range(4):
            for x in range(3):
                index = 4 * x + y
                if self.game.get(index + 4, 0) == self.game.get(index, 0):
                    self.game[index] *= 2
                    self.game[index + 4] = 0
                    break
        for x, y in self.index:
            if x == 3:
                continue
            index = 4 * x + y
            if index >= 15:
                break
            if self.game.get(index, 0) == 0:
                for i in range(1, 4 - x):
                    i *= 4
                    if self.game.get(index + i, 0):
                        self.game[index], self.game[
                            index + i] = self.game[index + i], self.game[index]
                        break

    def down(self):
        for x in range(4):
            self.game[x], \
                self.game[x + 1 * 4], \
                self.game[x + 2 * 4], \
                self.game[x + 3 * 4] = \
                self.game[x + 3 * 4], \
                self.game[x + 2 * 4], \
                self.game[x + 1 * 4], \
                self.game[x]
        self.up()
        for x in range(4):
            self.game[x], \
                self.game[x + 1 * 4], \
                self.game[x + 2 * 4], \
                self.game[x + 3 * 4] = \
                self.game[x + 3 * 4], \
                self.game[x + 2 * 4], \
                self.game[x + 1 * 4], \
                self.game[x]


if __name__ == '__main__':
    game = Game(2)
