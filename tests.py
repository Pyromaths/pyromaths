#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sixiemes.sixiemes
import cinquiemes.cinquiemes
import quatriemes.quatriemes
import troisiemes.troisiemes
f0 = open('test.tex', encoding='utf-8', mode='w')
f1 = open('test-cor.tex', encoding='utf-8', mode='w')
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
