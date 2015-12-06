# ProQodPy

ProQod is an autograder for institutes for programming assessment marking. ProQodPy is developed for Python assignment.

## Requirement Specifications

### Common interction specs
1. Single Authentication by password.

### Students' interaction specs
1. Weekly Quiz. This can be in the form of `MCQ`, `Programming`, or `Fill-In-The-Blank`.
2. Weekly Coursework Assessment. This can be in the form of `Proramming` and `Fill-In-The-Blank`.
3. Check-off. For non-digital assessment, students can let teacher give credits by password.
4. Project. Student can `Submit Code`, `Check Quality` and `Check Plagiarism`.
5. Exam. Time-limited and requirement same as Assessment.

### Teachers' interaction specs
1. Course Management. Teachers have an UI to customize courses, classes, students, weeks, Assessments and types, allocate marks and grades.
2. Course Statistics. Teachers can see the statistics of the class and cohort.
3. Window to execute SQL.

## System Requiremnet
The system architecture uses a Front-Back approach which loosely couples the Front-end and Back-end of the system and communicate via JSON.

### Front-end
Front-end uses the following frameworks:
* Jquery
* AngularJS
* Zurb Foundation 6

Reference:
`http://websymphony.net/almost-flat-ui/#doc-pagination`


### Back-end
Back-end is a RESTful API engine which includes:
* Python
* Django
* Django-Rest-Framework

The design pattern of Project will split into Front-end and Back-end, where front-end will be handled by AngularJS whereas the back-end will be a pure REST API server by Django and DRF.

### Host
The source code is hosted at Github:
```https://github.com/junhua/proqodpy.git```

The staging server will be at DigitalOcean, To be setup.

