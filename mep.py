# TO DO
## - test heavily
## - write a README and a test file
## - create an export option, something that would export the events to JSON or iCal eventually
#
# Name: mep - markdown events with python
# Author: Vít Černý
# License: GPL v3
# Description: mep parses and filters particular 'event entries' from a markdown file
#
# -*- coding: utf-8 -*-
import sys
import datetime
from dateutil.relativedelta import relativedelta

event = {
    0: "",  # date
    1: "",  # time
    2: "",  # name
    3: "",  # place
    4: "",  # additional info
    5: "e",  # type
}

event_time = {0: 0, 1: 0, 2: 0}  # year  # month  # day

date_time = {
    0: datetime.datetime.today().year,  # year
    1: datetime.datetime.today().month,  # month
    2: datetime.datetime.today().day,  # day
}

event_type = {"e": "event", "d": "deadline", "r": "reminder"}

# pylint: disable=invalid-name
approved_type = "all"
date_date = datetime.datetime.today()
week_number = int(date_date.strftime("%V"))

# pylint: disable=invalid-name
day_used = False
last_day = " "


def print_help():
    """prints help"""
    print("Usage: mep [FILE] [TIMESPAN] [TYPE]")
    print("\tEnter 'mep help' to print this menu")
    print("\t[FILE] - path to a file")
    print("\t[TIMESPAN] (optional, defaults to all) - options: ")
    print("\t\tall")
    print("\t\tday [+-NUMBER] (optional, defaults to 0) - everything for a day")
    print("\t\tweek [+-NUMBER] (optional, defaults to 0) - everything for a week")
    print("\t\tmonth [+-NUMBER] (optional, defaults to 0) - everything for a month")
    print("\t\tyear [+-NUMBER] (optional, default to 0) - everything for a year")
    print("\t\tdate [YYYY-MM-DD] - everything for a day, input by date")
    print("\t[TYPE] (optional, defaults to all) - options")
    print("\t\tall - all types")
    print("\t\tevents - only events")
    print("\t\tdeadlines - only deadlines")
    print("\t\treminders - only reminders")
    print(
        "example:\n\tmep events.md week +1 deadlines (shows all deadlines for the next week)\n"
    )


def time_to_dic(full_date, output: dict):
    """outputs date to a dict of a certain format"""
    # first clean the dictionary
    for attr in event_time:
        output[attr] = 0
    # get values
    indexer = 0
    for ch in full_date:
        # print(ch)
        if ch == "-":
            indexer += 1
            if indexer > 2:
                break
            continue
        if indexer > 1:
            try:
                int(ch)
            except ValueError:
                break
        output[indexer] *= 10
        output[indexer] += int(ch)


def decide_print(timespan):
    """decides whether a currently parsed event should be printed according to timespan"""
    print_permit = False
    if approved_type not in ("all", event[5]):
        return print_permit
    if timespan == "all":
        print_permit = True
    if timespan in ("date", "day"):
        if (
            date_time[0] == event_time[0]
            and date_time[1] == event_time[1]
            and date_time[2] == event_time[2]
        ):
            print_permit = True
    if timespan == "week":
        if date_time[0] == event_time[0] and week_number == int(
            datetime.date(event_time[0], event_time[1], event_time[2]).strftime("%V")
        ):
            print_permit = True
    if timespan == "month":
        if date_time[0] == event_time[0] and date_time[1] == event_time[1]:
            print_permit = True
    if timespan == "year":
        if date_time[0] == event_time[0]:
            print_permit = True
    return print_permit


# I don't wanna pollute main, so I'm using global variables, it's also more tidy imo
# pylint: disable=global-statement, invalid-name
def print_output(certain_event):
    """prints output as requiered by user"""
    global day_used, last_day

    day = datetime.datetime(event_time[0], event_time[1], event_time[2])
    if day != last_day:
        day_used = False
    if day_used is False:
        print(
            "\nOn",
            day.strftime("%A") + ",",
            (str(event_time[1]) + "/" + str(event_time[2]) + "/" + str(event_time[0]))
            + ":",
        )
        day_used = True

    print(
        event_type[event[5]] + ":",
        certain_event[2],
        "(" + certain_event[3] + ")",
        "at",
        certain_event[1],
    )
    print("\t" + certain_event[4])
    last_day = day


