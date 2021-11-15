import sys
from tri.athlete import Athlete
from tri.time import Time
from tri.common import *

_MORRO_BAY = "morro_bay"
_OAKLAND = "oakland"
_HALF_MOON_BAY = "half_moon_bay"
_SANTA_CRUZ = "santa_cruz"

def get_tri(tri):
    if tri == "morro" or tri == "mb" or tri == "morro_bay":
        return _MORRO_BAY
    if tri == "sc" or tri == "santa_cruz":
        return _SANTA_CRUZ
    if tri == "oak" or tri == "oakland":
        return _OAKLAND
    if tri == "half_moon_bay" or tri == "hmb":
        return _HALF_MOON_BAY

    print("Unknown tri: '%s'" % tri)
    raise SystemExit(1)


def get_data(tri):
    if tri == _MORRO_BAY:
        with open('tri/data/mb2021-oly-data.txt') as f:
            return f.readlines()
    if tri == _OAKLAND:
        with open('tri/data/oak2019-oly-data.txt') as f:
            return f.readlines()
    if tri == _HALF_MOON_BAY:
        with open('tri/data/hmb2019-oly-data.txt') as f:
            return f.readlines()
    if tri == _SANTA_CRUZ:
        with open('tri/data/sc2018-sp-data.txt') as f:
            return f.readlines()

def add_bib_and_name(a, line):
    bib = int(line[0])
    line.pop(0)
    # Take the first two names, sry three name fools.
    name = line[0] + " " + line[1]

    a.addData("bib", bib)
    a.addData("name", name)

def trim_team_names(a, line):
    # Trim until we hit the first times (remove the team names).
    while not _is_time(line[0]):
        line.pop(0)

def add_main_data(a, line):
    a.addData("start", Time.fromString(line[0]))
    a.addData("swim", Time.fromString(line[1]))
    a.addData("t1", Time.fromString(line[2]))
    a.addData("bike", Time.fromString(line[3]))
    a.addData("t2", Time.fromString(line[4]))
    a.addData("run", Time.fromString(line[5]))
    a.addData("elapsed", Time.fromString(line[6]))

def parse_common_data(a, line):
    add_bib_and_name(a, line)
    trim_team_names(a, line)
    add_main_data(a, line)


def parse_line_morro(line):
    # pop off the place, we don't care about that
    place = int(line[0])
    line.pop(0)

    a = Athlete()
    parse_common_data(a, line)
    a.addData("gender", line[7])
    a.addData("age", int(line[9]))
    return a

def parse_line_oak_hmb(line):
    a = Athlete()
    parse_common_data(a, line)
    a.addData("gender", line[12])
    a.addData("age", int(line[10]))
    return a

# can't share with parse_line_oak_hmb because age
# and gender flipped
def parse_line_santa_cruz(line):
    a = Athlete()
    parse_common_data(a, line)
    a.addData("gender", line[10])
    a.addData("age", int(line[12]))
    return a

def parse_line(tri, line):
    if tri == _MORRO_BAY:
        return parse_line_morro(line)
    if tri == _OAKLAND:
        return parse_line_oak_hmb(line)
    if tri == _HALF_MOON_BAY:
        return parse_line_oak_hmb(line)
    if tri == _SANTA_CRUZ:
        return parse_line_santa_cruz(line)


# times are presented as 00:00:00
def _is_time(s):
    return s.count(":") == 2

def main():

    tri = get_tri(sys.argv[1])

    data = get_data(tri)

    athletes = []

    # Parse the input from the text file. THIS MAY CHANGE FROM YEAR TO YEAR.
    for line in data:
        line = line.strip().split()
        if ('DNS' in line or 'DNF' in line or '00:00:00' in line):
            continue
        a = parse_line(tri, line)
        athletes.append(a)

    # Add in filters here. TODO: express this via command line.
    # athletes = list(filter(lambda x: x.data["gender"] == "F", athletes))
    # athletes = filter(lambda x: x.data["gender"] == "F" 
    #         and x.data["age"] >= 20 
    #         and x.data["age"] <= 24, 
    #     athletes)
    # athletes = filter(lambda x: x.data["start"] == Time(07, 00, 00), athletes)

    num_athletes = len(athletes)

    sort_aspects = sys.argv[2:]
    validateAspects(athletes[0], sort_aspects)

    # Sort by the summation of all aspects
    athletes = sorted(athletes, key=lambda x: x.getTotal(sort_aspects))

    relevant = ["NOAH EISEN", "SARAH KRULEWITZ", "JOSHUA MERLE", "JACKSON JESSUP", "CAELA SHAY"]
    printRelevantPeople(athletes, relevant, sort_aspects, num_athletes)

if __name__ == "__main__":
    main()
