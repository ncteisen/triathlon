import sys
from athlete import Athlete
from time import Time
import common

data = sys.stdin.readlines()

# times are presented as 00:00:00
def _is_time(s):
    return s.count(":") == 2

def main():
    athletes = []

    # Parse the input from the text file. THIS MAY CHANGE FROM YEAR TO YEAR.
    for line in data:
        line = line.strip().split()
        bib = int(line[0])
        line.pop(0)
        # Take the first two names, sry three name fools.
        name = line[0] + " " + line[1]
        # Trim until the times (remove the team names).
        while not _is_time(line[0]):
            line.pop(0)

        a = Athlete()
        a.addData("start", Time.fromString(line[0]))
        a.addData("bib", bib)
        a.addData("name", name)
        a.addData("swim", Time.fromString(line[1]))
        a.addData("t1", Time.fromString(line[2]))
        a.addData("bike", Time.fromString(line[3]))
        a.addData("t2", Time.fromString(line[4]))
        a.addData("run", Time.fromString(line[5]))
        a.addData("elapsed", Time.fromString(line[6]))
        a.addData("gender", line[12])
        a.addData("age", int(line[10]))
        athletes.append(a)

    # Add in filters here. TODO: express this via command line.
    athletes = filter(lambda x: x.data["gender"] == "F", athletes)
    # athletes = filter(lambda x: x.data["start"] == Time(07, 00, 00), athletes)

    sort_aspects = sys.argv[1:]
    common.validateAspects(athletes[0], sort_aspects)

    # Sort by the summation of all aspects
    athletes = sorted(athletes, key=lambda x: x.getTotal(sort_aspects))

    relevant = ["NOAH EISEN", "SARAH KRULEWITZ", "JOSHUA MERLE"]
    common.printRelevantPeople(athletes, relevant, sort_aspects)

if __name__ == "__main__":
    main()
