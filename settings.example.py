#regex for MAC/VLAN/interface/status detection from switch output
r1950=r"(?P<MAC>([0-9a-f]{4}-?){3})\s+(?P<VLAN>\d+)\s+(?P<status>\w+)\s+(?P<if>.+\/\d+\/\d+)\s+[YN]"
r1920=r"(?P<VLAN>\d+)(\s*)(?P<MAC>([0-9A-Fa-f]{2}[:-]?){6})(.{3})(?P<if>\d+)(\s*)(?P<ifindex>\d+)(\s*)(?P<status>\w*)"
rhuaw=r"(?P<MAC>([0-9a-f]{4}-?){3})\s+(?P<VLAN>\d+)\/\S*\s+(?P<if>.+\/\d+\/\d+)\s+(?P<status>\w+)"
mkrt=r"^\s?\d+\s[D\s]\s+\S+\s+(?P<MAC>([0-9A-F]{2}:?){6})\s\s(?P<if>[\w-]+)\s+\w+\s+\w+\s+\w+\s+(?P<VLAN>\d+)$"
devices = [
               {'ip':"192.168.0.2",'sudo':"xtd-cli-mode",'pass':"password",'promt':"<HP-1950>","cmd":"display mac-address","reg":r1950,"trunks":["XGE1/0/49"]},
               {'ip':"192.168.0.4",'sudo':"enable",'pass':"password",'promt':"\(HP-1920S\) #","cmd":"show mac-addr-table","reg":r1920,"trunks":["2"]},
               {'ip':"192.168.0.3",'sudo':"",'pass':"password",'promt':"<huawei>","cmd":"display mac-address","reg":rhuaw,"trunks":["XGE5/0/2"]},
               {'ip':"192.168.0.1",'sudo':"",'pass':"password",'promt':"[admin@mikrotik] >","cmd":"/interface/ethernet/switch/host/print","trunks":["ether1","ether2"]}
              ]
