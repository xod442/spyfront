from jsonrpclib import Server

cvp_user = 'admin'
cvp_word = 'admin'


switch_list = ['10.1.8.191','10.1.8.192',
                '10.1.8.193','10.1.8.194','10.1.8.195','10.1.8.196',
                '10.1.8.197','10.1.8.198','10.1.8.199','10.1.8.200']

for switch in switch_list:

    url = 'http://%s:%s@%s/command-api' % (cvp_user,cvp_word,switch)
    switcher = Server(url)


    response = switcher.runCmds(1,['configure terminal','management api http-commands', 'no protocol http','protocol https'])
    print response
    print '------------------------------------------'
