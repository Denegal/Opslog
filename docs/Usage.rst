Opslog Usage
++++++++++++

This script is used to fill in operator notes automatically in .csv file format.
You can use this functions to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be careful to use single quote marks around commands or notes if they contain anything
that bash will try to interpret ($ or ! for example)

Basic Info
==========

The basic usage and flags::

    opslog.py [-h | -v | -o | -lo | -so operator] [-p #] [-i a.b.c.d/f]
                 [-C 'Command' | -c 'Command'] [-n 'text']
                 [-f Flag [Flag ...]] [--cat | -lf | -sf Flag [Flag ...]]


Log File Syntax
===============

The log file for each operator is stored in .csv format; delimited by semicolons (;).
The syntax is always the same::

    date;operator name;flag;paa;ip address;command;executed;note

The eight fields are::

    - Date:     The date and time the entry was made in UTC timezone
        - YYYY-MM-DD HH:MM:SS
    - Operator: The operator who made the entry
    - Flag:     Tags used in a log entry. These can be used later for searching or catagorizing entries
    - PAA:      The pre-approved action number. This is dependant on mission and crew lead
    - IP:       Any IP address involved with the entry.
    - Command   The command syntax used.
    - Executed  Field used only when Command field is present
        - 'Yes' if the command was executed after logging
        - 'No' if the command was not executed or failed to execute
    - Note      The actual note entry to log.


Administration Arguments
========================

The following arguments are mutually exclusive and either display program
information or modify operator settings. If used, they will override any other
flags and no log entry will be created.

The admin arguments are::

  -h, --help            show this help message and exit
  -v, --version         Show program version information
  -o, --operator        Show the current operator
  -lo                   List all operators
  -so operator,
   --set-operator operator
                        Set the current operator

Most useful are the -o and -so arguments which are used to show/set the operator


Management Arguments
====================

The following arguments are mutually exclusive and are used to export or merge
operator logs.

The management arguments are::

  --export FILE     Export the current log
  --export-json FILE    Export the current log in json format
  --merge File1 File2   Merge multiple log files together into one

Note: The files can be given in absolute or relative path. If no path is specified
the file will output to the current directory.

Note 2: The merge command can accept any number of log files. It will first check to ensure all
supplied files are in the correct format, and then ask for the output log name before merging.

Output Arguments
================

The following arguments are mutually exclusive and display the current operator's
log or selective information in it. If used, they will override any other arguments
and no log entry will be created.

The output arguments are::

  --cat                 Output the current log (can be piped to less/more,
                        head/tail)
  -lf                   List all flags used in current operators log
  -sf Flag [Flag ...]   Search the log entries for those tagged with Flag(s)


.. _Logging-Arguments:

Logging Arguments
=================

The following arguments are not mutually exclusive, with the exception of the -c and
-C arguments, and are used to create a log entry in the current operators log. Any or
all of the arguments may be used in any order.

The logging arguments are::

  -p #                  The pre-approved action number
  -i a.b.c.d/f          The target ip address/range
  -C 'Command'          Command syntax to log before executing
  -c 'Command'          Command syntax to log without executing
  -n 'text'             Operator notes to include in the log entry
  -f Flag [Flag ...]    Flag(s) used to tag the log entry

Note 1: When inputting command syntax and notes, use of single quote marks (') are recommended to
prevent your shell from interpreting it before logging.

Note 1 Example::

    >IP='1.2.3.4'
    >opslog -c "ping $IP" -n "Testing connectivity to the $IP variable"
    >opslog -c 'ping $IP' -n 'Testing connectivity to the $IP variable'
    >opslog --cat

    2019-04-29 18:59:24;argument_tests;;;;ping 1.2.3.4;no;Testing connectivity to the ip 1.2.3.4 variable
    2019-04-29 18:59:42;argument_tests;;;;ping $IP;no;Testing connectivity to the $IP variable


Note 2: Flags can be added with the -f option. Multiple flags may be used if space separated.
