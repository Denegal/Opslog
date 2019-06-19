Opslog Examples
+++++++++++++++

Displaying and Changing the Current Operator
============================================

The current operator is stored in the program configuration file and is
referenced whenever log entries are made or the log is queried. You can
find the current operator by using the ``opslog -o`` command.

- Example::

    > opslog -o
    test_operator

Whenever the current operator is changed, the configuration file is updated to
reflect the new operator. You can change the current operator using the
``opslog -so`` command.

- Example::

    > opslog -o
    test_operator

    > opslog -so new_operator
    > opslog -o
    new_operator

Creating Log Entries
====================

Log entires are created by using any or all of the `Logging-Arguments`.
These can be as simple as a timestamped note using ``opslog -n 'note'`` command,
or as complicated as a full entry using all six arguments.

- Example 1::

    > opslog -n 'This is a simple operator note'
    > opslog --cat

               Date         Operator       Flag PAA IPs Command Syntax Executed              Note
    2019-04-30 13:44:10  Example Operator                                        This is a simple operator note

- Example 2::

    > opslog -c 'ping 1.2.3.4' -n 'This entry includes a command'
    > opslog --cat

           Date             Operator       Flag PAA IPs   Command Syntax  Executed              Note
    2019-04-30 13:46:42  Example Operator                ping 1.2.3.4         no     This entry includes a command


- Example 3::

        > opslog -p 1 -i '127.0.0.1' -C 'ping -c 4 127.0.0.1' -f 'testing' -n 'This is a full note with command execution'
        PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
        64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.027 ms
        64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.037 ms
        64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.036 ms
        64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.038 ms

        --- 127.0.0.1 ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 59ms
        rtt min/avg/max/mdev = 0.027/0.034/0.038/0.007 ms
        > opslog --cat

            Date                Operator        Flag     PAA     IPs            Command Syntax    Executed              Note
        2019-04-30 13:48:36  Example Operator  testing     1   127.0.0.1     ping -c 4 1.2.3.4      yes     This is a full note with command execution


  - Note 1: In all three examples. the ``opslog --cat`` command is executed to show the contents of the log.

  - Note 2: In example 2, the 7th field(executed) lists 'no' because the command syntax was entered with the ``-c`` option. This option only logs the command but does not attempt to execute it.

  - Note 3: In example 3, the 7th field(executed) lists 'yes' because the command syntax was entered with the ``-C`` option. This option creates the log entry and then attempts to execute the command exactly as entered. Example 3 also shows the results of the executed command.

Displaying and Searching the Log
================================

Logs can be easily displayed using the ``opslog --cat`` command. The log displayed will always
be the current operators log only. the output from this command can be piped into other commands
as needed such as ``head``, ``less``, or ``grep``.

- Example 1::

    > opslog -o
    Example Operator
    > opslog --cat

              Date              Operator            Flag        PAA IPs Command Syntax Executed              Note
    1  2019-04-30 14:00:03  Example Operator                                                     Sample Entry 1
    2  2019-04-30 14:00:06  Example Operator                                                     Sample Entry 2
    3  2019-04-30 14:00:31  Example Operator  mission                                            Sample Entry 3, with flag
    4  2019-04-30 14:00:38  Example Operator  mission                                            Sample Entry 4, with flag
    5  2019-04-30 14:00:49  Example Operator  opschecks                                          Sample Entry 5, with flag 2
    6  2019-04-30 14:00:52  Example Operator  opschecks                                          Sample Entry 6, with flag 2
    7  2019-04-30 14:01:14  Example Operator  example opschecks                                  Sample Entry 7, with 2 flags
    8  2019-04-30 14:01:25  Example Operator  example mission                                    Sample Entry 8, with 2 flags

- Example 2::

    > opslog --cat | head -n4

          Date              Operator            Flag        PAA IPs Command Syntax Executed              Note
    1  2019-04-30 14:00:03  Example Operator                                                     Sample Entry 1
    2  2019-04-30 14:00:06  Example Operator                                                     Sample Entry 2
    3  2019-04-30 14:00:31  Example Operator  mission                                            Sample Entry 3, with flag

Although the logs can be searched by piping to grep, Flags provide a much more efficient way of
tagging entries of particular interest. You can list out all the flags used in the current log
using the ``opslog -lf`` command.

- Example::

    > opslog --lf

        Below are the flags being used in the current log

            Count      Flag            Entries
            -----      -----           -------
            3          opschecks       [5, 6, 7]
            3          mission         [3, 4, 8]
            2          example         [7, 8]

You can also search for and display log entries based on the flags the entry was tagged with using
the ``opslog -sf flag`` command. The command can accept multiple flags in it's search.

- Example 1::

    > opslog -sf opschecks

            Date              Operator            Flag        PAA IPs Command Syntax Executed              Note
    5  2019-04-30 14:00:49  Example Operator  opschecks                                          Sample Entry 5, with flag 2
    6  2019-04-30 14:00:52  Example Operator  opschecks                                          Sample Entry 6, with flag 2
    7  2019-04-30 14:01:14  Example Operator  example opschecks                                  Sample Entry 7, with 2 flags

