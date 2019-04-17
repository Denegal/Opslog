import argparse
import sys
import os

_desc = """This script is used to fill in operator notes automatically while performing commands.
You can use this functions to simply input timestamped notes using the -n option alone.
Commands input with the -C option will be executed exactly as entered after logging.
Be careful to use single quote marks around commands or notes if they contain anything
that bash will try to interpret ($ or ! for example)
  
log file syntax is:
    date;operator name;flag;paa;ip address;command;executed;note
    
Date format:
    YYYY-MM-DD HH:MM:SS"""

try:
    operator = os.environ['OPS_LOG_USER']
except KeyError as e:
    operator = 'pytest_operator'
    os.environ['OPS_LOG_USER'] = 'pytest_operator'

logdir = '/home/assessor/working_dir/ops_logs'
logfile = os.path.join(str(logdir), operator)
alias = '/etc/profile.d/opslog_data.sh'


def get_operator():
    print(os.getenv('OPS_LOG_USER'))


def set_operator(value):
    os.environ['OPS_LOG_USER'] = value


def cat_log():
    log = open(logfile).read()
    print(log)


def main(args):
    print(args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=_desc)

    root_group = parser.add_mutually_exclusive_group()
    admin_group = root_group.add_argument_group()
    admin_group.description = 'Use the following commands to manage or change the current operator log'
    admin_group.add_argument(
        '-o', '--operator',
        action='store_const',
        const=get_operator,
        help='Show the current operator'
    )
    admin_group.add_argument(
        '-so', '--set-operator',
        dest='operator',
        nargs=1,
        type=str,
        help='Set the current operator'
    )
    log_group = root_group.add_argument_group()
    log_group.description = 'Use any or all of the following commands to put an entry into the current operator log'
    log_group.add_argument(
        '-p',
        dest='#',
        nargs=1,
        type=int,
        action='store',
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
        help='Flag used to tag the log entry'
    )

    display_group = root_group.add_mutually_exclusive_group()
    display_group.description = "Use the following commands to display or search the current operator log"
    display_group.add_argument(
        '--cat',
        action='store_const',
        const=cat_log,
        help='Output the current log (can be piped to less/more, head/tail)'
    )

    args = parser.parse_args()

    if args.set_operator:
        set_operator(args.set_operator)
        exit()

    args.show_operator() if args.show_operator else args.cat() if args.cat else main(args)
