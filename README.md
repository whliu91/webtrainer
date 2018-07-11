# Webtrainer
Web application for creating, training and testing Artificial Neuron Networks Online.

## Working environment Setup

For developers who is working on or want to contribute to the project. The web application is powered by (tested on) Django 1.11.8 on Python 3.6.5 with Google Chrome Browser, to setup working environment, follow below steps:

- Setup required software for this project

|tools|website|descriptions|
|-|-|-|
|git|https://git-scm.com/|version control|
|python|https://www.python.org/downloads/release/python-365/|python 3.6.5|
|MySQL|https://dev.mysql.com/downloads/mysql/5.7.html#downloads|database for project (changable)|
|RabbitMQ|https://www.rabbitmq.com/download.html|async message broker (changable)|

*When installing MySQL, select full-install, and you will be prompted to create a root user's account, do remember the credentials which will be required in the django `SETTINGS.py`

- setup environment
If you are not familiar with python virtualenv, read this(https://virtualenv.pypa.io/en/stable/) first.

Clone this repository using git, and run
```sh
$ bash script/setup_env.sh
```
*Python's Virtualenv directory is slightly different under Windows and Unix-like OS. This script automatically handles this directory differences, however if you are coding in Windows, you would probably need something that provides a shell like interface to run this script - this is not tested, otherwise, setup a virtualenv and install requried packages `(script/requirements.txt)` via pip manually.

- config RabbitMQ
The difference in windows and unix-systmes are minor for RabbitMQ, ultimately just use the `.bat` files in the installed packages in windows that has the same name with those in shell. 

In the terminal/cmd.exe, type: 
(replace `myuser` and `mypassword` to something you can remenmber, this will be required in `SETTINGS.py` as well)

|Unix|Windows|
|-|-|
|sudo rabbitmqctl add_user myuser mypassword|rabbitmqctl.bat add_user myuser mypassword|
|sudo rabbitmqctl set_user_tags myuser administrator|rabbitmqctl.bat set_user_tags myuser administrator|
|sudo rabbitmqctl add_vhost vhost|rabbitmqctl.bat add_vhost vhost|
|sudo rabbitmqctl set_permissions -p vhost myuser ".*" ".*" ".*"|rabbitmqctl.bat set_permissions -p vhost myuser ".*" ".*" ".*"|
|rabbitmq-plugins enable rabbitmq_management|rabbitmq-plugins.bat enable rabbitmq_management|

Go to {hostip(normally 127.0.0.1)}:15672 to see if this worked

- go to venv and setup project
activate the venv by:
```sh
$ source venv/bin/activate
```
or on windows:
```sh
venv/Scripts/activate.bat
```
cd to src/com/django/django/webtrainer/
under `\webtrainer` folder, there is a `settings.py`
change the `DATABASES` property to your MySQL root user config and
the `BROKER_URL` to your RabbitMQ credentials.

Then, initialise database with:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

- start server and test!
The easiest way to test the application is to run the server using django built-in server.

```sh
$ python manage.py celery worker --loglevel=info
$ python manage.py runserver
```
default server runs on http://127.0.0.1:8000/

### Prerequisite-Tools
List of all the packages used in this project (updating)
#### Front End
*BootStrap - multiple version see html templates in templates folders.* <br />
*Vue.js 2.0* <br />
*iView 2.0* <br />
*axios 0.18.0* <br />

#### Back End
**Django 1.11.8**
- Because we are using django-users2 for simplify developing a user management application, which is only compatible with Django 1, in case migration to Django 2 is required, we will have to re-implement the user management function.

**Python 3.6.5 64bit**
- Currently, the official Tensorflow distribution runs only on 64 bit OS

**RabbitMQ**
- message broker between django and celery
- make sure start a virtual host (vhost) and enable management plugin with
```sh
$ rabbitmq-plugins enable rabbitmq_management
```

**MySQL 5.7.22**
- Django 1 is not compatible with the current latest MySQL(8.0), if upgrade required will have to upgrade Django version first

**Celery 3.1.18**
- From Celery 3.1 onwards, django-celery connector is not required

**Tensorflow 1.8**
- latest at development time, probably worthwile to investigate in installing GPU version of Tensorflow
- Tensorflow is not the only backend option, for example, if you are looking into deploy the project under a 32 bit
OS, you might want to use Theano instead.

**Keras 2.2.0**
- Deep Learning framework on top of Tensorflow

**matplotlib 2.2.2**
- For drawing NN model Note: in Unix like system for Matplotlib to run, it is probably required to build tkinter independently with the following command “sudo apt-get install python3-tk”

**pandas 0.23.3**
- used along keras
