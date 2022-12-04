# Django Blog 
Django app for a personal blog. You can find this app working on (https://www.laestanciaazul.com)

## CONTENTS
- [Introduction](#INTRODUCTION)
- [Installation and Execution](#INSTALLATION-AND-EXECUTION)
  - [Download](#Download)
  - [Preparation of server](#Preparation-of-server)
  - [Start server](#Start-server)
  - [Configuration](#Configuration)
- [Screenshoots](#SCREENSHOTS)


## INTRODUCTION

I started this app in 2017 as a side project in order to start learning the Django framework. The goal I had with this project was at the same time to develop a tool where I could write (kind of a diary) all
the stuff I learn on a daily basis. I try to keep writting at least two posts every month in the blog. You can follow me in the "blue nowhere" :)

The name I gave to this project (laestanciaazul) comes from the book "The blue nowhere" from Jeffery Deaver, that I read in 2001 when I was a teen. This book was one of the reasons, among many other :), that force
me to decide studying Computer Science in University. 

The book tells the story about a serial killer (Phate) in Silicon Valley, that uses his hacking abilities to enter in their victims lives in order to kill them. The police of California, in a desperate attempt to capture
the killer contact anothe hacker, the good guy of the story, named Gillete. Who takes it personal to capture Phate. You can read more: https://www.jefferydeaver.com/novel/the-blue-nowhere/

## INSTALLATION AND EXECUTION

### Download

First clone this repository
```
\downloads\git clone https://github.com/IsmaelB83/laestanciaazul
```

### Preparation of server

This django app has been tested in several linux servers, and works by default (see settings.py) with a Postgree database. Therefore the first thing we need to do is prepare our system to have both python, postgree, etc installed and ready.

Installing software in our linux
```console
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

Preparing the virtualenv and activating (optional but recommended)
```console
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
virtualenv webenv
source myprojectenv/bin/activate
(webenv) (ready)
```

Install requirements in the virtuaenv. This will install all the modules indicated in requirements.txt
```console
(webenv) pip install -r requirements.txt
```

Configure postgree and create the database:
```console
sudo -u postgres psql
postgres=# CREATE DATABASE myproject;
postgres=# CREATE USER myprojectuser WITH PASSWORD 'password';
postgres=# ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
postgres=# ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE myprojectuser SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
postgres=#\q
```

Before doing the first migration process you need to comment first one lie in file /post/forms.py, due to that sentence is trying to get categories from the database where they don't exist already. Therefore the migfrate process will fail. After the database is created you
can restore the instruction back to it's original value:
```
# CATEGORY_CHOICES = [[c.id, c.name] for c in apps.get_model('category', 'Category').objects.all()]
CATEGORY_CHOICES = ['PROGRAMING']
```

Prepare database with the structure required by the application:
```console
(webenv) ./manage.py migrate
(webenv) ./manage.py makemigrations
(webenv) ./manage.py createsuperuser
```

### Copy Statics

Before starting the server we need to collect statics
```console
(webenv) ./manage.py collectstatic
```

### Start server

First we need to activate the virtuaenv (in case we are using one):
```console
source webenv/bin/activate      
```

Once the virtualenv is activate (notice the "webenv" before the prompt), we can start the server trough manage.py. By using 0.0.0.0:8080 we can specify the port where the server is going to listen, and morever it will be accessible from the
outside (by using the dns or IP of our server). In order to configure this for production you need to use apache, nginx, etc. For which there are several user guides on the internet.
```console
(webenv) ./manage.py runserver 0.0.0.0:8080
Performing system checks...

System check identified no issues (0 silenced).
November 01, 2019 - 16:43:50
Django version 1.11, using settings 'web.settings'
Starting development server at http://0.0.0.0:8080/
Quit the server with CONTROL-C.
```

### Configuration

As you can see in settings.py. This app is dependent on a file called "passwords.json". This file should contain some important information that is required both for starting the app (secret and database password), as well as to be able to use oauth
in order to login in the app trough the apis of twitter, github, facebook or google. The file needs to be located in the base path of the application.

The structure of this json file should be as seen below:
```js
{
    "secret": "mydjangosecretkey",
    "database_password": "mydatabasepassword",
    "github": {
        "key": "githubkeyforoauth",
        "secret": "githubsecretforoauth"
    },
    "twitter": {
        "key": "twitterkeyforoauth",
        "secret": "twittesecretforoauth"
    },
    "facebook": {
        "key": "facebookkeyforoauth",
        "secret": "facebooksecretforoauth"
    },
    "google": {
        "key": "googlekeyforoauth",
        "secret": "googlesecretforoauth"
    }
}
```


## SCREENSHOTS

### Home

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/home.jpg).

### Post

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/post.jpg).

### Post editor

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/post_editor.jpg).

### Login

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/login.jpg).

### Archive

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/archive.jpg).

### Contact

![alt text](https://raw.githubusercontent.com/IsmaelB83/laestanciaazul/master/static/img/readme/contact.jpg).

