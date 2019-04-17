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

logdir = '/home/assessor/working_dir/ops_logs'
logfile = os.path.join(str(logdir), operator)
alias = '/etc/profile.d/opslog_data.sh'


def get_operator():
    return os.environ['OPS_LOG_USER']


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
    parser.add_argument(
        '-p',
        metavar='#',
        nargs=1,
        type=int,
        action='store',
        help='The pre-approved action number'
    )
    parser.add_argument(
        '-i',
        metavar='a.b.c.d/f',
        nargs=1,
        type=str,
        help='The target ip address/range'
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-C',
        metavar="'Command'",
        nargs=1,
        type=str,
        help='Command syntax to log before executing'
    )
    group.add_argument(
        '-c',
        metavar="'Command'",
        nargs=1,
        type=str,
        help='Command syntax to log without executing'
    )
    parser.add_argument(
        '-n',
        metavar="'text'",
        nargs=1,
        type=str,
        help='Operator notes to include in the log entry'
    )
    parser.add_argument(
        '-f',
        metavar='Flag',
        nargs='+',
        type=str,
        help='Flag used to tag the log entry'
    )
    parser.add_argument(
        '--cat',
        action='store_const',
        const=cat_log,
        help='Output the current log (can be piped to less/more, head/tail)'
    )

    args = parser.parse_args()
    args.cat() if args.cat else main(args)
