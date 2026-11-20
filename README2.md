Study Shift
A mobile-first study app that turns assigned BIOL 101 material into a quick review, a glossary, and practice questions with answers students can trace back to the source.

Ivy Tech 2030 IT Challenge · Case 2 · Alternative-Format Study Tool
Run the demo
From the repository root, run:
python3 -m http.server 8080 --directory case2
Leave the terminal running and open Study Shift on your laptop. The app uses a JavaScript module, so open it through the server. The local prototype runs with the bundled sample data.
Judge walkthrough
1. Select The Scientific Method and tap Start studying.
2. In Quick review, switch from Course wording to Plain English. Notice how the explanation changes while the course vocabulary stays visible.
3. Open Key terms and try Español where supplied glossary definitions are available.
4. In Practice, submit an answer and open View source to see the excerpt behind the explanation.
5. Open Get help to see where a student could turn for after-hours support. The listed routes are sample data.
1. Problem
Maya is a fictional Ivy Tech online student who studies late at night on her phone and speaks English as a second language. When course material comes in one format and her usual tutoring option is closed, she needs a way to work through unfamiliar terms, check her understanding, and know where to go if she is still stuck.
2. Solution
Study Shift gives Maya a short study session built around the material her instructor assigned. She chooses a lesson, reviews it in the wording that works for her, practices a question, and checks the explanation against the lesson.
Pilot feedback	Prototype response
The summary is still difficult to understand.	A reading-level control offers Course wording and Plain English. The glossary provides Spanish definitions where available.
It is hard to tell whether a quiz question comes from assigned material.	The practice flow ties questions to the selected lesson and shows the supporting source excerpt with the answer.
The student needs a person to ask when she is still stuck.	Get help shows sample tutoring and instructor routes, including an after-hours option.


3. Technical approach and architecture
[`case2/index.html`](case2/index.html) is the browser entry point. It uses the bundled [`case2/case_data.js`](case2/case_data.js) for course materials, practice, and support. The selected material ID connects the study views to the same lesson. Practice feedback shows a source excerpt so the student can check the explanation against the material.

The demo uses local sample content. A runtime AI integration point exists in the scaffold, with a sample fallback for the demo. The challenge prototype uses sample course materials and help information. In a campus rollout, instructors would approve course content and campus staff would verify support routes.

Use the existing data check from the repository root:
python3 case2/case2_data_test.py
Use the judge walkthrough above to check the interactive features independently of the data test.
4. Pillar and statewide strategy
- Pillar 1 · Academic & Instructional Quality
- Statewide strategy · Ensure Consistent Quality Across Learning Modalities
- A-Ivy focus · Learning and study support
Study Shift gives online learners another way to study the same assigned concepts while keeping the original course vocabulary and source material visible.

Proposed 2030 target · Increase online course completion by 3 percentage points in participating sections compared with comparable sections. A pilot would compare completion across similar courses and terms. The primary risk to monitor is a study answer that sounds plausible but lacks support in the assigned material.

[Read the 2030 Impact Statement](docs/IMPACT_STATEMENT.md)
5. How we used IBM Bob
We used IBM Bob to develop the prototype in stages. The team started with a template and gave Bob the case requirements, sample data, and Maya’s study flow. We then used focused prompts for the mobile frontend and roadblock features. For example, the source-reveal prompt translated a student concern into a concrete interaction that the team could check by comparing the excerpt with the selected lesson.
- [IBM Bob collaboration log](docs/BOB_LOG.md)
- [Development prompts](docs/PROMPTS.md)
- [Pilot feedback and roadblocks](docs/PILOT_FEEDBACK.md)
