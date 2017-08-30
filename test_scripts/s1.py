#!/usr/bin/env python
from generate import Gen_ip
from configlet import letzbuild
print 'test one'
cvp = '10.132.0.77'
cvp_user='cvpadmin'
cvp_word='Grape123'
project='aarg2'

letzbuild.interfaces(cvp,cvp_user,cvp_word,project)
