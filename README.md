# selenium test framework sample

This repo provides the test framework for e2e test and UI operation tool by command line.
Also, this includes the test pipeline for e2e test on CICD.
Basically command line tool is used for executing any operation automatically on browser.


## Precondition
* Install modules for selenium and chrome.
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
$ sudo apt update
$ sudo apt -f install -y
$ sudo apt install python3-selenium
```

## Tools by commandline
1. install requirements :
``` 
$ pip install -r requirements.txt
```

2. Execute command
``` 
$ python commandline_tool.py
```

## Execute test
1. install requirements :
``` 
$ pip install -r requirements_test.txt
```

2. Execute command
``` 
$ pytest tests
```

## Flow of Jenkins test pipeline
1. Execute linter for python files updated on PR.
* linter contain pylint, flake8 and mypy.

2. Execute e2e test