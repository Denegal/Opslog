This script is used to fill in operator notes automatically while performing commands.
You can use this functions to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be careful to use single quote marks around commands or notes if they contain anything
that bash will try to interpret ($ or ! for example)


    usage: opslog.py [-h | -v | -o | -so operator]  [-p #]  [-i a.b.c.d/f]
       [-C 'Command' | -c 'Command']    [-n 'text']
       [-f Flag [Flag ...]] [--cat | -lf | -sf Flag [Flag ...]]
       
         
log file syntax is:
 
    date;operator name;flag;paa;ip address;command;executed;note
    
Date format:
 
    YYY-MM-DD HH:MM:SS
     
  
     
Admin arguments:
 
  Use the following commands to retrieve program information or set operator

  
    -h, --help            show this help message and exit
    -v, --version         Show program version information
    -o, --operator        Show the current operator
    -lo                   List all operators
    -so operator, 
     --set-operator operator
                          Set the current operator

 
 
Logging arguments:

  Use any or all of the following commands to put an entry into the current operator log


    -p #                  The pre-approved action number
    -i a.b.c.d/f          The target ip address/range
    -C 'Command'          Command syntax to log before executing
    -c 'Command'          Command syntax to log without executing
    -n 'text'             Operator notes to include in the log entry
    -f Flag [Flag ...]    Flag(s) used to tag the log entry

 
 
Output Arguments:

  Use the following commands to display or search the current operator log


    --cat                 Output the current log (can be piped to less/more,
                        head/tail)
    -lf                   List all flags used in current operators log
    -sf Flag [Flag ...]   Search the log entries for those tagged with Flag(s)
 
 
 
Management Arguments:

  Use the following commands to manage the operator log


    --export FILENAME     Export the current log
    --merge F1 F2 [F3...] Merge multiple log files together into one log