- Example 2::

    > opslog -sf example mission

            Date              Operator            Flag        PAA IPs Command Syntax Executed              Note
    3  2019-04-30 14:00:31  Example Operator  mission                                            Sample Entry 3, with flag
    4  2019-04-30 14:00:38  Example Operator  mission                                            Sample Entry 4, with flag
    7  2019-04-30 14:01:14  Example Operator  example opschecks                                  Sample Entry 7, with 2 flags
    8  2019-04-30 14:01:25  Example Operator  example mission                                    Sample Entry 8, with 2 flags


Exporting and Merging Logs
==========================

Once the logs are complete, they can be exported by using the ``opslog --export`` command
and specifying the export location and optional format. The location can use absolute or relative path, and will
output to the current directory if only a filename is given


- Example::

    > ls -l ~/tmp/
    total 0
    > opslog --export ~/tmp/log
    Log file successfully exported
    >ls -l ~/tmp/
    total 4
    -rw-r--r-- 1 assessor assessor 594 Apr 30 10:24 log
    > cat ~/tmp/log
              Date              Operator            Flag        PAA IPs Command Syntax Executed              Note
    1  2019-04-30 14:00:03  Example Operator                                                     Sample Entry 1
    2  2019-04-30 14:00:06  Example Operator                                                     Sample Entry 2
    3  2019-04-30 14:00:31  Example Operator  mission                                            Sample Entry 3, with flag
    4  2019-04-30 14:00:38  Example Operator  mission                                            Sample Entry 4, with flag
    5  2019-04-30 14:00:49  Example Operator  opschecks                                          Sample Entry 5, with flag 2
    6  2019-04-30 14:00:52  Example Operator  opschecks                                          Sample Entry 6, with flag 2
    7  2019-04-30 14:01:14  Example Operator  example opschecks                                  Sample Entry 7, with 2 flags
    8  2019-04-30 14:01:25  Example Operator  example mission                                    Sample Entry 8, with 2 flags

- Example 2::

    > ls -l ~/tmp/
    total 0
    > opslog --export ~/tmp/log.csv --format csv
    Log file successfully exported
    >ls -l ~/tmp/
    total 4
    -rw-r--r-- 1 assessor assessor 594 Apr 30 10:24 log.csv
    > cat ~/tmp/log.csv
    2019-04-30 14:00:03;Example Operator;;;;;;Sample Entry 1
    2019-04-30 14:00:06;Example Operator;;;;;;Sample Entry 2
    2019-04-30 14:00:31;Example Operator;mission;;;;;Sample Entry 3, with flag
    2019-04-30 14:00:38;Example Operator;mission;;;;;Sample Entry 4, with flag
    2019-04-30 14:00:49;Example Operator;opschecks;;;;;Sample Entry 5, with flag 2
    2019-04-30 14:00:52;Example Operator;opschecks;;;;;Sample Entry 6, with flag 2
    2019-04-30 14:01:14;Example Operator;example opschecks;;;;;Sample Entry 7, with 2 flags
    2019-04-30 14:01:25;Example Operator;example mission;;;;;Sample Entry 8, with 2 flags

If for any reason multiple logs need to be combined, the ``opslog --merge`` command can
do so. The command takes any number of files as arguments, checks these files to ensure they
are csv formated log files, and merges them together into one log.

- Example::

    > ls -l

    total 8
    -rw-r--r-- 1 assessor assessor 138 Apr 30 10:29 merg1_log.csv
    -rw-r--r-- 1 assessor assessor  92 Apr 30 10:30 merg2_log.csv

    > cat merg1_log.csv

    2019-04-30 15:28:32;merg1;;;;;;Sample entry 1
    2019-04-30 15:28:41;merg1;;;;;;Sample entry 2
    2019-04-30 15:29:19;merg1;;;;;;Sample entry 5

    > cat merg2_log.csv

    2019-04-30 15:28:55;merg2;;;;;;Sample entry 3
    2019-04-30 15:29:03;merg2;;;;;;Sample entry 4

    > opslog --merge merg1_log.csv merg2_log.csv

    Checking files...
    All files matches log format.
    Enter destination filename: merged_log.csv
    Enter destination log format(default, csv, json): csv
    Merge Successful

    > ls -l

    total 12
    -rw-r--r-- 1 assessor assessor 138 Apr 30 10:29 merg1_log.csv
    -rw-r--r-- 1 assessor assessor  92 Apr 30 10:30 merg2_log.csv
    -rw-r--r-- 1 assessor assessor 230 Apr 30 10:33 merged_log.csv

    > cat merged_log.csv

    2019-04-30 15:28:32;merg1;;;;;;Sample entry 1
    2019-04-30 15:28:41;merg1;;;;;;Sample entry 2
    2019-04-30 15:28:55;merg2;;;;;;Sample entry 3
    2019-04-30 15:29:03;merg2;;;;;;Sample entry 4
    2019-04-30 15:29:19;merg1;;;;;;Sample entry 5

  - Note 1: Currently, all logs you are attempting to merge MUST be in csv format or the merge will fail.