from functools import total_ordering

def _fmt_num(n):
    return "0" + str(n) if n < 10 else str(n)

# Simple time class that supports addition and ordering.
@total_ordering
class Time:

    # Constructor
    def __init__(self, h, m, s):
        self.hours = h
        self.mins = m
        self.secs = s

    # Alternative ctor from string
    @classmethod
    def fromString(cls, s):
        s = list(map(int, s.strip().split(":")))
        return cls(s[0], s[1], s[2])

    # Addition overload
    def __add__(self, other):
        ts = ((self.secs + other.secs) + (60 * (self.mins + other.mins)) +
              (3600 * (self.hours + other.hours)))
        h = ts // 3600
        ts -= h * 3600
        m = ts // 60
        ts -= m * 60
        assert (ts < 60)
        n = Time(h, m, ts)
        return Time(h, m, ts)

    # Needed to support total ordering
    def __eq__(self, other):
        return (self.hours == other.hours and self.mins == other.mins and
                self.secs == other.secs)

    def __ne__(self, other):
        return not (self == other)

    # Needed to support total ordering
    def __lt__(self, other):
        if self.hours < other.hours:
            return True
        elif self.hours > other.hours:
            return False
        else:
            if self.mins < other.mins:
                return True
            elif self.mins > other.mins:
                return False
            else:
                if self.secs < other.secs:
                    return True
                else:
                    return False

    def __repr__(self):
        return _fmt_num(self.hours) + ":" + _fmt_num(
            self.mins) + ":" + _fmt_num(self.secs)