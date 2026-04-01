# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Three things a user should be able to do:

1. Add a pet — Enter basic info about themselves and their pet.
2. Add tasks — Create care tasks like walks or feedings with a duration and priority.
3. See today's plan — Generate a daily schedule that shows what to do and when.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I chose four classes:

- **Owner** — holds the user's info and their list of pets
- **Pet** — holds basic pet info like name, species, and age
- **Task** — represents one care task with a type, duration, and priority
- **Schedule** — holds all tasks and is responsible for building the daily plan

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the skeleton:

1. Changed `Task` to store `pet_name` (a string) instead of the full `Pet` object,
   to keep the classes loosely coupled and easier to manage.

2. Added `available_minutes` to `Schedule` so the scheduler can respect
   the owner's time budget when building a daily plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
