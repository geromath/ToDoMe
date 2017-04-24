﻿# ToDoMe  [![Build Status](https://travis-ci.org/geromath/ToDoMe.svg?branch=master)](https://travis-ci.org/geromath/ToDoMe)  [![Coverage Status](https://coveralls.io/repos/github/geromath/ToDoMe/badge.svg?branch=master)](https://coveralls.io/github/geromath/ToDoMe?branch=master)

![ToDoMe](https://raw.github.com/geromath/ToDoMe/dev/images/todome_logo.png)



# Table of contents 
- Project description 
- Getting started 
- Prerequisites 
- Installation 
- Running the application
- Running the tests 
- Built with 
- Contributing 
- Authors 
- License 
- Acknowledgments  

# Project description 
ToDoMe is a web-based task manager that lets you organize your tasks for the day and week in an easy manner. 
You earn credits for completing tasks you set for yourself and for passing the quizzes created by your teacher. 
ToDoMe helps the students repeat the curriculum throughout the semester and it gives the professors a better overview of their students progress.


# Prerequisites

- <a href="https://www.python.org/downloads/">Python 2.7+ </a>

# Installation  

- Clone the repo by typing the following command in terminal:
`git clone https://github.com/geromath/ToDoMe.git`
- Ensure you have setuptools installed, by typing the following command in terminal:
`pip install setuptools`
- Navigate to the ToDoMe directory and type the following command in terminal:
`pip install -r requirements.txt` 
- Navigate into the root directory (/ToDoMe/root) and type the following command in terminal:
- `python manage.py migrate` alternatively `python3 manage.py migrate`
- `python manage.py makemigrations todolist quizzes`
- `python manage.py migrate`

# Running the application

- You are now ready start ToDoMe
- In terminal, type the following command:
`python manage.py runserver`
- The server is now running, and you can navigate to ToDoMe using your preferred browser, and entering "http://localhost:8000/" into the search bar

# Running the tests  

Explain how to run the automated tests for this system 
Break down into end to end tests
 Explain what these tests test and why
 Give an example
 And coding style tests

Navigate to the folder where the manage.py file is and
- In the terminal, type: 'python manage.py test'


# Built With

- <a href="https://www.djangoproject.com/">Django</a>
- <a href="https://www.python.org/">Python</a>
- <a href="http://getbootstrap.com/">Bootstrap</a>
- <a href="https://www.javascript.com/">Javascript</a>
- <a href="https://jquery.com/">JQuery</a>
- <a href="https://www.sqlite.org/">SQLite</a>
- HTML
- CSS


# Contributing
- Make sure you have a GitHub account
- Fork the repository on GitHub
- Create a new branch: `git checkout -b newbranchname`
- Commit changes: `git commit -m "Your text"`
- Push to branch: `git push origin newbranchname`
- Submit pull request

__Making changes:__

Create a topic branch from where you want to base your work.
This is usually the master branch.
Please avoid working directly on the master branch.

To create a new branch, type 'git checkout -b newbranchname'

Make commits of logical units.
Check for unnecessary whitespace with "git diff --check" before committing.
Make sure your commit messages are in the proper format.
- Make sure you have added the necessary tests for your changes.
- Run _all_ the tests to assure nothing else was accidentally broken.

# Authors  
- Mathias
- Erik
- Caroline
- Marius

# License
This project is licensed under the MIT License - see the LICENSE.md file for details  .

# Acknowledgments  
NTNU TDT4140 course staff - Spring 2017.






