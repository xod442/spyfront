#!/usr/bin/env python
from generate import Gen_ip
print 'test one'
test = Gen_ip.make_man('10.0.0.0',24, 4, 6)
print test
test2 = Gen_ip.make_man('10.132.0.20',24,6,4)
print '-----------------------------------------'
print test2
test3 = Gen_ip.make_loop('10.1.0.1',6,4)
print '-----------------------------------------'
print test3
test4 = Gen_ip.make_rtr('1.1.1.1',6,4)
print '-----------------------------------------'
print test4
test5 = Gen_ip.make_spine_list(4)
print '-----------------------------------------'
print test5
