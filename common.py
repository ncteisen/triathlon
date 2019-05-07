from athlete import Athlete
import tabulate
import time

# Ensures that given aspects are present, and times.
def validateAspects(golden, aspects):
    for a in aspects:
        if a not in golden.data:
            print "Aspect '%s' not present in Athletes" % a
            raise SystemExit(1)
        if not isinstance(golden.data[a], time.Time):
            print "Aspect '%s' is not a time" % a
            raise SystemExit(1)

# Only prints out the people we care about.
def printRelevantPeople(athletes, relevant, aspects):
    is_multi_aspect = len(aspects) > 1
    headers = ["Rank", "Name"]
    if is_multi_aspect:
        headers += ["Total"]
    headers += aspects
    table = []
    for i, a in enumerate(athletes):
        if a.data["name"] in relevant:
            row = [i + 1, a.data["name"]]
            if is_multi_aspect:
                row += [str(a.getTotal(aspects))]
            row += [str(a.data[ass]) for ass in aspects]
            table += [row]
    print tabulate.tabulate(table, headers=headers)