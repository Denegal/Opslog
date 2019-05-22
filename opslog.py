import argparse
import configparser
import re
import datetime
import sys
import csv
import json
from shutil import copyfile
from shutil import copytree
import os
import subprocess
import pandas


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

  --export FILE         Export the current log
  --export-json FILE    Export the current log in json format
  --merge F1 F2 [F3...] Merge multiple log files together into one log



The man page can be accessed with the command 'man opslog'.

Complete documentation can be found in the /usr/lib/ops_log/html/index.html webfile

"""

# Setup program and read operator settings
_logdir = '/usr/lib/ops_log/operator_logs/'
_aliasfile = '/etc/profile.d/opslog_alias.sh'
_configfile = '/usr/lib/ops_log/config.ini'
pandas.set_option('display.expand_frame_repr', False)
pandas.set_option('display.colheader_justify', 'center')


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
    print("New operator set")
    exit()


def list_operators():
    print("Logs exist for the following operators:")
    operators = os.listdir(_logdir)
    for name in operators:
        print("\t" + re.split("_ops_log.csv", name)[0])
    exit()


def _get_log():

    try:

        log = pandas.read_csv(os.path.join(_logdir, get_operator() + "_ops_log.csv"), delimiter=';').fillna('')
        log.index += 1
    except FileNotFoundError:
        print("No log for current operator.")
        exit()
    return log


def display_log(log = _get_log()):
    left_justify = {"Flag": '{{:<{}s}}'.format(log['Flag'].str.len().max()).format,
                    "Command Syntax": '{{:<{}s}}'.format(log['Command Syntax'].str.len().max()).format,
                    "Note": '{{:<{}s}}'.format(log['Note'].str.len().max()).format}

    if not log.empty:
        return log.to_string(formatters=left_justify)
    else:
        print("\nThere are no entries in current log tagged with any of the provided flags.")
        print("Use 'opslog -lf' to list all currently used flags\n")
    exit()


def list_flags():
    log = _get_log()

    # Creates a set which contains all the unique flags found in entries
    # This is created using nested list comprehensions.
    # the first comprehension creates a list of flag entries, the second takes that
    # list and creates a list of all individual flags from those entries.
    # this is required because the first comprehension can create a list of lists
    # if multiple flags are used in a single entry.
    flags = set([flag2 for i in range(len([flag.split() for flag in log['Flag']]))
                 for flag2 in [flag.split() for flag in log['Flag']][i]])

    # Create some string variables to hold the final output
    data = str()
    output = list()
    header = str("""
    Below are the flags being used in the current log

        {: <10} {: <15} {: <}
        {: <10} {: <15} {: <}""".format("Count", "Flag", "Entries", "-----", "-----", "-------\n"))

    # For each unique flag, count how many times it appears, and find which lines it appears on
    # Then create a line of text with this information and add it to the output variable
    for flag in flags:
        count = len(log[[flag in entry.split() for entry in log['Flag']]])
        entrylist = list(log[[flag in entry.split() for entry in log['Flag']]].index)
        data = "\n".join([data, "\t{: <10} {: <15} {: <}".format(str(count), flag, str(entrylist))])

        output = data.splitlines()

    output.sort(reverse=True)
    output = "\n".join(output)

    return [header, output]


def search_log(flags):

    log = _get_log()

    entrylist = list()
    entryhit = bool()
    for entry in log['Flag']:
        for flag in flags:
            if flag in entry.split():
                entrylist.append(True)
                entryhit = True
                break
        if not entryhit:
            entrylist.append(False)
        entryhit = False

    return log[entrylist]


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
            copytree('install/help/', '/usr/lib/ops_log/help/')
            os.chmod("/usr/lib/ops_log/help/", 0o775)  # this line must be changed to work with python 2.7 (771)
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


def _export_log(location, style):

    if os.path.isfile(location):
        response = input(location + " already exists. Do you wish to overwrite? (y/n)")
        if not response.startswith('y'):
            print("Aborting export of log file")
            exit()

    try:
        if style == 'default' or style == 'd':
            with open(location, 'w+') as f:
                f.write(display_log())
                f.write("\n")
        elif style == 'csv':
            copyfile(_logdir + get_operator() + "_ops_log.csv", location)
        elif style == 'json':
            input_file = _logdir + get_operator() + "_ops_log.csv"
            output_file = location

            csv_rows = []
            with open(input_file) as csvfile:
                fields = ["Date", "Operator", "Flags", "PAA", "IP", "Command", "Executed", "Note"]
                reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=';')
                title = reader.fieldnames
                for row in reader:
                    csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])

                with open(output_file, "w") as f:
                    f.write(json.dumps(csv_rows, sort_keys=False, indent=4,
                                       separators=(';', ': ')))  # , encoding="utf-8", ensure_ascii=False))
        else:
            print("Export failed: unknown filetype {}".format(style))
            exit()

        print('Log file successfully exported')

    except IOError as e:
        print('export failed due to error: \n  ' + str(e))

    exit()


def _merge_logs(logs_list):
    print("Checking files...")

    # First check that each file provided is the correct format
    patern = re.compile("^.*;.+;.*;.*;.*;.*;.*;.*")
    for file in logs_list:
        with open(file, 'r') as log:
            for line in log.readlines():
                if not patern.match(line) and not line == "":
                    print("ERROR: file {} does not match logging format. Unable to merge".format(file))
                    exit()

    print("All files matches log format.")
    dest_file = input("Enter destination filename: ")
    output = str()
    for file in logs_list:
        with open(file, 'r') as log:
            output = output + str(log.read())
    result = sorted(output.splitlines())
    with open(dest_file, "+a") as newlog:
        newlog.writelines("\n".join(result))
        newlog.write("\n")
    print("Merge Successful")
    exit()


def _run_command(command):

    date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    retcode = subprocess.run(['/bin/bash', '-i', '-c', command], stderr=subprocess.PIPE)
    if retcode.returncode > 0:
        executed = 'no'
        cmd_error = re.split(".*: ", str(retcode.stderr).replace("b'", '')
                             .replace("\\n'", '').replace('\\n"', ''))[1]
        new_entry = str(date) + ';' + get_operator() + ';' + args.f + ';' + args.p + ';' + \
                    args.i + ';' + command + ';' + executed + ';' + args.n + " - ERROR: " + cmd_error

        log = open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'r')
        lines = log.readlines()
        log.close()

        newlog = open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'w')
        for item in lines[:-1]:
            newlog.writelines(item)
        newlog.writelines(new_entry + "\n")
        newlog.close()
        print("\n".join(cmd_error.split("\\n")))


def main(args):
    """This function will handle the main logging"""

    new_entry = str()

    # if no log exists, create one with proper header
    if not os.path.isfile(os.path.join(_logdir, get_operator() + "_ops_log.csv")):
        with open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'a+') as log:
            log.write('Date;Operator;Flag;PAA;IPs;Command Syntax;Executed;Note')
            log.write("\n")

    date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # make sure arguments are in proper format for logging
    args.f = '' if not args.f else ' '.join(args.f)
    args.p = '' if not args.p else str(args.p[0])
    args.i = '' if not args.i else ' '.join(args.i)
    command = ' '.join(args.c) if args.c else ' '.join(args.C) if args.C else ''
    executed = 'yes' if args.C else 'no' if args.c else ''
    args.n = '' if not args.n else args.n[0]

    # Create entry with all provided arguments
    new_entry = str(date) + ';' + get_operator() + ';' + args.f + ';' + args.p + ';' + \
               args.i + ';' + command + ';' + executed + ';' + args.n

    # Write new entry to log
    with open(os.path.join(_logdir, get_operator() + "_ops_log.csv"), 'a+') as log:
        log.write(new_entry)
        log.write("\n")

    # If -C was used, execute the command
    if args.C:
        _run_command(command)

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
        metavar='newoperator',
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
        const=display_log,
        help='Output the current log (can be piped to less/more, head/tail)'
    )
    display_group.add_argument(
        '-lf',
        action='store_const',
        const=list_flags(),
        help='List all flags used in current operators log'
    )
    display_group.add_argument(
        '-sf',
        metavar='Flag',
        nargs='+',
        type=str,
        help='Search the log entries for those tagged with Flag(s)'
    )
    mgmt_group = parser.add_argument_group()
    mgmt_group.description = "Use the following commands to manage operator logs"
    mgmt_group.add_argument(
        '--export',
        dest='filename',
        nargs=1,
        type=str,
        help='Export the current operator log to file'
    )
    mgmt_group.add_argument(
        '--format',
        dest='filetype',
        nargs=1,
        type=str,
        choices=['csv', 'json', 'default'],
        default='default',
        help='format to export the operator log in (csv, json, or default)'
    )
    mgmt_group.add_argument(
        '--merge',
        dest='mergefile',
        nargs='+',
        type=str,
        help='Merge multiple logs into one file'
    )

    if not len(sys.argv) > 1:
        print(_desc)
        exit()

    args = parser.parse_args()

    if args.sf:
        print(display_log(search_log(args.sf)))
        exit()
    if args.set_operator:
        set_operator(args.set_operator[0])
        exit()
    if args.filename:
        _export_log(args.filename[0], args.filetype[0])

    print(list_flags()[0], list_flags()[1]) if args.lf \
        else print(get_operator()) if args.operator \
        else print(args.list_operators()) if args.list_operators \
        else print(display_log()) if args.cat \
        else main(args)
