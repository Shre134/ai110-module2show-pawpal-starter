# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Three things a user should be able to do:

1. Add a pet — Enter basic info about themselves and their pet.
2. Add tasks — Create care tasks like walks or feedings with a duration and priority.
3. See today's plan — Generate a daily schedule that shows what to do and when.


I chose four classes:

- **Owner** — holds the user's info and their list of pets
- **Pet** — holds basic pet info like name, species, and age
- **Task** — represents one care task with a type, duration, and priority
- **Schedule** — holds all tasks and is responsible for building the daily plan

**b. Design changes**



After reviewing the skeleton:

1. Changed `Task` to store `pet_name` (a string) instead of the full `Pet` object,
   to keep the classes loosely coupled and easier to manage.

2. Added `available_minutes` to `Schedule` so the scheduler can respect
   the owner's time budget when building a daily plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: task priority (high, medium, low)
and scheduled time. Priority was the most important because urgent tasks
like medication should never be bumped by lower-priority ones like playtime.

**b. Tradeoffs**




The conflict detector only flags tasks at the exact same time, not overlapping
durations. This keeps the logic simple but means a 30-minute task at 07:00 and
a task at 07:15 would not be caught.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude for brainstorming classes, generating skeletons, and writing
tests. The most helpful prompts were specific ones like "add conflict detection
that returns a warning instead of crashing."

**b. Judgment and verification**

Claude stored the full Pet object inside Task. I changed it to just the pet
name since it kept things simpler and less coupled.

## 4. Testing and Verification

**a. What you tested**

I tested task completion, sorting, conflict detection, and recurring tasks.
These cover the core behaviors the scheduler relies on.

**b. Confidence**

⭐⭐⭐⭐ — Core behaviors work. I'd next test overlapping durations and
owners with no pets.

## 5. Reflection

**a. What went well**

Keeping the backend separate from the UI made debugging way easier.

**b. What you would improve**

Add a proper time picker instead of a text input, and make conflict detection
duration-aware instead of just exact time matches.

**c. Key takeaway**

AI is great for boilerplate but you still have to make the real design calls.
If you accept every suggestion without thinking, the code gets messy fast.