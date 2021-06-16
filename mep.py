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


def print_help():
    print('Usage: mep [FILE] [TIMESPAN]')


def get_event_time(event: dict):
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


def decide_print(timespan):
    ct = datetime.datetime.now()  # ct stands for current time
    print_permit = False
    if timespan == "all":
        print_permit = True
        return print_permit
    if timespan == "today":
        if ct.year == event_time[0] and ct.month == event_time[1] and ct.day == event_time[2]:
            print_permit = True
        return print_permit


def print_output(event):
    day = datetime.datetime(event_time[0], event_time[1], event_time[2])
    print('On', day.strftime('%A') + ',', (str(event_time[1]) + '/' + str(event_time[2]) + '/' + str(event_time[0])) + ',', 'at', event[1] + ':')
    print('\t'+ event[2], '(' + event[3] + ')')
    print('\t'+ event[4], '\n')

def main():
    # Read command-line args
    if len(sys.argv) < 2:
        print_help()
        exit()
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Enter a file name!')
        exit()
    if len(sys.argv) > 2:
        timespan = sys.argv[2]
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
                if cuch == ';':
                    event[event_attr] = data.strip()
                    get_event_time(event)
                    print_permit = decide_print(timespan)
                    if print_permit:
                        print_output(event)
                    break
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
