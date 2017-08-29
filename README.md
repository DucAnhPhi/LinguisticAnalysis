# Linguistic Analysis

As part of my Bachelor's thesis I implemented a program which computes
and displays the textual features of a person's tweets. With the gained
insights from that program, I trained a Neural Network to classify the
tweets by their creator.

## Installation WORK IN PROGRESS


Conda is an open source package manager and environment
manager for installing multiple versions of software packages (and related dependencies),
which makes it easy to switch from one version to the other. It supports Linux, macOS, and
Windows.

distributions that ship with conda: the batteries-included version,
Anaconda, which comes with approximately 100 packages for scientific computing already
installed

pip install tweepy==3.3.0

https://www.anaconda.com/download/

## Getting started

Before you can make any API request to Twitter, you’ll need to create an application at
https://dev.twitter.com/apps. Creating an application is the standard way for developers
to gain API access and for Twitter to monitor and interact with third-party platform developers
as needed

After registering your application, at this point, you
should have a **consumer key**, **consumer secret**, **access token**, and **access token secret**.

In order to promote the separation of concerns between application logic and configuration,
we're storing the credentials in environment variables.

In Unix environments, such as Linux or macOS, if your shell is Bash, you can set the
environment variables as follows:
```
$ export TWITTER_CONSUMER_KEY="your-consumer-key"

$ export TWITTER_CONSUMER_SECRET="your-consumer-secret"

$ export TWITTER_ACCESS_TOKEN="your-access-token"

$ export TWITTER_ACCESS_SECRET="your-access-secret"

```

In a Windows environment, you can set the variables from the command line as follows:
```
$ set TWITTER_CONSUMER_KEY="your-consumer-key"

$ set TWITTER_CONSUMER_SECRET="your-consumer-secret"

$ set TWITTER_ACCESS_TOKEN="your-access-token"

$ set TWITTER_ACCESS_SECRET="your-access-secret"
```
