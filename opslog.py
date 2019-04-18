import argparse
import sys
import os


def _setup():
    """This function will setup the program to use aliases, setup initial operator, and create missing folders/files"""
    print('Begin setup of operator and program')
    exit()


_desc = """
usage: opslog.py [-h | -v | -o | -so operator] [-p #] [-i a.b.c.d/f]
                 [-C 'Command' | -c 'Command'] [-n 'text']
                 [-f Flag [Flag ...]] [--cat | -lf | -sf Flag [Flag ...]]

This script is used to fill in operator notes automatically while performing commands.
You can use this functions to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be careful to use single quote marks around commands or notes if they contain anything
that bash will try to interpret ($ or ! for example)
  
log file syntax is:
    date;operator name;flag;paa;ip address;command;executed;note
    
Date format:
    YYYY-MM-DD HH:MM:SS
     
     
Admin arguments:
  Use the following commands to retrieve program information or set operator
  
  -h, --help            show this help message and exit
  -v, --version         Show program version information
  -o, --operator        Show the current operator
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

 
"""

try:
    operator = os.environ['OPS_LOG_USER']
except KeyError as e:
    operator = 'pytest_operator'
    os.environ['OPS_LOG_USER'] = 'pytest_operator'
    # _setup()


logdir = '/home/assessor/working_dir/ops_logs'
logfile = os.path.join(str(logdir), operator)
alias = '/etc/profile.d/opslog_data.sh'


def get_operator():
    print(os.getenv('OPS_LOG_USER'))
    return os.getenv('OPS_LOG_USER')


def set_operator(value):
    os.environ['OPS_LOG_USER'] = value


def cat_log():
    """Display the current operators log and exit"""
    log = open(logfile).read()
    print(log)


def list_flags():
    print('Display all flags used in current log')
    exit()


def search_log(flags):
    print('search through log for flag entries: ', flags)
    exit()


def main(args):
    """This function will handle the main logging"""
    print(args)
    return args


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=_desc,
                                     add_help=False)

    root_group = parser.add_mutually_exclusive_group()
    root_group.description = 'Use the following commands to manage or change the current operator log'
    root_group.add_argument(
        '-h', '--help',
        action='version',
        version=_desc
    )
    root_group.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s version 0.1'
    )
    root_group.add_argument(
        '-o', '--operator',
        action='store_const',
        const=get_operator,
        help='Show the current operator'
    )
    root_group.add_argument(
        '-so', '--set-operator',
        metavar='operator',
        nargs=1,
        type=str,
        help='Set the current operator'
    )

    log_group = parser.add_argument_group()
    log_group.description = 'Use any or all of the following commands to put an entry into the current operator log'
    log_group.add_argument(
        '-p',
        metavar='#',
        nargs=1,
        type=int,
        help='The pre-approved action number'
    )
    log_group.add_argument(
        '-i',
        metavar='a.b.c.d/f',
        nargs=1,
        type=str,
        help='The target ip address/range'
    )
    command_group = log_group.add_mutually_exclusive_group()
    command_group.add_argument(
        '-C',
        metavar="'Command'",
        nargs=1,
        type=str,
        help='Command syntax to log before executing'
    )
    command_group.add_argument(
        '-c',
        metavar="'Command'",
        nargs=1,
        type=str,
        help='Command syntax to log without executing'
    )
    log_group.add_argument(
        '-n',
        metavar="'text'",
        nargs=1,
        type=str,
        help='Operator notes to include in the log entry'
    )
    log_group.add_argument(
        '-f',
        metavar='Flag',
        nargs='+',
        type=str,
        help='Flag(s) used to tag the log entry'
    )

    display_group = parser.add_mutually_exclusive_group()
    display_group.description = "Use the following commands to display or search the current operator log"
    display_group.add_argument(
        '--cat',
        action='store_const',
        const=cat_log,
        help='Output the current log (can be piped to less/more, head/tail)'
    )
    display_group.add_argument(
        '-lf',
        action='store_const',
        const=list_flags,
        help='List all flags used in current operators log'
    )
    display_group.add_argument(
        '-sf',
        metavar='Flag',
        nargs='+',
        type=str,
        help='Search the log entries for those tagged with Flag(s)'
    )

    args = parser.parse_args()

    if args.sf:
        search_log(args.sf)

    if args.set_operator:
        set_operator(args.set_operator[0])
        exit()

    list_flags() if args.lf else args.operator() if args.operator else args.cat() if args.cat else main(args)
