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



# New way

[10:09 0.21 ~ ]
[ferrazpc 10] ~ > /home/cs/richard/Free_Lamp81/START_lamp -nws

Getting source from /home/cs/richard/Free_Lamp81/lamp ......
bash: line 0: unalias: rm: not found
bash: line 0: unalias: cp: not found
bash: line 0: unalias: mv: not found
update81a.rt loaded ...
Lamp> 
Lamp> 
Lamp> 
Lamp> w1=dist(50)
w 1: Float   dim = 50 * 50 min=0.00000 max=35.3553
Lamp> w2=w1
w 2: Float   dim = 50 * 50 min=0.00000 max=35.3553
Lamp> print,w1[*,0]
      0.00000      1.00000      2.00000      3.00000      4.00000      5.00000
      6.00000      7.00000      8.00000      9.00000      10.0000      11.0000
      12.0000      13.0000      14.0000      15.0000      16.0000      17.0000
      18.0000      19.0000      20.0000      21.0000      22.0000      23.0000
      24.0000      25.0000      24.0000      23.0000      22.0000      21.0000
      20.0000      19.0000      18.0000      17.0000      16.0000      15.0000
      14.0000      13.0000      12.0000      11.0000      10.0000      9.00000
      8.00000      7.00000      6.00000      5.00000      4.00000      3.00000
      2.00000      1.00000
w 1: Float   dim = 50 * 50 min=0.00000 max=35.3553
Lamp> w3=total(w1,2)
w 3: Float   dim = 50 min=625.000 max=1434.86
Lamp> write_lamp,w=3,foramt='Column'

write_lamp,w=3,foramt=�'Column'
                        ^
% Syntax error.
Syntax error.
Syntax error.

write_lamp,w=3,foramt='Column'
% Keyword FORAMT not allowed in call to: WRITE_LAMP
Keyword FORAMT not allowed in call to: WRITE_LAMP
Keyword FORAMT not allowed in call to: WRITE_LAMP

Lamp> write_lamp,w=3,format='Column'
file not saved ...!
Lamp> 
Lamp> write_lamp,'totot',w=3,format='Column'
Lamp> 
Lamp> write_lamp,'totot',w=3,format='HDF'
W3 saved in totot_LAMP.hdf
Lamp> 


```

