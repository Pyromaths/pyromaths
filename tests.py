#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyromaths import LesFiches
import codecs
for j in range(100):
    f0 = codecs.open('/tmp/test.tex', encoding='utf-8', mode='w')
    f1 = codecs.open('/tmp/test-cor.tex', encoding='utf-8', mode='w')
    for n in range(len(LesFiches)):
        for i in range(len(LesFiches[n][2])):
            LesFiches[n][1].main(i, f0, f1)
    f0.close()
    f1.close()
