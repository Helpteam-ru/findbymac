import pexpect
import re
from pprint import pprint

from settings import devices

def send_show_command(ip, username, password, enable, command, prompt=">"):
    with pexpect.spawn(f"ssh {username}@{ip}", timeout=20, encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        ssh.expect([">", "#"])
        if enable:
            ssh.sendline(enable)
            enable_status = ssh.expect(["#","Switch to extended CLI mode?"])
            if enable_status== 1:
                ssh.sendline("y")
                ssh.expect("[Pp]assword:")
                ssh.sendline("foes-bent-pile-atom-ship")
                enable_status = ssh.expect("Warning: Extended CLI mode is intended for developers to test the system. Before using commands in extended CLI mode, contact the Technical Support and make sure you know the potential impact on the device and the network.")
                ssh.expect(prompt)

        ssh.sendline(command)
        output = ""

        while True:
            match = ssh.expect([prompt, "---- More ----","--More-- or \(q\)uit", pexpect.TIMEOUT])
            page = ssh.before.replace("\r\n", "\n").replace("\r\r               \r","").replace("\r                  \r","")
            page = re.sub(" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match in [1,2]:
                ssh.send(" ")
            else:
                print("Ошибка: timeout")
                break
        output = re.sub("\n +\n", "\n", output)
        return output


if __name__ == "__main__":
    print("enter MAC to find",end=">")
    findMAC=input().replace(":","").replace("-","").upper()
    found=False
    print(f"Searching for {findMAC}...")

    for dev in devices:
        dev['id']=re.search(r"A-\d*",dev["promt"])[0]
        print(f"Parsing {dev['ip']}...",end="\r")
        result = send_show_command(dev['ip'], "admin", dev['pass'], dev['sudo'],dev["cmd"] , dev["promt"])#"display lldp neighbor-information list"
        #print(result) ## .replace(":","").replace("-","")
        with open(f"{dev['ip']}_mac_result.txt", "w") as f:
            f.write(result)
        # mac.translate(None,"-:")
        for l in re.finditer(dev["reg"],result):
            d=l.groupdict()
            print(f"Parsing {dev['ip']}...",end="\r")
            d['MAC']=d['MAC'].replace(":","").replace("-","").upper()
            if d["if"] in dev['trunks']: continue #do not report MAC as found if it is in trunk port
            if d['MAC'].find(findMAC)!=-1:
                if not found:
                    print(f"SWITCH         MAC        VLAN interface")
                    found=True
                print(f"{dev['id']} = {d['MAC']:15} {d['VLAN']:4} {d['if']}")

    if not found: print(f"Nothing like {findMAC} found :(")
