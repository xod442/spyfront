# It's a list


ligs = [ {'networkUris' : [], 'uplinkSets' : [
    {
        'primaryPort': None,
        'networkUris':
            [
                '/rest/ethernet-networks/4b359f46-710e-4418-a0b3-c88434bcc644',
                '/rest/ethernet-networks/e7aed782-6811-4e24-b0c3-890205fd8765',
                '/rest/ethernet-networks/52ffb0c3-bb12-423f-add8-fa9c4ba642d1',
                '/rest/ethernet-networks/9f3f863c-f5ee-4610-a22d-28b0b0e743aa'
            ],
        'logicalPortConfigInfos':
            [
                {
                    'desiredSpeed': 'Auto',
                    'logicalLocation':
                        {
                            'locationEntries':
                                [
                                    {
                                        'type': 'Port',
                                        'relativeValue': 61
                                    },
                                    {
                                        'type': 'Bay',
                                        'relativeValue': 3
                                    },
                                    {
                                        'type': 'Enclosure',
                                        'relativeValue': 1
                                    }
                                ]
                        }
                },
                {
                    'desiredSpeed': 'Auto',
                    'logicalLocation':
                        {
                            'locationEntries':
                                [
                                    {
                                        'type': 'Port',
                                        'relativeValue': 61
                                    },
                                    {
                                        'type': 'Enclosure',
                                        'relativeValue': 1
                                    },
                                    {
                                        'type': 'Bay',
                                        'relativeValue': 6
                                    }
                                ]
                        }
                }
            ],
        'reachability': None,
        'nativeNetworkUri': None,
        'lacpTimer': 'Short',
        'name': 'up4skip',
        'mode': 'Auto',
        'networkType': 'Ethernet',
        'ethernetNetworkType': 'Tagged'
    }
]}]

link = []
links = []
# print c7000/Synergy port configurations

# where x = uplinkSets
# print (ligs)
for i in ligs:
    for j in i['uplinkSets']:
        for k in j['logicalPortConfigInfos']:
            for l in k['logicalLocation']['locationEntries']:
                ident = l['type']
                value = l['relativeValue']
                info = ident+'-'+str(value)
                link.append(info)
                link.sort()
            links.append(link)
            link = []
print (links)            # List of uplinks ports on frame
print (j['networkUris'])    # List of network URI's...do db lookup
links = []



print ('-------------------------------------------')
