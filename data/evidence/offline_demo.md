# Offline Demonstration

**Date:** 2026-09-29 22:39
**Python:** 3.12.10
**Internet connected:** YES - DISCONNECT BEFORE RUNNING

> WARNING: Internet is still connected. Disconnect WiFi/Ethernet and rerun this script.
> The test results below are still valid (all local), but offline status is not verified.

---

## 1. Search Mode

**Command:** `python wiki.py search "pricing"`

```
Searching for: pricing

Found 5 passages:

+- [1] FTMBA 201A Economic Analysis Syllabus.txt — III Class Schedule (releva-+
| • Lecture 1 (Mon 8/24): The double auction and competitive equilibrium–     |
| [Reading pack: TBD — net-new lecture]– Samuelson and Marks (SM) 9th Ed.     |
| Ch.1, Ch.7 to p. 208 (8th Ed. Ch.1, Ch.7 to p.                              |
| 224) (7th Ed. Ch.1, Ch.7 to p. 295)                                         |
| • Lecture 2 (Wed 8/26): The concept of economic cost– “Farms in Downtown    |
| Tokyo?!” (Hermalin)– “The Real Lessons From Kodak’s Decline” MIT Sloan      |
| Management Review Summer                                                    |
| 2016– Hermalin (H) pp. 29-37, pp. 44-46– SM9th: Ch.6 to p. 183 (8th: Ch.6   |
| to p. 199) (7th: Ch.6 to p.255...                                           |
+-----------------------------------------------------------------------------+
+- [2] FTMBA 201A Economic Analysis Syllabus.txt — This course presents a cur-+
| businesses and other organizations. These topics include decision-making    |
| under uncertainty, eco                                                      |
| nomic costs, pricing, and the basics of strategic interactions between      |
| competitors. The course will                                                |
| use readings and cases, along with class discussion, to develop practical   |
| insights into managing for                                                  |
| competitive advantage.                                                      |
| Key dates—subject to change:                                                |
| • Midterm (in class): Wednesday, September 16 — covers Lectures 1–6.        |
| • Final exam: Friday, October 16, 9:00–11:00 AM — Oski in N470, Axe in      |
| N570.                                                                       |
| • Pro...                                                                    |
+-----------------------------------------------------------------------------+
+- [3] Data and Decisions Syllabus.txt — AI Policy (relevance: 36%) ----------+
| 5                                                                           |
+-----------------------------------------------------------------------------+
+- [4] CLAUDIA ESI DENTU RESUME.txt — Formerly Vodafone Group PLC - A Multina-+
| •       Owned product strategy from concept to launch for a fintech         |
| marketplace serving 200k+ broadband customers, consolidating fragmented     |
| lifestyle services and onboarding 20+ partners to drive $20M in annual      |
| transactions                                                                |
| •       Drove the establishment of Telecel Ghana's AI Center of Excellence, |
| defining organizational structure, governance strategy, and solutions       |
| architecture; built the operating model now used to scale AI across the     |
| business                                                                    |
| •       Established Telecel’s AI Center of Excellence, defining org...      |
+-----------------------------------------------------------------------------+
+- [5] FTMBA 201A Economic Analysis Syllabus.txt — Main (relevance: 28%) -----+
| FTMBA 201A: Economic Analysis for Business Decisions                        |
| Course Syllabus: Fall 2026                                                  |
| (Oprea sections: 03A Oski & 04A Axe)                                        |
| Version: August 23, 2026                                                    |
+-----------------------------------------------------------------------------+
```

## 2. Ask Mode — Test 1

**Command:** `python wiki.py ask "What is the estimated global data-center electricity demand by 2030?"`

```
Question: What is the estimated global data-center electricity demand by 2030?

Retrieved passages:
  [1] AI & Sustainability.txt — The Sustainability of AI and AI for 
Sustainability: Confronting the Paradox of Responsible Innovation
Overview (58%)
  [2] AI & Sustainability.txt — Cross-Cutting Themes

The edited collection will feature contributions that address overarching 
themes on the Sustainability of AI and AI for Sustainability, including but not
limited to: (58%)
  [3] AI & Sustainability.txt — Guiding Questions: (47%)
  [4] CLAUDIA ESI DENTU RESUME.txt — EXPERIENCE (37%)
  [5] Data and Decisions Syllabus.txt — Final Exam (37%)

Generating answer...

+---------------------------------- Answer -----------------------------------+
| The International Energy Agency estimates that global data-center           |
| electricity demand could exceed 1,500 terawatt-hours by 2030 [Source: AI &  |
| Sustainability.txt, Section: The Sustainability of AI and AI for            |
| Sustainability: Confronting the Paradox of Responsible Innovation].         |
+---------------------- Model: gemma3:4b | Mode: local -----------------------+
```

## 3. Ask Mode — Test 2

**Command:** `python wiki.py ask "How is the Economic Analysis course graded?"`

