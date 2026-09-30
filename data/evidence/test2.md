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
The Economic Analysis course is graded as follows:

*   10% Attendance, tracked using iClickers [Source: FTMBA 201A Economic Analysis Syllabus.txt, Section: Grading:]. Students can miss 1 class without penalty, starting from Lecture 2.
*   50% Group Projects, determined by the simple average of the take-home deliverables [Source: FTMBA 201A Economic Analysis Syllabus.txt, Section: Grading:].
*   40% Final Exam, which is in person [Source: FTMBA 201A Economic Analysis Syllabus.txt, Section: Exams]. 

The letter grade for each student is determined by an academic curve based on the numerical scores of the entire class [Source: FTMBA 201A Economic Analysis Syllabus.txt, Section: Grading:].

## Assessment

**Accuracy: INCORRECT.** The model returned the grading breakdown from *Data and Decisions* (10% Attendance / 50% Group Projects / 40% Final Exam) but attributed it to the Economic Analysis syllabus. The actual FTMBA 201A grading is: Participation 30%, Quizzes 10%, Midterm 15%, Final 20%, Group Memo 15%, Examples in the Wild 10%.

**Root cause:** Passage 5 (from Data and Decisions, relevance 43%) contains the 10%/50%/40% breakdown. The model incorrectly treated this as Economic Analysis grading despite the passage being from a different source. This is a known limitation of smaller models — they can conflate evidence from multiple retrieved passages.

**Citations:** Incorrect — cites FTMBA 201A but the numbers come from Data and Decisions.
