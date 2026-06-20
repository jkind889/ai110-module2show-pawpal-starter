# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I designed 6 classes based off real world examples

Owner - a class that holds a list of Pet objects and methods to add a pet and fetch a list of scheduled tasks
Pet - a class that holds a pets name, species, breed and age as well as a list of task objects. Theres also methods to create add a task, remove tasks and get tasks by priority
Task - Holds a task id, task name and duration and priority, validate() which returns a boolean
WalkTask - holds distance, route notes, a boolean for a lesh and validate() which returns a boolean
Scheduler - takes an Owner + Pet object and sorts tasks by priority, filters by available times and produces of a list of ScheduledTask objects
ScheduledTask - takes a task object, a start time and an end time and a reason of the task

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Owner class has no path to scheduler since it owns no Scheduler instance and takes no pet argument
Priority into an enum instead of string
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
