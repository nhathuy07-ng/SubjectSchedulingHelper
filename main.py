#!/usr/bin/python3

import re
import enum
import pickle
from pathlib import Path
import sys

class Actions(enum.Enum):
    LIST= 1
    EXIT= 2
    DELETE= 3

class Schedule:
    @classmethod
    def create_schedules(cls, frags: list[str]):
        """
        frags: [day, hhmmAM|PM-hhmmAM|PM, day, ...]
        """
        scheds: list[Schedule] = []
        for i in range(0, len(frags), 2):
            # date, time
            time_from, time_to = frags[i+1].split('-')
            mins_from = int(time_from[:2]) * 60 + int(time_from[2:4])
            mins_to = int(time_to[:2]) * 60 + int(time_to[2:4])

            if time_from.lower().endswith('pm') and time_from[:2] != '12':
                mins_from += (12 * 60)

            if time_to.lower().endswith('pm') and time_to[:2] != '12':
                mins_to += (12 * 60)

            scheds.append(Schedule(mins_from=mins_from, mins_to=mins_to, date=frags[i]))
        return scheds

    def __init__(self, mins_from, mins_to, date):
        self.mins_from = mins_from
        self.mins_to = mins_to
        self.date = date

    def __repr__(self):
        return f"{self.date} {self.mins_from//60}:{self.mins_from - (self.mins_from//60 * 60):02} - {self.mins_to//60}:{self.mins_to - (self.mins_to//60 * 60):02}"

class Course:
    def __init__(self, course_name: str, course_code: str, creds_count: str|int, schedule: list[Schedule]):
        self.course_name: str = course_name
        self.course_code: str = course_code
        self.schedule: list[Schedule] = schedule
        self.creds_count = int(creds_count)
    def __repr__(self):
        return f"[{self.creds_count} credits] {self.course_name}-{self.course_code} ({self.schedule})"

class Conflict:
    def __init__(self, course_1: Course, course_2: Course, schedule_1: Schedule, schedule_2: Schedule):
        self.course_1 = course_1
        self.course_2 = course_2
        self.schedule_1 = schedule_1
        self.schedule_2 = schedule_2

    def __repr__(self):
        return f"CONFLICT: {self.course_1.course_name}-{self.course_1.course_code} ({self.schedule_1}) vs {self.course_2.course_name}-{self.course_2.course_code} ({self.schedule_2})"
        

def validate_input(input_frags: list[str]):
    if input_frags.__len__() < 5:
        return False

    for i, f in enumerate(input_frags[3:], 0):
        if i % 2 == 0:
            if f.lower() not in ["mon", "tue", "wed", "thur", "fri", "sat", "sun"]:
                return False

        if i % 2 == 1:
            if not re.search(r"\d{4}am|pm|AM|PM\d{4}am|pm|AM|PM", f):
                return False
    return True


def map_function(func_str) -> Actions | None:

    if func_str.lower() == "list":
        return Actions.LIST

    if func_str.lower() == "exit":
        return Actions.EXIT

    if func_str.lower() == "delete":
        return Actions.DELETE

    return None

def poll_input():
    _raw = input("[course name] [course code] [creds count] [day hhmmAM|PM-hhmmAM|PM] ... ").split()

    if _raw.__len__() == 1:
        f = map_function(_raw[0])

        if f is None:
            pass
        else:
            return f

    if not validate_input(_raw):
        return None
    else:
        return Course(_raw[0], _raw[1], _raw[2], Schedule.create_schedules(_raw[3:]))

def check_overlap(new_course: Course, courses: list[Course]) -> Course | None:
    for course in courses:
        for schedule in course.schedule:
            # if schedule overlaps, return the overlapping subject
            for new_schedule in new_course.schedule:
                if (schedule.mins_to >= new_schedule.mins_from >= schedule.mins_from or schedule.mins_from <= new_schedule.mins_to <= schedule.mins_to) and schedule.date == new_schedule.date:
                    return Conflict(course, new_course, schedule, new_schedule)

    return None

def print_line_arrays(a: list[any]):
    for i, ia in enumerate(a, 0):
        print(f"{i}. {ia}")

def initialize_save():
    if not (Path(sys.argv[0]) / "saves").exists():
        (Path(sys.argv[0]).parent / "saves").mkdir(parents=True)

def new_file(name):
    pass

def main():

    print("\033[H\033[2J", end="")

    initialize_save()

    courses = []
    while True:
        out = poll_input()
        if out is None:
            print("invalid input")

        if isinstance(out, Course):
            conflict = check_overlap(out, courses)
            if not conflict:
                print("new course added:", out)
                courses.append(out)
            else:
                print(conflict)
        elif isinstance(out, Actions):
            if out == Actions.EXIT:
                print(courses)
                break

            if out == Actions.LIST:
                print_line_arrays(courses)

            if out == Actions.DELETE:
                print_line_arrays(courses)
                _del_id = input("delete #? ")
                print(f"Del'd {courses.pop(int(_del_id))}")


if __name__ == "__main__":
    main()
