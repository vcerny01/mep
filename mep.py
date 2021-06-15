#
# Name: mep - markdown events with python
# Author: Vít Černý
# License: GPL v3
# Description: mep parses and filters particular 'event entries' from a markdown file
#
import sys
import datetime

event = {
	0 :'', # date
	1: '', # time
	2: '', # name
	3: '', # place
	4: ''  # additional info
}

event_time = {
	0: 0, # year
	1: 0, # month
	2: 0  # day
}


def print_Help():
	print('Usage: mep [FILE] [TIMESPAN]')

def getEvent_time(event):
	full_date = event[0]
	indexer = 0
	for ch in full_date:
		#print(ch)
		if (ch == '-'):
			indexer += 1
			if (indexer > 2):
				break;
			continue
		event_time[indexer] *= 10
		event_time[indexer] += int(ch)

def decide_Print(timespan):
	ct = datetime.datetime.now() # ct stands for current time
	print_permit = False
	if (timespan == "all"):
		print_permit = True
		return print_permit
	if (timespan == "today"):
		if (ct.year == event_time[0] and ct.month == event_time[1] and ct.day == event_time[2]):
			print_permit = True
			return print_permit
		else:
			return print_permit


def print_Output(event):
	print('Date: ', event[0], ' ', event[1])
	print('Name ', event[2])
	print('Place: ', event[3])
	print('Additional info: ', event[4])
	print('\n\n')

def main():
	# Read command-line args
	if (len(sys.argv) < 2):
		print_Help()
		exit()
	try:
		filename = sys.argv[1]
	except (IndexError):
		print('Enter a file name!')
		exit()
	if (len(sys.argv) > 2):
		timespan = sys.argv[2]
	else:
		ch = input('Proceed to display all events? (y/n) ')
		timespan = "all"
		if (ch != 'y'):
			exit()

	# Open the file
	try:
		fp = open(filename, 'r')
	except (FileNotFoundError):
		print('File does not exist!')
		exit()

	# Read and print output
	while(True):
		ch = fp.read(1)
		if (ch == ''):
			break
		# read event entry and output to event dict
		if (ch == ';'):
			# Initialize variables
			cuch = '' # cuch stands for current char as ch is already taken in this scope
			data = ''
			type = 0
			# read event parameters till the event end
			while(True):
				cuch = fp.read(1)
				if(cuch == ';'):
					event[type] = data.strip()
					getEvent_time(event)
					print_permit = decide_Print(timespan)
					if (print_permit == True):
						print_Output(event)
					break
				if (cuch == '/'):
					if (type > 4):
						break
					event[type] = data.strip()
					data = ''
					cuch = ''
					type += 1
				data += cuch

if __name__ == "__main__":
	main()
