

Overview on How to Install and setup this Script
++++++++++++++++++++++++++++++++++++++++++++++++

Simple Installation/Upgrade
===========================

1. Download the opslog program and extract zip file

2. Inside the opslog folder run the opslog program as root or with sudo privileges.

    - Example: ``sudo ./opslog_installer``

3. Follow the prompts to complete install/upgrade of the program

4. If installing, restart terminal and ensure alias is working by running ``opslog``

    - If the opslog program help is displayed, the program installed correctly
    - The original folder can now be removed if desired




Install Location
================

opslog is installed to the /usr/lib/ops_log/ directory.
The folder is created with root privileges and the sticky bit set.
This allows the program to access it's configuration file and create
operator logs regardless of the user running it (after install, root
privileges are not required to run the program or create logs.)

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
    drwxrwxr-x 4 root root  4096 Apr 29 15:35 help
    drwsrwxrwx 2 root root 4096 Apr 29 10:50 operator_logs
    -rwxrwxr-x 1 root root 15216 Apr 29 15:47 opslog

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
shortcut after installation, users can manually create this alias by adding the line::

    alias opslog='/usr/lib/ops_log/opslog'

in their .bashrc file found in their home directory.


A man page is created for the program and can be access with the command::

    man opslog


Simple Uninstall
===================

1. Ensure all log file are backed up by exporting or copying logs

    - Example: ``opslog --export ~/Desktop/log_backup --format csv``

    - Example: ``cp /usr/lib/ops_log/operator_logs/* ~/Desktop/log_backups/``

2. Run the following commands to remove the opslog program files, alias file, and man page

    - ``sudo rm -rf /usr/lib/ops_log/``

    - ``sudo rm /etc/profile.d/opslog_alias.sh``

    - ``sudo /usr/share/man/man1/opslog.1``

3. Restart terminal

    - The opslog program is now uninstalled