```
Question: How is the Economic Analysis course graded?

Retrieved passages:
  [1] FTMBA 201A Economic Analysis Syllabus.txt — Main (59%)
  [2] FTMBA 201A Economic Analysis Syllabus.txt — We often have short polls and
exercises during class, or short questions that you complete on (51%)
  [3] Data and Decisions Syllabus.txt — The Course
Course Objectives: (46%)
  [4] FTMBA 201A Economic Analysis Syllabus.txt — Finally, the syllabus also 
lists content from supplementary texts, which you should read as back (46%)
  [5] Data and Decisions Syllabus.txt — Grading: (43%)

Generating answer...

+---------------------------------- Answer -----------------------------------+
| The Economic Analysis course is graded as follows:                          |
|                                                                             |
|  • 10% Attendance, tracked using iClickers [Source: FTMBA 201A Economic     |
|    Analysis Syllabus.txt, Section: Grading:]. Students can miss 1 class     |
|    without penalty, starting from Lecture 2.                                |
|  • 50% Group Projects, determined by the simple average of the take-home    |
|    deliverables [Source: FTMBA 201A Economic Analysis Syllabus.txt,         |
|    Section: Grading:].                                                      |
|  • 40% Final Exam, which is in person [Source: FTMBA 201A Economic Analysis |
|    Syllabus.txt, Section: Exams].                                           |
|                                                                             |
| The letter grade for each student is determined based on an academic curve  |
| [Source: FTMBA 201A Economic Analysis Syllabus.txt, Section: Grading:].     |
+---------------------- Model: gemma3:4b | Mode: local -----------------------+
```

## 4. Ask Mode — Test 3

**Command:** `python wiki.py ask "What is the AI usage policy for MBA courses at Berkeley Haas?"`

```
Question: What is the AI usage policy for MBA courses at Berkeley Haas?

Retrieved passages:
  [1] FTMBA 201A Economic Analysis Syllabus.txt — IV A note on AI (52%)
  [2] Data and Decisions Syllabus.txt — Recordings of courses are available for
viewing to: (50%)
  [3] Data and Decisions Syllabus.txt — Live stream viewing of courses is 
available to: (49%)
  [4] Data and Decisions Syllabus.txt — By enrolling in, or attending, any MBA 
courses, I acknowledge and consent to the
terms of this Privacy and Recording Notice and provide my authorization to the 
(49%)
  [5] Data and Decisions Syllabus.txt — Students in this course are allowed to 
use generative AI tools provided for certain
assignments and may use other generative AI tools unless specifically 
prohibited for a (48%)

Generating answer...

+---------------------------------- Answer -----------------------------------+
| Students in this course are allowed to use generative AI tools provided for |
| certain assignments and may use other generative AI tools unless            |
| specifically prohibited for a) given assignment [Source: Data and Decisions |
| Syllabus.txt, Section: Students in this course are allowed to use           |
| generative AI tools provided for certain assignments and may use other      |
| generative AI tools unless specifically prohibited for a) ]. The use of AI  |
| is strictly forbidden on the Final Exam, and any use during the Final Exam  |
| will trigger an automatic Failing Grade [Source: Data and Decisions         |
| Syllabus.txt, Section: Specifically, the use of AI is strictly forbidden on |
| the Final Exam. Any use of AI during the Final Exam will trigger an         |
| automatic Failing Grade on the course].                                     |
+---------------------- Model: gemma3:4b | Mode: local -----------------------+
```

## 5. Ask Mode — Test 4 (Unsupported)

**Command:** `python wiki.py ask "What is Esi's GPA at Berkeley Haas?"`

```
Question: What is Esi's GPA at Berkeley Haas?

Retrieved passages:
  [1] Data and Decisions Syllabus.txt — Graduate Student Instructor:
Shreya Chandra (50%)
  [2] CLAUDIA ESI DENTU RESUME.txt — EDUCATION (50%)
  [3] Data and Decisions Syllabus.txt — Recordings of courses are available for
viewing to: (48%)
  [4] FTMBA 201A Economic Analysis Syllabus.txt — GSI: Zac Pond (48%)
  [5] Data and Decisions Syllabus.txt — Live stream viewing of courses is 
available to: (48%)

Generating answer...

+---------------------------------- Answer -----------------------------------+
| The wiki does not contain sufficient evidence to answer this question. The  |
| passage regarding Claudia Esi Dentu’s education states she received a BSc   |
| Business Administration, Cum Laude Honors (First Class) at Ashesi           |
| University, but does not provide her GPA at UC Berkeley Haas.               |
+---------------------- Model: gemma3:4b | Mode: local -----------------------+
```

## 6. Help

**Command:** `python wiki.py --help`

```
Usage: wiki.py [OPTIONS] COMMAND [ARGS]...

  Esi's Personal Wiki CLI — chat, ask, search your personal knowledge base.

  Uses local Gemma model via Ollama with RAG for grounded answers. All modes
  work offline after initial setup.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  ask     Ask a factual question and get a cited answer from your wiki.
  chat    Start an interactive chat session with your wiki assistant.
  ingest  Ingest source documents and generate wiki pages.
  search  Search for matching passages in the wiki (no LLM generation).
```

## 7. Internet Status Verification

Internet reachable at end of test: **Yes**