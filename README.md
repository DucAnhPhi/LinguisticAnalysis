# Linguistic Analysis

As part of my Bachelor's thesis I implemented a program which computes
and displays the textual features of a person's tweets. With the gained
insights from that program, I trained a Neural Network to classify the
tweets by their creator.


- [Installation](#installation)
- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Author](#author)
- [License](#license)

## Installation
* Install Python 3.6 (if not already installed)

* When installing a new python version there may be the '_tkinter' module missing, which is needed for matplotlib. To be on the safe side, install it by doing:

```
sudo apt-get install python3-tk
```

* **Recommended:**
Setup a python virtual environment for this project. It keeps the dependencies required by different projects in separate places.

```
$ pip install virtualenv

$ cd LinguisticAnalysis

$ virtualenv -p python3.6 LinguisticAnalysis
```
* To begin using the virtual environment, it needs to be activated:

```
$ source LinguisticAnalysis/bin/activate
```

* Finally install all dependencies running:

```
$ python setup.py
```

* If you are done working in the virtual environment for the moment, you can deactivate it:

```
$ deactivate
```

* To delete a virtual environment, just delete its folder.

```
rm -rf my_project
```

## Getting started

Before you can make any API request to Twitter, you’ll need to create an application at
https://dev.twitter.com/apps. Creating an application is the standard way for developers
to gain API access and for Twitter to monitor and interact with third-party platform developers
as needed

* After registering your application, at this point, you
should have a **consumer key**, **consumer secret**, **access token**, and **access token secret**.


* In Unix environments, such as Linux or macOS, if your shell is Bash, set the
environment variables as follows:

```
$ export TWITTER_CONSUMER_KEY="your-consumer-key"

$ export TWITTER_CONSUMER_SECRET="your-consumer-secret"

$ export TWITTER_ACCESS_TOKEN="your-access-token"

$ export TWITTER_ACCESS_SECRET="your-access-secret"

```

* In a Windows environment, set the variables from the command line as follows:

```
$ set TWITTER_CONSUMER_KEY="your-consumer-key"

$ set TWITTER_CONSUMER_SECRET="your-consumer-secret"

$ set TWITTER_ACCESS_TOKEN="your-access-token"

$ set TWITTER_ACCESS_SECRET="your-access-secret"
```

## Project structure

Executables

* [neural_network.py](neural_network.py): Neural network for supervised machine learning
* [linguistic_analysis.py](linguistic_analysis.py): Compute textual features of tweets
* [setup.py](setup.py): Setup script for downloading all dependencies

Other files

* [utils.py](utils.py): Reusable functions
* [twitter_api_setup.py](twitter_api_setup.py): Setup Twitter client for API calls
* [flesch_kincaid.py](flesch_kincaid.py): Compute Flesch Kincaid readability tests
* [dataset.py](dataset.py): Prepare datasets for Neural Network

Unit tests

* [utils_tests.py](utils.tests.py)
* [linguistic_analysis_tests.py](linguistic_analysis_tests.py)
* [dataset_tests.py](dataset_tests.py)
* [neural_network_tests.py](neural_network_tests.py)

## Author

* **Duc Anh Phi**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
