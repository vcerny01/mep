# IMPORT RELEVANT FUNCTIONS FROM mep.py !!!!

#
# Name: mepi
# Author: Vít Černý
# License: GPL v3
# Description: mepi offers an easy, scriptable way to add 'event expression' (see mep) to text files
#
# -*- coding: utf-8 -*-

import sys
import argparse
import datetime

default_event = {
    "date": datetime.datetime.today().strftime('%Y-%m-%d'),
    "time": "12:00",
    "name": "New Event",
    "place": "",
    "info": "",
    "kind": "event"
}
event = {
    "date": "",  # date
    "time": "",  # time
    "name": "",  # name
    "place": "",  # place
    "info": "",  # additional info
    "kind": "",  # type
}

char_types = {
    "event": "e",
    "reminder": "r",
    "deadline": "d"
}

def parse_args():
    """Parse and return command line arguments using argparse"""
    parser = argparse.ArgumentParser(description="Add event expressions to text files")
    parser.add_argument("-f", "--file", type=str, help="filename")
    parser.add_argument("-k", "--kind", type=str, help="expression type", choices=["event", "e", "deadline", "d", "reminder", "r"])
    parser.add_argument("-d", "--date", type=str, help="date in ISO (YYYY-MM-DD) format")
    parser.add_argument("-t", "--time", type=str, help="time of a day")
    parser.add_argument("-n", "--name", type=str, help="expression name")
    parser.add_argument("-p", "--place", type=str, help="place, e.g., an adress")
    parser.add_argument("-i", "--info", type=str, help="additional info")
    args = parser.parse_args()
    return args


def main():
    """ Main function """
    # populate the dict with values from argv
    args = parse_args()
    for arg in vars(args).items():
        if arg[1] is not None:
            event[arg[0]] = arg[1]

    # populate missing values
    if args.file is None:
        filename = input("file (default: events.md): ")
        if filename == "":
            filename = "events.md"
    else:
        filename = args.file
    for var in event.items():
        var = list([var[0], var[1]])
        if var[1] == "":
            print(var[0], "(default:", default_event[var[0]], ")",  ": ", end="")
            var[1] = input()
            if var[1] == "":
                var[1] = default_event[var[0]]
            event[var[0]] = var[1]
    # write event to the file
    try:
        fp = open(filename, "a+")
    except FileNotFoundError:
        print("File", "'" + filename + "'", "does not exist!")
        sys.exit()
    # prepare variables
    if event["kind"] not in ("event", "reminder", "deadline", "e", "d", "r"):
        print("Invalid expression type!!")
        sys.exit()

        ## TO DO CHECK FOR IF TIME IS ISO - IMPORTANT

    if event["kind"] in ("event", "reminder", "deadline"):
        event["kind"] = char_types[event["kind"]]

    print("Tests passed, writing...")
    # switch standard output and start printing
    sys.stdout = fp
    print(";;", "%" + event["kind"] + "%", event["date"], "/", event["time"], "/", event["name"], "/", event["place"], "/", event["info"], ";;")

    # switch back to the standard standard output :-))
    sys.stdout = sys.__stdout__
    print("Your event has succesfully been written: ")
    print(";;", "%" + event["kind"] + "%", event["date"], "/", event["time"], "/", event["name"], "/", event["place"], "/", event["info"], ";;")
if __name__ == "__main__":
    main()
