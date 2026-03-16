# checkpoint_answers.md

# Checkpoint Question 1
What is the business purpose of the London Transport Data Engineering Project?
The purpose of the project is to build a data pipeline that collects and transforms London transport data into a reporting table. This helps analyze passenger activity, delays, and transport usage across stations and lines.

Checkpoint Question 2
Why are we using multiple raw source files instead of one clean table?
Because the data comes from different systems like stations, lines, and journeys. Keeping them as separate raw files preserves the original data and makes the pipeline easier to manage and transform later.

Checkpoint Question 3
What is the difference between ETL and ELT in this project?
ETL transforms the data before loading it into the database. ELT loads the raw data first and then transforms it inside the database. In this project, we use ELT with SQL in PostgreSQL.

Checkpoint Question 4
Why is it important to use your own public GitHub repository for this project?
It keeps the project organized, tracks changes, and allows others to see the work. It also serves as a portfolio to show data engineering skills.

Checkpoint Question 5
Which raw files seem to be the most important for building the final reporting output on Day 1, and why?
The journey or transport usage data is the most important because it contains key information like passenger counts, delays, stations, and transport modes used in the final report.

Final reflection
What was the most important thing you learned from Day 1?
I learned how to organize raw data, load it into a database, and use SQL transformations to create a reporting dataset in a real data engineering workflow.



## Submission reminder

Before finishing Day 1, make sure you have:

* answered all 5 checkpoint questions
* added your name
* added your public GitHub repository link
* committed this file
* pushed it to your GitHub repository

Example:

```bash
git add .
git commit -m "Add Day 1 checkpoint answers"
git push -u origin main
```

This file is part of your Day 1 deliverables, so do not skip it.


