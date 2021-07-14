# mep

#### Table of Contents

- [Introduction](#introduction)
- [Syntax](#Syntax)
  - [Parameters](#parameters)
- [mep](#mep)
  - [export](#export)
- [mepi](#mepi)
- [Installation](#installation)


## Introduction

I organize a big part of my life in markdown. One thing I've been missing was a way to plan events, set reminders and deadlines,... in markdown (plain text). So I've created a special syntax for these things, compatible with markdown, `mep`, which is a basic parser for the resulting expressions, and `mepi`, which offers an easier way to add expressions to text files.

## Syntax

example:

`;; %e% 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;`

Every expression starts and ends with two semicolons (`;;`). Parameters are separated by a slash (`/`).

Events can be anywhere in a text file.

Whitespace is insignificant both between parameters and outside the expression. For example, you can write:

```markdown
;; %e%
  2021-6-25 / 12:00 /
  Meeting with John Doe /
3 Abbey Road /
Bring the papers. Don't forget to call John beforehand.

;;
```

### Parameters:

0. Type (optional) - a type specifier, currently supported types are `e` for events, `r` for reminders, `d` for deadlines. Put it anywhere inside the expression (I recommend to put it at the beginning) in format `%[TYPE]%`. Defaults to `e` for events
1. Date (required) - the date must be in ISO format
2. Time (optional) - time of day, e.g., `16:30`, no special format required as it doesn't affect sorting, in fact, you can write whatever you want, e.g., `4 p.m.` or `12:00 - 16:00`, still I'd recommend to be consistent. If you time blank it will be parsed by mep as "all day"
3. Event name (well, optional) - name of the event, no special format required
4. Place (optional) - a place that has something to do with your event, no special format required
5. Additional information (optional) - Some additional information for the event, e.g., a short note or a link to an online meeting

You can write `;; %e% 2021-6-25 / 12:00 / Meeting with John Doe ;;` and omit other parameters. You can also write: `;; 2021-6-25 / / Meeting with John Doe / / Bring the papers. ;;`

## `mep`

`mep` is a small command-line program. It parses and displays (exports) events based on user requirements.

example:

`mep file.md month +1 deadlines` - prints all deadlines in the next month.

From `mep`'s `help`:

```text
Usage: mep [FILE] [TIMESPAN] [TYPE] [{export}]
        Enter 'mep help' to print this menu
        [FILE] - path to a file
        [TIMESPAN] (optional, defaults to all) - options:
                all
                day [+-NUMBER] (optional, defaults to 0) - everything for a day
                week [+-NUMBER] (optional, defaults to 0) - everything for a week
                month [+-NUMBER] (optional, defaults to 0) - everything for a month
                year [+-NUMBER] (optional, default to 0) - everything for a year
                date [YYYY-MM-DD] - everything for a day, input by date
        [TYPE] (optional, defaults to all) - options:
                all - all types
                event - only events
                deadline - only deadlines
                reminder - only reminders
        export - just add 'export' to the end and the output is going to be exported to JSON
                example: mep events.md all deadlines export - will export all deadlines from the file
example:
        mep events.md week +1 deadlines (shows all deadlines for the next week)

```

`[+-NUMBER]` is a shift relative to the current day/week/month/year, it can be both positive and negative. It doesn't need to be specified, defaults to 0.

example:

This is text in file `test.md`:

```markdown
# Events

## Meetings

Yet another meeting with John Doe. See that because I didn't include any type specifier, the parser set it to event.
;; 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;
```

This is the command I used to get all expressions for 6/25/2021 (you can omit the 'all' parameter here):

`mep test.md date 2021-6-25 all`

This is the output I got:

```text
On Friday, 6/25/2021:
event: Meeting with John Doe (3 Abbey Road)
        12:00
        Bring the papers
```

### Export

`mep` can export to JSON. Just add `export` as the last argument, e.g., `mep event.md week +1 export` exports everything in the next week to JSON.

This is an event exported to JSON:

```json
{
  "id": 0,
  "type": "event",
  "name": "My Event",
  "date": "2021-6-20",
  "time": "9:00",
  "place": "Some Place",
  "additional information": "Some additional information"
}
```

## `mepi`

`mepi` offers an easy, scriptable way to write text expressions to text files.

Useful for when you want to add an expressions fast or you want to create a cronjob, e.g.,for creating a birthday event every year. `mepi`` uses argparse for parsing command-line arguments.

From `mepi`'s help:

``` text
usage: mepi.py [-h] [-f FILE] [-k {event,e,deadline,d,reminder,r}] [-d DATE] [-t TIME] [-n NAME] [-p PLACE] [-i INFO]

Write mep expressions to text files

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  filename
  -k {event,e,deadline,d,reminder,r}, --kind {event,e,deadline,d,reminder,r}
                        expression type
  -d DATE, --date DATE  date in ISO (YYYY-MM-DD) format
  -t TIME, --time TIME  time of a day
  -n NAME, --name NAME  expression name
  -p PLACE, --place PLACE
                        place, e.g., an adress
  -i INFO, --info INFO  additional info

```

All command-line arguments are optional, so for each argument you omit, `mepi` will ask you to input. You can basically just call `mepi` with no arguments.

You can also set your defaults for `mepi`. Just go to the code and edit the `default_event` dict.

## Installation

TO DO
