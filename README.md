# mep - markdown events with python

## Introduction

I organize a big part of my life in markdown. One thing I've been missing was a way to plan events in plain text. So I've created a special syntax for events, compatible with markdown, and `mep`, which is a basic parser for such events.

## Syntax

example:

`;; 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;`

Every event starts and ends with two semicolons (`;;`). Event parameters are separated by a slash (`/`).

Events can be inserted anywhere in a text file

Whitespace is significant both between event parameters and outside the event expression. For example, you can write:

```markdown
;;
2021-6-25 / 12:00 /
    Meeting with John Doe /
    3 Abbey Road /
    Bring the papers. Don't forget to call John beforehand.

;;
```

;; 2021-6-25 / 12:00 /

### Parameters:

1. Date (required) - a date must be in `YYYY-MM-DD` format
2. Time (optional) - a time in a day, e.g., `16:30`, no special format required as it doesn't affect sorting, in fact, you can write whatever you want, e.g., `4 p.m.` or `12:00 - 16:00`, still I'd recommend to be consistent
3. Event name (well, optional, but don't be weird) - name of the event, no special format required
4. Place (optional) - a place that has something to do with your event, no special format required
5. Additional information (optional) - Some additional information for the event, e.g., a short note or a link to an online meeting

you can write: `;; 2021-6-25 / Meeting with John Doe`

## `mep`

`mep` is a small command-line program. It parses and displays events based on user requirements.

example:

`mep file.md week +1`

prints all events in the next week.

from `mep`'s `help`:

``` text
Usage: mep [FILE] [TIMESPAN]
        Enter 'mep help' to print this menu
        [FILE] - path to a file
        [TIMESPAN] - options: 
                all - all events
                day [+-NUMBER] (optional) - all events for a day
                week [+-NUMBER] (optional) - all events for a week
                month [+-NUMBER] (optional) - all events for a month
                year [+-NUMBER] (optional) - all events for a year
                date [YYYY-MM-DD] - all events for a certain day, input by date
```

`[+-NUMBER]` is a shift relative to current day/week/month/year, can be both positive and relative. Doesn't need to be specified, defaults to 0 (current day/week/month/year)

Just test it out with a few events.

example:

these are the contents a markdown file named `test.md`:

``` markdown
# Events

## Meetings

Yet another meeting with John Doe.
;; 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;

```

this is a command for mep I used to get this event:

`mep test.md date 2021-6-25`

This is the output I got:

``` text
On Friday, 6/25/2021:
event: Meeting with John Doe (3 Abbey Road) at 12:00
        Bring the papers
```

## Export

TO DO

## installation

TO DO
