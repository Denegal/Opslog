This program is used to fill in operator notes automatically while performing commands.
You can use this function to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be carefull to use single quote marks around commands or notes if they contain anything
which bash will try to interpret ($ or ! for example)

The first time the program is run it must be run with ./opslog.sh --setup
as root or with sudo. Afterwards, the user can use the shorthand opslog to
run the program from anywhere.

Usage: opslog [options]

Examples:

		opslog --cat

		opslog -p # -i 'ip_address' -C 'command syntax' -n 'Operator Notes' -f 'flag'

		opslog -n 'Quick operator note'

		opslog -sf 'flag flag2'


Options:

       -p       The Pre-Approved Action number
       -i       The Ip Addresses involved
       -C       The command syntax used. Will execute after logging
       -c       The command syntax used. WILL NOT execute after logging
       -n       Operator notes to log
       -f       flag (used for tagging note entries)
       -lf      List all flags currently used
       -sf      search for and display entries tagged with flag
    
       --setup  Setup the logging or change user (Must be done as root or via SUDO)
    
       --cat    Output the current users log (can then be piped to less/more, head/tail)

log file syntax is:

    date;operator name;flag;paa;ip address;command;executed?;notes

Date format:

    YYYY-MM-DD HH:MM:SS +zone

