.. OpsLog documentation master file, created by
   sphinx-quickstart on Mon Apr 29 11:02:23 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpsLog's documentation!
**********************************

The opslog program is designed to allow operators to take detailed notes
quickly and efficiently from the terminal without the need to open additional
programs or enter VM's. Multiple operators can take notes on a single machine,
as each operator's notes, are stored in separate logs, and the current operator
can be switched quickly without the need for restarting the terminal. Logs can
be exported in .csv format, allowing for easy import into any program that accepts
it (excel for example).

Log entries are created from the terminal from anywhere on the system
Each log entry contains a timestamp and the operators name, in addition to information
provided by the operator. Currently each log entry can hold the following:

    - A pre-approved action number
    - An ip address/range
    - Command syntax
    - Multiple flags used to tag entries
    - Notes by the operator about the action taken

Using flags to tag log entries allows operators to later search through their
logs easily and display entries of interest or entries regarding particular
events.

Additionally, the program allows operators to log commands as they are run using
the command syntax field. The command input here can, if the operator chooses, be
executed after logging, giving a timestamped record of when commands were run on the
network.

Finally, multiple logs can be merged together. Merged logs are automatically sorted
properly based on time, allowing an operator to combine their logs from multiple
machines into one concise log or for multiple operator logs to be combined to
create an msl.



Documentation for the Code
**************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Installation
   Usage
   Examples