# pylint: disable=global-statement, invalid-name
def parse_shift(arg, output):
    """parses relative shift of timespan as defined in args"""
    global date_date
    global week_number
    # parsing shift
    to_add = 0
    for char in arg:
        to_add *= 10
        try:
            if arg[0] == "-":
                to_add -= int(char)
            else:
                to_add += int(char)
        except ValueError:
            continue
    # outputing shift
    if output == 2:
        date_date += relativedelta(days=to_add)
    if output == 1:
        date_date += relativedelta(months=to_add)
    if output == 0:
        date_date += relativedelta(years=to_add)
    if output == "week_number":
        date_date += relativedelta(weeks=to_add)
        week_number = int(date_date.strftime("%V"))
    time_to_dic(str(date_date), date_time)


def parse_timespan():
    """parses timespan args and outputs to dicts"""
    timespan = sys.argv[2]
    argv_len = len(sys.argv)

    if timespan == "date":
        try:
            time_to_dic(sys.argv[3], date_time)
        except IndexError:
            print("Argument missing for date!")
            sys.exit()
        return timespan
    if timespan == "day":
        if argv_len > 3:
            parse_shift(sys.argv[3], 2)
        return timespan
    if timespan == "week":
        if argv_len > 3:
            parse_shift(sys.argv[3], "week_number")
        return timespan
    if timespan == "month":
        if argv_len > 3:
            parse_shift(sys.argv[3], 1)
        return timespan
    if timespan == "year":
        if argv_len > 3:
            parse_shift(sys.argv[3], 0)
        return timespan
    if timespan == "all":
        return timespan
    print("Invalid argument!")
    sys.exit()


def set_approved_type(string):
    """Sets approved type"""
    global approved_type
    if string == "events":
        approved_type = "e"
    elif string == "deadlines":
        approved_type = "d"
    elif string == "reminders":
        approved_type = "r"
    else:
        print("Unrecognized type!")
        sys.exit()


# pylint: disable=too-many-statements,too-many-branches, invalid-name
def main():
    """ Main function, where it all gets done, used to from C, more tidy imo """
    # Read command-line args
    ## help
    if len(sys.argv) < 2:
        print_help()
        sys.exit()
    if sys.argv[1] == "help":
        print_help()
        sys.exit()
    ## filename
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Enter a file name!")
        sys.exit()
    ## set timespan
    if len(sys.argv) > 2:
        timespan = parse_timespan()
    else:
        ch = input("Proceed to display all events? (y/n) ")
        timespan = "all"
        if ch != "y":
            sys.exit()
    try:
        set_approved_type(sys.argv[4])
    except IndexError:
        if sys.argv[3][0] not in ("+", "-", "0"):
            set_approved_type(sys.argv[3])
    # Open the file
    # pylint: disable=consider-using-with
    try:
        fp = open(filename, "r")
    except FileNotFoundError:
        print("File does not exist!")
        sys.exit()
    # Read and print output
    while True:
        ch = fp.read(1)
        if ch == "":
            break
        # read event entry and output to event dict
        if ch == ";" and fp.read(1) == ";":
            # Initialize some variables now
            data = ""
            type_read = False
            event_attr = 0
            # read event parameters till the event end

            while True:
                # cuch stands for current char as ch is already taken in this scop
                cuch = fp.read(1)
                pos = fp.tell()
                tch = fp.read(1)

                if cuch == "":
                    break
                if type_read is False and tch == "%":
                    tstring = tch
                    while len(tstring) < 4:
                        tchar = fp.read(1)
                        tstring += tchar
                    if tstring[2] != "%" or tstring[1] not in ("e", "d", "r"):
                        data += tstring
                    else:
                        type_read = True
                        event[5] = tstring[1]
                        pos = fp.tell()

                if cuch == ";" and tch == ";":
                    event[event_attr] = data.strip()
                    time_to_dic(event[0], event_time)
                    print_permit = decide_print(timespan)
                    if print_permit:
                        print_output(event)
                    event[5] = "e"
                    break

                fp.seek(pos)

                if cuch == "/":
                    if event_attr > 4:
                        break
                    event[event_attr] = data.strip()
                    data = ""
                    cuch = ""
                    event_attr += 1

                data += cuch


if __name__ == "__main__":
    main()
