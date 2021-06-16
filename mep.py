# TO DO
## - redo TIME SPAN to be more customizable
##    - that will mean deleting ct and getting and implemanting date_time at all circumstances as the ultimate variable for setting the desired date
##    - the goal is that a user can customize exactly his desired date
##    - might not eventually do it as a person that knows shell scripting doesn't really need these
##    - another option is implementing this extra functionality in a shell script, which would be easier as far as I'm concerned.
## - month option
## - year option
##
#
# Name: mep - markdown events with python
# Author: Vít Černý
# License: GPL v3
# Description: mep parses and filters particular 'event entries' from a markdown file
#
# -*- coding: utf-8 -*-
import sys
import datetime

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
    0: 0,  # year
    1: 0,  # month
    2: 0  # day
}

week_number =  int(datetime.datetime.now().strftime("%V"))

def print_help():
    print('Usage: mep [FILE] [TIME SPAN]')
    print('\tEnter \'mep help\' to print this menu')
    print('\t[FILE] - path to a file')
    print('\t[TIME SPAN] - options: ')
    print('\t\tall - all events')
    print('\t\ttoday - all events for today')
    print('\t\ttomorrow - all events for tomorrow')
    print('\t\tweek [+-NUMBER] (optional, works only within current year) - all events for a certain week')
    print('\t\tmonth [+-NUMBER] (optional, works only within current year) - all events for a certain month')
    print('\t\tdate [YYYY-MM-DD] - all events for a day')



def time_to_dic(event: dict):
    # first clean the dictionary
    for attr in event_time:
        event_time[attr] = 0
    # get values
    full_date = event[0]
    indexer = 0
    for ch in full_date:
        # print(ch)
        if ch == '-':
            indexer += 1
            if indexer > 2:
                break
            continue
        event_time[indexer] *= 10
        event_time[indexer] += int(ch)


def date_to_dic(certain_date):
    indexer = 0
    for ch in certain_date:
        # print(ch)
        if ch == '-':
            indexer += 1
            if indexer > 2:
                break
            continue
        date_time[indexer] *= 10
        date_time[indexer] += int(ch)



def decide_print(timespan):
    print_permit = False
    if timespan == "date":
        if date_time[0] == event_time[0] and date_time[1] == event_time[1] and date_time[2] == event_time[2]:
            print_permit = True
            return print_permit
    ct = datetime.datetime.now()  # ct stands for current time
    if timespan == "all":
        print_permit = True
    if timespan == "today":
        if ct.year == event_time[0] and ct.month == event_time[1] and ct.day == event_time[2]:
            print_permit = True
    if timespan == "tomorrow":
        if ct.year == event_time[0] and ct.month == event_time[1] and ct.day+1 == event_time[2]:
            print_permit = True
    if timespan == "week":
        if week_number == int(datetime.date(event_time[0], event_time[1], event_time[2]).strftime("%V")):
            print_permit = True
    return print_permit


def print_output(event):
    day = datetime.datetime(event_time[0], event_time[1], event_time[2])
    print('On', day.strftime('%A') + ',', (str(event_time[1]) + '/' + str(event_time[2]) + '/' + str(event_time[0])) + ',', 'at', event[1] + ':')
    print('\t'+ event[2], '(' + event[3] + ')')
    print('\t'+ event[4], '\n')

def main():
    # Read command-line args
    ## help
    if len(sys.argv) < 2:
        print_help()
        exit()
    if sys.argv[1] == "help":
        print_help()
        exit()
    ## filename
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Enter a file name!')
        exit()
    ## timespan
    if len(sys.argv) > 2:
        timespan = sys.argv[2]
    else:
        ch = input('Proceed to display all events? (y/n) ')
        timespan = "all"
        if ch != 'y':
            exit()
    ### date
    if timespan == "date":
        try:
            certain_date = sys.argv[3]
        except IndexError:
            print("Argument missing for date!")
            exit()
        date_to_dic(certain_date)
    ### week
    if timespan == "week" and len(sys.argv) > 3:
        global week_number
        add_to_week = 0
        for char in sys.argv[3]:
            add_to_week *= 10
            try:
                if sys.argv[3][0] == '-':
                    add_to_week -= int(char)
                else:
                    add_to_week += int(char)
            except ValueError:
                continue
        week_number += add_to_week
    # Open the file
    try:
        fp = open(filename, 'r')
    except FileNotFoundError:
        print('File does not exist!')
        exit()

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
                    time_to_dic(event)
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
