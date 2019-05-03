

Overview on How to Install and setup this Script
++++++++++++++++++++++++++++++++++++++++++++++++

Simple Installation
===================

1. Ensure python3 is installed on the system

2. Copy the opslog.py file to your chosen folder and move to it
    - It is recommended not to move the program file after install
    - A folder dedicated to custom scripts is recommended

3. run ``python opslog.py``

4. Follow the prompts to install the program


Install Location
================

opslog is installed to the /usr/lib/ops_log/ directory.
The folder is created with root privileges and the sticky bit set.
This allows the program to access it's configuration file and create
operator logs regardless regardless of the user running it (root privileges
are not required to run the program or create logs.)

Inside the ops_log/ folder are the config.ini file which the script
uses for tracking the current operator, and a operator_logs/ folder
which stores the .csv file logs for the operators. Like the main installation
folder, the operator_logs folder is created by root, with sticky bit permissions
to allow the program to update logs for operators even if they were initially
created while another user was logged in.

Below is an sample directory listing of the install location::

    /usr/lib/:
    total 595256
    ....
    drwsrwxrwx  3 root root     4096 Apr 29 13:16 ops_log
    ...

    /usr/lib/ops_log/:
    total 8
    -rw-rw-rw- 1 root root   54 Apr 29 10:49 config.ini
    drwxrwxr-x 4 root root  4096 Apr 29 15:35 html
    drwsrwxrwx 2 root root 4096 Apr 29 10:50 operator_logs
    -rwxrwxr-- 1 root root 15216 Apr 29 15:47 opslog.py

    /usr/lib/ops_log/operator_logs:
    total 4
    -rw-r--r-- 1 assessor assessor 616 Apr 29 10:51 test_operator_ops_log.csv
    -rw-r--r-- 1 assessor assessor 486 Apr 29 10:57 second_operator_ops_log.csv


Post Install
============

Once the initial installation is complete, the program can be run from anywhere on the system
using the shortcut alias 'opslog'. This is due to an alias being created in the /etc/profile.d/
directory in the opslog_alias.sh file.

If for any reason this does not work and users are unable to use the 'opslog'
shortcut after installation, you can manually create this alias by adding the line::

    alias opslog='/usr/lib/ops_log/opslog.py'

in their .bashrc file found in their home directory.


A man page is also created for the program and can be access with the command::

    man opslog

