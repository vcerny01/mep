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
    0: '',  # date
    1: '',  # time
    2: '',  # name
    3: '',  # place
    4: ''  # additional info
}

event_time = {
    0: 0,  # year
    1: 0,  # month
    2: 0  # day
}

date_time = {
    0: datetime.datetime.today().year,  # year
    1: datetime.datetime.today().month,  # month
    2: datetime.datetime.today().day  # day
}

date_date = datetime.datetime.today()
week_number =  int(date_date.strftime("%V"))

day_used = False
last_day = ' '

def print_help():
    print('Usage: mep [FILE] [TIMESPAN]')
    print('\tEnter \'mep help\' to print this menu')
    print('\t[FILE] - path to a file')
    print('\t[TIMESPAN] - options: ')
    print('\t\tall - all events')
    print('\t\tday [+-NUMBER] (optional) - all events for a day')
    print('\t\tweek [+-NUMBER] (optional) - all events for a week')
    print('\t\tmonth [+-NUMBER] (optional) - all events for a month')
    print('\t\tyear [+-NUMBER] (optional) - all events for a year')
    print('\t\tdate [YYYY-MM-DD] - all events for a day, input by date')



def time_to_dic(full_date, output: dict):
    # first clean the dictionary
    for attr in event_time:
        output[attr] = 0
    # get values
    indexer = 0
    for ch in full_date:
        # print(ch)
        if ch == '-':
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
    print_permit = False
    if timespan == "all":
        print_permit == True
    if timespan == "date" or "day":
        if date_time[0] == event_time[0] and date_time[1] == event_time[1] and date_time[2] == event_time[2]:
            print_permit = True
    if timespan == "week":
        if date_time[0] == event_time[0] and week_number == int(datetime.date(event_time[0], event_time[1], event_time[2]).strftime("%V")):
            print_permit = True
    if timespan == "month":
        if date_time[0] == event_time[0] and date_time[1] == event_time[1]:
            print_permit = True
    if timespan == "year":
        if date_time[0] == event_time[0]:
            print_permit = True
    return print_permit


def print_output(event):
    global day_used, last_day
    day = datetime.datetime(event_time[0], event_time[1], event_time[2])
    if day != last_day:
        day_used = False
    if day_used == False:
        print('\nOn', day.strftime('%A') + ',', (str(event_time[1]) + '/' + str(event_time[2]) + '/' + str(event_time[0])) + ':')
        day_used = True
    print('event:', event[2], '(' + event[3] + ')', 'at', event[1])
    print('\t'+ event[4])
    last_day = day


def parse_shift(arg, output):
    global date_date
    global week_number
    # parsing shift
    to_add = 0
    for char in arg:
        to_add *= 10
        try:
            if arg[0] == '-':
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
        print('hey')
        date_date += relativedelta(years=to_add)
    if output == "week_number":
        date_date += relativedelta(weeks=to_add)
        week_number = int(date_date.strftime("%V"))
    time_to_dic(str(date_date), date_time)


def parse_timespan():
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
    print('Invalid argument!')
    sys.exit()


def main():

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
        print('Enter a file name!')
        sys.exit()
    ## set timespan
    if len(sys.argv) > 2:
        timespan = parse_timespan()
    else:
        ch = input('Proceed to display all events? (y/n) ')
        timespan = "all"
        if ch != 'y':
            exit()
    # Open the file
    try:
        fp = open(filename, 'r')
    except FileNotFoundError:
        print('File does not exist!')
        sys.exit()
    # Read and print output
    while True:
        ch = fp.read(1)
        if ch == '':
            break
        # read event entry and output to event dict
        if ch == ';' and fp.read(1) == ';':
            # Initialize variables
            cuch = ''  # cuch stands for current char as ch is already taken in this scope
            data = ''
            event_attr = 0
            # read event parameters till the event end
            while True:
                cuch = fp.read(1)
                pos = fp.tell()
                tch = fp.read(1)
                if cuch == ';' and tch == ';':
                    event[event_attr] = data.strip()
                    time_to_dic(event[0], event_time)
                    print_permit = decide_print(timespan)
                    if print_permit:
                        print_output(event)
                    break
                fp.seek(pos)
                if cuch == '/':
                    if event_attr > 4:
                        break
                    event[event_attr] = data.strip()
                    data = ''
                    cuch = ''
                    event_attr += 1
                data += cuch


if __name__ == "__main__":
    main()
