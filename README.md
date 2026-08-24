# SubjectSchedulingHelper
A simple TUI tool for course-planning and checking course schedule conflicts.

---

## How to run?
- Install Python 3.10 or later if you haven't installed.
- Run `python3 main.py`. That's it!

## Commands
- `[course name] [course code] [creds count] [day hhmmAM|PM-hhmmAM|PM]...`: check a new course against existing ones for conflicts, then add if no conflict occurs.
- `list`: list the current courses
- `exit`: exit the program
- `delete`: delete a course from the list

## What's next?
- [ ] Adds a total credit count for `list`.
- [ ] Saving/Loading course plans.
- [ ] Adding proper error handling.
- [ ] Gantt-like chart for visualizing occupied time per day.
