Reduction Scripts
===============

This is an independent folder!

Home folder configuration should go in the local config.ini.

## For remote connections please add the public key of the reduction server machine to the authorised keys of the processing machine:

If the reduction server is installed in the **A** machine with user **a**, and the processing machine is **B** with user **b**:
(source: [The linux problem base](http://www.linuxproblem.org/art_9.html). )

1. Generate public key in the server machine if it does not exist yet.

```bash
a@A:~> ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/a/.ssh/id_rsa): 
Created directory '/home/a/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/a/.ssh/id_rsa.
Your public key has been saved in /home/a/.ssh/id_rsa.pub.
The key fingerprint is:
3e:4f:05:79:3a:9f:96:7c:3b:ad:e9:58:37:bc:37:e4 a@A
```

2. Now use ssh to create a directory ~/.ssh as user b on B. (The directory may already exist, which is fine):

```bash
a@A:~> ssh b@B mkdir -p .ssh
b@B's password: 
```

3. Finally append a's new public key to b@B:.ssh/authorized_keys and enter b's password one last time:

```bash
a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
b@B's password:
```
 
4. From now on you can log into B as b from A as a without password:

```bash
a@A:~> ssh b@B hostname
B
```



# Running LAMP in a remote machine:

```
#!/bin/bash
ssh -T root@barns <<\EOI

IDL_DIR=/usr/users/BarnsDir/APPLI/rsi/idl
IDL_PATH=\+$IDL_DIR/lib:\+$IDL_DIR/examples
LAMP_DIR=/usr/users/BarnsDir/APPLI/lamp
export LAMP_DIR IDL_DIR IDL_PATH
unset DISPLAY

# Run lamp
$IDL_DIR/bin/idl $LAMP_DIR/lamp.ini

; DO stuff

exit

EOI

```

