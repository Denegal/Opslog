usage: opslog.py [-h] [-p #] [-i a.b.c.d/f] [-C 'Command' | -c 'Command']
                 [-n 'text'] [-f Flag [Flag ...]] [--cat]

This script is used to fill in operator notes automatically while performing commands.
You can use this functions to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be careful to use single quote marks around commands or notes if they contain anything
that bash will try to interpret ($ or ! for example)
  
log file syntax is:
    date;operator name;flag;paa;ip address;command;executed;note
    
Date format:
    YYYY-MM-DD HH:MM:SS

optional arguments:
  -h, --help          show this help message and exit
  -p #                The pre-approved action number
  -i a.b.c.d/f        The target ip address/range
  -C 'Command'        Command syntax to log before executing
  -c 'Command'        Command syntax to log without executing
  -n 'text'           Operator notes to include in the log entry
  -f Flag [Flag ...]  Flag used to tag the log entry
  --cat               Output the current log (can be piped to less/more,
                      head/tail)
