# Repo Description

## 1.reportgenerator.py

This is the python file for the solution of the all the challenges.

## 2.unit_testing.py
This is the python file for the unit testing of the reportgenerator python file.

## 3.report.db

This is the database which contains 2 tables:
    
1. Petroleum_Report: It contains original dataset.
1. Normalized_Form: It contains normalized dataset.

## 4.requirements.txt

This is the txt file for all the dependencied to python file in the repo.

## 5.Results_Images

This folder contains images of results in command line and jupyter-notebook.

---

# How to run the code?

Follow the following steps to run the code:

## 1.Create a virtual environment: (in any directory you want)
    
```
python3 -m venv intern_env    
```  
(any name you wish to keep for virtual environment.)

## 2.Activating a virtual environment
    
```
source intern_env/bin/activate    
```

## 3.Installing Dependencies
    
```
pip install -r requirements.txt    
```

## 4.Run the code

```
python3 reportgenerator.py    
```
    
    report.db is created after running the code.

## 5.Run the Unit test

```
python3 unit_testing.py
```

# Linter Setup

I've used linter-flake8 in Atom Editor.
