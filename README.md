# iReporter

## Badges

[![Build Status](https://travis-ci.org/mderek227/iReporterAPI.svg?branch=develop)](https://travis-ci.org/mderek227/iReporterAPI) [![Maintainability](https://api.codeclimate.com/v1/badges/45c45c9764de208c3303/maintainability)](https://codeclimate.com/github/mderek227/iReporterAPI/maintainability) [![Coverage Status](https://coveralls.io/repos/github/mderek227/iReporterAPI/badge.svg?branch=develop)](https://coveralls.io/github/mderek227/iReporterAPI?branch=develop)



## Features 

- Create a red flag record
- Get all red flag records
- Get a specific red flag record
- Edit a specific red flag record
- Delete a red flag record


## API Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v1/redFlag |Create a red flag record|
| GET | /api/v1/redFlag |Fetch all red flag records|
| GET | api/v1/redFlag/&lt;redFlag_id&gt; | Fetch a specific red flag record |
| DELETE | /api/v1/redFlag/&lt;redFlag_id&gt; /cancel | Delete a specific red flag record |

**Getting started with the app**

**Modules and tools used to build the endpoints**

* [Python 3.6](https://docs.python.org/3/)

* [Flask](http://flask.pocoo.org/)


## Installation

Create a new directory and initialize git in it. Clone this repository by running
```sh
$ git clone URL   which in this case is https://github.com/mderek227/iReporterAPI.git
```
Create a virtual environment named venv using
```sh
$ virtualenv venv
```
Activate the virtual environment
```sh
$ cd venv/scripts/activate
```
Install the dependencies in the requirements.txt file using pip
```sh

$ pip install -r requirements.txt
```
Populate the requirements.txt using

$ pip freeze  >  requirements.txt
```sh
Start the application by running
```
$ python run.py
```sh


## Author

Derrick Mananu


