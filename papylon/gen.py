# -*- coding: utf-8 -*-


class Gen:
    def __init__(self, gen):
        self.gen = gen()

    def generate(self):
        return self.gen.send(None)