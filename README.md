# Search Engine with Web Analytics. Team 2
# IRWA Final Project

In this repository you will find the code for the UPF IRWA final project from group 2 (Ferran Pérez and Guillem Moreno)

This final project consist on a search engine which implements different indexing and ranking algorithms.

The project has already ended, and it contains a repository as well as all the notebook that we have been using to progress on our search engine.

The full roadmap of the project is the following:
 
 
| Part | Topic | Deadline |
| --- | --- | --- |
| 1 | Text Processing | 29/10/2021 |
| 2 | Indexing and Evaluation | 11/11/2021 |
| 3  | Ranking | 29/11/2021 |
| 4 | User Interface and Web Analytics | 03/12/2021 |

In the Jupyter Notebook, you will find different cells that must be executed in order
 - The first cell will install all the necesary libraries that may not be installed in the user environment.
 - The following cells have the necessary imports, functions, and code in order to process the text.
 - After this point, you will find the code for all the different parts of the Final Project

ATENTION! YOU MUST CHANGE THE PATH OF THE INPUT FILE TO THE ONE OF YOUR COMPUTER!

Regarding the final app, you will find a repository that you just need to donwload to your computer. After this, go inside the repository and just run the web_app.py python code in an appropiate virtual environment. The environment must have the following dependencies installed:

* Flask
* matplotlib
* collections
* numpy
* json
* nltk
* num2words

You will find more details about our web application in our report.

Thank you.

## Starting the Web App

```bash
python -V
# Make sure we use Python 3

python web_app.py
```
The above will start a web server with the application:
```
 * Serving Flask app 'web-app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8088/ (Press CTRL+C to quit)
```

## Virtualenv for the project (first time use)
### Install virtualenv
Having different version of libraries for different projects.  
Solves the elevated privilege issue as virtualenv allows you to install with user permission.

In the project root directory execute:
```bash
pip3 install virtualenv
virtualenv --version
```
virtualenv 20.10.0

### Prepare virtualenv for the project
In the root of the project folder run:
```bash
virtualenv .
```

If you list the contents of the project root directory, you will see that it has created several sub-directories, including a bin folder (Scripts on Windows) that contains copies of both Python and pip. Also, a lib folder will be created by this action.

The next step is to activate your new virtualenv for the project:
```bash
source bin/activate
```
This will load the python virtualenv for the project.

### Installing Flask and other packages in your virtualenv
```bash
pip install Flask pandas nltk faker
```

Enjoy!

