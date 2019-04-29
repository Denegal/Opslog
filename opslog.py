import argparse
import configparser
import re
import datetime
import sys
from shutil import copyfile
from shutil import copytree
import os
import subprocess
from pprint import pprint as pp


def _setup():
    """This function will setup the program to use aliases, setup initial operator, and create missing folders/files"""
    print('Begin setup of operator and program')
    exit()


_desc = """
usage: opslog.py [-h | -v | -o | -lo | -so operator] [-p #] [-i a.b.c.d/f]
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



The man page can be accessed with the command 'man opslog'.

Complete documentation can be found in the /usr/lib/ops_log/html/index.html webfile

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


def list_operators():
    print("Logs exist for the following operators:")
    operators = os.listdir(_logdir)
    for name in operators:
        print("\t" + re.split("_ops_log.csv", name)[0])

    exit()


def cat_log():
    """Display the current operators log and exit"""

    try:
        log = open(os.path.join(_logdir, get_operator() + "_ops_log.csv")).read()
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
        {: <10} {: <15} {: <}""".format("Count", "Flag", "Entries", "-----", "-----", "-------\n"))

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

    return [header, output]


def search_log(flags):
    # get the current flags in use using the list_flags function
    current_flags = list_flags()[1]
    entries = str()

    # enumerate each line and check if any of the searched for flags appear on that line
    # if they do, add all the entry numbers to the entries variable
    for line in current_flags.splitlines():
        for flag in flags:
            if re.search(r'\b' + flag + r'\b', line):
                entries = entries + re.sub(r".*\[", "", line)

    # this for loop uses tuple unpacking to remove unneeded chars in the entries string
    for r in (("]", ''), (',', ''), (' ', '')):
        entries = entries.replace(*r)

    entries = set(entries)
    output = str()

    # enumerate each line and every line that appears in the set of results, add it to the output
    with open(os.path.join(_logdir, get_operator() + "_ops_log.csv")) as log:
        for i, line in enumerate(log):
            if entries.__contains__(str(i + 1)):
                output = output + line

    return output


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
            create_alias.write("/usr/lib/ops_log/opslog.py")
            create_alias.write(r' "$@"')
            create_alias.write('\n}\nexport opslog')
            create_alias.close()

            # Add man page to system
            copyfile('install/opslog.1', '/usr/share/man/man1/opslog.1')

            # Add html documentation to install folder
            copytree('install/html/', '/usr/lib/ops_log/html/')
            os.chmod("/usr/lib/ops_log/html/", 0o775)  # this line must be changed to work with python 2.7 (771)
            for root, dirs, files in os.walk("/usr/lib/ops_log/html/"):
                for momo in dirs:
                    os.chmod(os.path.join(root, momo), 0o775)  # this line must be changed to work with python 2.7 (771)
                for momo in files:
                    os.chmod(os.path.join(root, momo), 0o775)  # this line must be changed to work with python 2.7 (771)

            copyfile(os.getcwd() + "/opslog.py", "/usr/lib/ops_log/opslog.py")
            os.chmod("/usr/lib/ops_log/opslog.py", 0o774)  # this line must be changed to work with python 2.7 (771)

            print("""Program successfully installed to /usr/lib/ops_log/
            After restarting terminal, logs may now be created using shortcut command 'opslog'.
            
               Example: opslog -n 'operator note'
            
            """)

        except PermissionError:
            print("Install failed due to insufficient permissions.")
            print("  ->opslog must be installed as root or with sudo.")

    exit()


def _export_log(location):

    if os.path.isfile(location):
        response = input(location + " already exists. Do you wish to overwrite? (y/n)")
        if not response.startswith('y'):
            print("Aborting export of log file")
            exit()
    try:
        copyfile(_logdir + get_operator() + "_ops_log.csv", location)
        print('Log file successfully exported')
    except IOError as e:
        print('export failed due to error: \n  ' + str(e))
    exit()


def _cmd_failed(entry):

    log = open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'r')
    lines = log.readlines()
    log.close()

    newlog = open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'w')
    for item in lines[:-1]:
        newlog.writelines(item)
    newlog.writelines(entry + "\n")
    newlog.close()


def main(args):
    """This function will handle the main logging"""
    new_entry = str()
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # make sure arguments are in proper format for logging
    args.f = '' if not args.f else ' '.join(args.f)
    args.p = '' if not args.p else str(args.p[0])
    args.i = '' if not args.i else ' '.join(args.i)
    command = ' '.join(args.c) if args.c else ' '.join(args.C) if args.C else ''
    executed = 'yes' if args.C else 'no' if args.c else ''
    args.n = '' if not args.n else args.n[0]

    new_entry = str(date) + ';' + get_operator() + ';' + args.f + ';' + args.p + ';' + \
               args.i + ';' + command + ';' + executed + ';' + args.n

    with open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'a+') as log:
        log.write(new_entry)
        log.write("\n")

    if args.C:

        retcode = subprocess.run(['/bin/bash', '-i', '-c', command], stderr=subprocess.PIPE)
        if retcode.returncode > 0:
            executed = 'no'
            cmd_error = re.split(".*: ", str(retcode.stderr).replace("b'", '')
                                 .replace("\\n'", '').replace('\\n"', ''))[1]
            new_entry = str(date) + ';' + get_operator() + ';' + args.f + ';' + args.p + ';' + \
                        args.i + ';' + command + ';' + executed + ';' + args.n + " - ERROR: " + cmd_error

            _cmd_failed(new_entry)
            print("\n".join(cmd_error.split("\\n")))
            exit()


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
        version='%(prog)s version 1.0\n\nCreated by: \n  Jacob Coburn\n  834COS\\DOB\n  jacob.coburn.1@us.af.mil'
    )
    root_group.add_argument(
        '-o', '--operator',
        action='store_const',
        const=get_operator,
        help='Show the current operator'
    )
    root_group.add_argument(
        '-lo', '--list-operators',
        action='store_const',
        const=list_operators,
        help='List all known operators'
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
    mgmt_group = parser.add_mutually_exclusive_group()
    mgmt_group.description = "Use the following commands to manage operator logs"
    mgmt_group.add_argument(
        '--export',
        dest='filename',
        nargs=1,
        type=str,
        help='Export the current operator log to file'
    )

    if not len(sys.argv) > 1:
        print(_desc)
        exit()

    args = parser.parse_args()

    if args.sf:
        print(search_log(args.sf))
        exit()
    if args.set_operator:
        set_operator(args.set_operator[0])
        exit()
    if args.filename:
        _export_log(args.filename[0])
        exit()

    print(list_flags()[0], list_flags()[1]) if args.lf else print(get_operator()) if args.operator \
        else print(args.list_operators()) if args.list_operators else print("\n" + args.cat()) if args.cat else main(args)
