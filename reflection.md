# PawPal+ Project Reflection

## 1. System Design
- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors
**a. Initial design**

- Briefly describe your initial UML design.
Pet ( dog breed, name, foodtype, collar number)
tasks ( walk,feed,play)
Schedule(time calaneder)
displayChart(Schedule)
Test functions
- What classes did you include, and what responsibilities did you assign to each?
pet class to store info
tasks class to store lenght of activitys
schedule to document time and date
displayChart to compile Schedule into a proper format 
Test functions to test all classes

**b. Design changes**

- Did your design change during implementation?
No
- If yes, describe at least one change and why you made it.
There were not much changes within the initial design besides some more expansion to the predetermined classes

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
I made a subclass of task that can document the constraints and their time requirments 
- How did you decide which constraints mattered most?
I decided it based on time it required to be done 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler currently checks for exact start/end time overlaps in `detect_conflicts()` but does not detect partial overlaps from duration ranges that cross (e.g., 7:30-8:00 vs 7:50-8:20). This is a lightweight design choice to keep conflict detection simple and non-blocking, but it means some real conflicts may be missed unless the user has common tie times.
- Why is that tradeoff reasonable for this scenario?
The app only pertains to simple pet care so a quick readable schedule and first-pass warning system is all that is needed; more complex conflict resolution could be added later using interval trees or a calendar library.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used them to input code considering I dont know python and from their i adjusted it based on the limitations and features i wanted
- What kinds of prompts or questions were most helpful?
there was no specific prompt or question that was most helpful as i had to repeatedly tell the ai to change its responses when code didnt fit. I followed a trial and error format
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
The ai attempted to gate priority to every task and task conflict at 0 and 1 but i wanted it to set a specific priority to a specific type of task so that it would be fixed every time rather then userinputed 
- How did you evaluate or verify what the AI suggested?
I went over each bit of code manually to see if it fit my image of the app
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Tested the printing logic
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
