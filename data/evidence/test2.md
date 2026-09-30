# Evidence Card

## Question
How is the Economic Analysis course graded?

## Model
- Name: gemma3:4b
- Parameters: 4.3B
- Quantization: Q4_K_M
- Mode: local

## Retrieved Passages

### Passage 1
- Source: `FTMBA 201A Economic Analysis Syllabus.txt`
- Section: Main
- Relevance: 59%

> FTMBA 201A: Economic Analysis for Business Decisions
Course Syllabus: Fall 2026
(Oprea sections: 03A Oski & 04A Axe)
Version: August 23, 2026

### Passage 2
- Source: `FTMBA 201A Economic Analysis Syllabus.txt`
- Section: We often have short polls and exercises during class, or short questions that you complete on
- Relevance: 51%

> bCourses before class. Where these are recorded, they will inform your participation grade.
Exams: We will have a midterm and a final exam. This involves a traditional exam format, on
paper, in person. The midterm is worth 15% of the course grade, and the final is worth 20% of the
course grade. To r...

### Passage 3
- Source: `Data and Decisions Syllabus.txt`
- Section: The Course
Course Objectives:
- Relevance: 46%

> Data and Decisions is not a typical statistics course. We move quickly, covering during
seven weeks everything from statistical tests and confidence intervals all the way through
interpretation and inference in multiple regression models. Along the way, we emphasize
deep ideas rather than memorizing...

### Passage 4
- Source: `FTMBA 201A Economic Analysis Syllabus.txt`
- Section: Finally, the syllabus also lists content from supplementary texts, which you should read as back
- Relevance: 46%

> ground as you see fit. Particularly for those of you with a limited background in economics, you
may want to have a textbook as a reference. Find a version that fits your purse and purpose.
• Samuelson and Marks Managerial Economics, 9th Ed. (or 8th, or 7th)
Page numbers below refer to the U.S. prin...

### Passage 5
- Source: `Data and Decisions Syllabus.txt`
- Section: Grading:
- Relevance: 43%

> 10% Attendance. Recorded using iClickers. Students can miss 1 class without
penalty. Attendance is tracked starting from Lecture 2.
50% Group Projects. The simple average of the take-home deliverables
determines this score.
40% Final Exam. The final exam is in person. You need to take this test in
o...

## Answer
The Economic Analysis course is graded with the following components: 15% for the midterm exam, 20% for the final exam, and a group project [Source: FTMBA 201A, Section: Group memo]. [Source: Data and Decisions, Section: Grading:] Attendance is worth 10%, Group Projects are worth 50%, and the Final Exam is worth 40%. The final grade is determined by an academic curve set by the instructor [Source: Data and Decisions, Section: Grading].

## Assessment

**Accuracy: PARTIALLY CORRECT.** After implementing source-separated prompting, the model now correctly identifies some FTMBA 201A grading components (midterm 15%, final 20%) from Passage 2. However, it also includes the Data and Decisions grading breakdown (10% Attendance, 50% Group Projects, 40% Final Exam) from Passage 5, mixing two courses in one answer.

**Improvement from source-separated prompting:** The model now correctly cites Data and Decisions as the source for the 10%/50%/40% numbers, instead of misattributing them to FTMBA 201A (as happened before the fix). The source boundaries are better respected, but the model still fails to exclude irrelevant source data from the answer.

**Actual FTMBA 201A grading:** Participation 30%, Quizzes 10%, Midterm 15%, Final 20%, Group Memo 15%, Examples in the Wild 10%. The full breakdown is not fully captured in the top-5 retrieved passages, which is a retrieval limitation.

**Root cause:** Two factors — (1) the complete grading breakdown for FTMBA 201A is split across passages not all in the top-5, and (2) the 4B model still includes tangentially retrieved evidence from a different course rather than filtering it out.

**Citations:** Now correctly attributed to their actual sources (improved from the original run where Data & Decisions numbers were misattributed to FTMBA 201A).
