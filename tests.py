#!/usr/bin/python
# -*- coding: utf-8 -*-
import sixiemes.sixiemes
import cinquiemes.cinquiemes
import quatriemes.quatriemes
import troisiemes.troisiemes
import codecs
f0 = codecs.open('test.tex', encoding='utf-8', mode='w')
f1 = codecs.open('test-cor.tex', encoding='utf-8', mode='w')
for j in range(30):
    for i in range(17):
        sixiemes.sixiemes.main(i, f0, f1)
    for i in range(6):
        cinquiemes.cinquiemes.main(i, f0, f1)
    for i in range(15):
        quatriemes.quatriemes.main(i, f0, f1)
    for i in range(17):
        troisiemes.troisiemes.main(i, f0, f1)
f0.close()
f1.close()
