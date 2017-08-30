from jsonrpclib import Server

switch = '10.1.8.192'
cvp_user = 'admin'
cvp_word = 'admin'
url = 'http://%s:%s@%s/command-api' % (cvp_user,cvp_word,switch)
switcher = Server(url)

#response = switcher.runCmds(1,['show interfaces'])
response = switcher.runCmds(1,['show version'])
print response
