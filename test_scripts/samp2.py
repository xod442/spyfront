#!/usr/bin/env python
from generate import Gen_ip

def main():
    # Generate counters
    spines = 4
    leafs = 6
    lanz_count = 0
    tot_links = (spines*leafs)
    leaf_count = 0
    spine_count = 0
    spine_port = 1
    leaf_port = 1
    count = 0
    net_count = 0
    l_id = 0001
    mgmt_ip ='10.132.0.0'
    loopbackz = '10.1.0.0'
    rtr_idz = '1.1.1.1'

    # Create lists

    networkz = Gen_ip.make_ip(mgmt_ip, spines, leafs)
    spinez = Gen_ip.make_spine_list(spines)
    leafz = Gen_ip.make_leaf_list(leafs)
    lanz = Gen_ip.make_lanz_list(leafs)
    loopz = Gen_ip.make_loop(loopbackz,spines,leafs)
    rtr_id = Gen_ip.make_rtr(rtr_idz,spines,leafs)

    # Build the links

    while net_count < tot_links:
        # Run loop for the number of leafs and reset for next spine
        while leaf_count < leafs:
            net = networkz[net_count]
            l_id = l_id
            sa = 65020
            ss = spinez[spine_count]
            sp = spine_port
            sip = net[1]
            sm = 30
            sn = net[0]
            la = lanz[lanz_count]
            la = int(la)
            ls = leafz[leaf_count]
            lp = leaf_port
            lip = net[2]
            lm = 30
            ln = net[0]
            link = [l_id,sa,ss,sp,sip,sm,sn,la,ls,lp,lip,lm,ln]
            print link
            leaf_count = leaf_count + 1
            net_count = net_count + 1
            spine_port = spine_port + 1
            l_id = l_id + 1
            lanz_count = lanz_count + 1
        print '-----------------------------------------------------------'
        print type(l_id)
        print type(sa)
        print type(ss)
        print type(sp)
        print type(sip)
        print type(sm)
        print type(sn)
        print type(la)
        print type(ls)
        print type(lp)
        print type(lip)
        print type(lm)
        print type(ln)
        print '-----------------------------------------------------------'
        print l_id
        print sa
        print ss
        print sp
        print sip
        print sm
        print sn
        print la
        print ls
        print lp
        print lip
        print lm
        print ln
        leaf_count = 0
        spine_count = spine_count + 1
        leaf_port = leaf_port + 1
        spine_port = 1
        lanz_count = 0
        count = count + 5
        #print loopz
        #print rtr_id

# Start program
if __name__ == "__main__":
   main()
