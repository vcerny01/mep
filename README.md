# mep - markdown events with python

Not fully developed, yet!

#### Table of Contents

TO DO

## Introduction

I organize a big part of my life in markdown. One thing I've been missing was a way to plan events in plain text. So I've created a special syntax for events, compatible with markdown, and `mep`, which is a basic parser for such events.

## Syntax

example:

`;; %e% 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;`

Every event starts and ends with two semicolons (`;;`). Event parameters are separated by a slash (`/`).

Events can be inserted anywhere in a text file

Whitespace is significant both between event parameters and outside the event expression. For example, you can write:

```markdown
;; %e%
2021-6-25 / 12:00 /
    Meeting with John Doe /
    3 Abbey Road /
    Bring the papers. Don't forget to call John beforehand.

;;
```

### Parameters:

0. Type (optional) - a type specifier, currently supported are `e` for events, `r` for reminders, `d` for deadlines. Put it anywhere inside the expression (I recommend to put it at the beginning) in format `%[TYPE]%`. Defaults to `e` for events
1. Date (required) - a date must be in `YYYY-MM-DD` format
2. Time (optional) - a time in a day, e.g., `16:30`, no special format required as it doesn't affect sorting, in fact, you can write whatever you want, e.g., `4 p.m.` or `12:00 - 16:00`, still I'd recommend to be consistent
3. Event name (well, optional, but don't be weird) - name of the event, no special format required
4. Place (optional) - a place that has something to do with your event, no special format required
5. Additional information (optional) - Some additional information for the event, e.g., a short note or a link to an online meeting

You can write `;; %e% 2021-6-25 / 12:00 / Meeting with John Doe ;;` and omit other parameters. You can also write: `;; 2021-6-25 / / Meeting with John Doe / / Bring the papers. ;;`

## `mep`

`mep` is a small command-line program. It parses and displays events based on user requirements.

example:

`mep file.md month +1 deadlines` - prints all deadlines in the next month.

From `mep`'s `help`:

```text
Usage: mep [FILE] [TIMESPAN] [TYPE]
        Enter 'mep help' to print this menu
        [FILE] - path to a file
        [TIMESPAN] (optional, defaults to all) - options:
                all
                day [+-NUMBER] (optional, defaults to 0) - everything for a day
                week [+-NUMBER] (optional, defaults to 0) - everything for a week
                month [+-NUMBER] (optional, defaults to 0) - everything for a month
                year [+-NUMBER] (optional, default to 0) - everything for a year
                date [YYYY-MM-DD] - everything for a day, input by date
        [TYPE] (optional, defaults to all) - options
                all - all types
                events - only events
                deadlines - only deadlines
                reminders - only reminders
example:
        mep events.md week +1 deadlines (shows all deadlines for the next week)

```

`[+-NUMBER]` is a shift relative to current day/week/month/year, can be both positive and relative. Doesn't need to be specified, defaults to 0. (current day/week/month/year)

Just test it out.

example:

These are contents of a markdown file named `test.md`:

```markdown
# Events

## Meetings

Yet another meeting with John Doe. See that because I didn't include any type specifier, the parser set it to event.
;; 2021-6-25 / 12:00 / Meeting with John Doe / 3 Abbey Road / Bring the papers ;;
```

This is a command I used to get this event:

`mep test.md date 2021-6-25`

This is the output I got:

```text
On Friday, 6/25/2021:
event: Meeting with John Doe (3 Abbey Road) at 12:00
        Bring the papers
```

## Export

TO DO

## Installation

TO DO
