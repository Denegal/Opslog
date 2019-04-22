import argparse
import configparser
import sys
import os
from pprint import pprint as pp


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

# Setup program and read operator settings
_logdir = '/usr/lib/ops_log/operator_logs/'
_aliasfile = '/etc/profile.d/opslog_alias.sh'
_configfile = '/usr/lib/ops_log/config.ini'


def get_operator():
    # print(os.getenv('OPS_LOG_USER'))
    config = configparser.ConfigParser()
    config.read(_configfile)

    return config.get("Operator Settings", "Current Operator")


def set_operator(value):

    config = configparser.ConfigParser()

    config.read(_configfile)
    config.set("Operator Settings", "Current Operator", value)

    with open(_configfile, 'w') as cfgfile:
        config.write(cfgfile)


def cat_log():
    """Display the current operators log and exit"""

    try:
        log = open(os.path.join(_logdir, get_operator())).read()
    except FileNotFoundError:
        print("No entries for current operator.")
        exit()

    return log


def list_flags():
    log = cat_log()

    # Creates a dictionary containing log entries and the flag used in that entry
    entries = {}
    i = int()
    for line in log.splitlines():
        i = i + 1
        entries[i] = line.split(';').__getitem__(2)

    # Creates a set which contains all the unique flags found in entries
    flags = set()
    entries2 = {key: list(map(str, value.split())) for key, value in entries.items()}
    for flaglist in entries2.values():
        for single_flags in flaglist:
            flags.add(single_flags)

    # Create some string variables to hold the final output
    data = str()
    header = str("""
    Below are the flags being used in the current log
    
        {: <10} {: <15} {: <}
        {: <10} {: <15} {: <}""".format("Count", "Flag", "Entries", "-----", "-----", "-------"))

    # For each unique flag, count how many times it appears, and find which lines it appears on
    # Then create a line of text with this information and add it to the output variable
    entrylist = []
    for flag in flags:
        count = sum(flag in value for value in entries2.values())
        entrylist.clear()
        for key in entries2.keys():
            if flag in entries2[key]:
                entrylist.append(key)
        data = "\n".join([data, "\t{: <10} {: <15} {: <}".format(str(count), flag, str(entrylist))])

    output = data.splitlines()
    output.sort(reverse=True)
    output = "\n".join(output)

    return header + "\n" + output


def search_log(flags):
    print('search through log for flag entries: ', flags)
    exit()


def _install_opslog():

    response = input("opslog has not yet been installed. Would you like to install now? (y/n)")

    if not response.lower().startswith("y"):
        print("Exiting")
        exit()

    print("Beginning Install...")
    if not os.path.isdir('/usr/lib/ops_log/'):
        try:
            os.mkdir('/usr/lib/ops_log/')
            os.chmod('/usr/lib/ops_log', 0o4777)  # this line must be changed to work with python 2.7 (04777)

            os.mkdir(_logdir)
            os.chmod(_logdir, 0o4777)  # this line must be changed to work with python 2.7 (04777)

            cfgfile = open("/usr/lib/ops_log/config.ini", 'w')
            input_operator = input("Enter operator name: ")
            config = configparser.ConfigParser()
            config.add_section('Operator Settings')
            config.set('Operator Settings', 'Current Operator', input_operator)
            config.write(cfgfile)

            cfgfile.close()

            os.chmod("/usr/lib/ops_log/config.ini", 0o666)  # this line must be changed to work with python 2.7 (644)

            create_alias = open(_aliasfile, '+a')
            create_alias.write("\nfunction opslog()\n{\npython ")
            create_alias.write(os.path.realpath(__file__))
            create_alias.write(r' "$@"')
            create_alias.write('\n}\nexport opslog')
            create_alias.close()
            
            print("""Program successfully installed to /usr/lib/ops_log/
            After restarting terminal, logs may now be created using shortcut command 'opslog'.
            
               Example: opslog -n 'operator note'
            
            """)

        except PermissionError:
            print("Install failed due to insufficient permissions.")
            print("  ->opslog must be installed as root or with sudo.")

    exit()


def read_configs():
    config = configparser.ConfigParser()
    config.read("/usr/lib/ops_log/config.ini")

    return config.items()


def main(args):
    """This function will handle the main logging"""
    print(args)
    return args


if __name__ == '__main__':

    if not os.path.isfile(_configfile):
        _install_opslog()

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

    print(list_flags()) if args.lf else print(get_operator()) if args.operator \
        else print(args.cat()) if args.cat else main(args)
