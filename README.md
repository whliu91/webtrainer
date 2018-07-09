# Webtrainer
Web application for creating, training and testing Artificial Neuron Networks Online.

## Working environment Setup
For developers who is working on or want to contribute to the project. The web application is mainly powered by Django on Python 3.6.5, the current tools in use is listed here

### Prerequisite-Tools

#### Front End
*BootStrap - multiple version see html templates in templates folders.* <br />
*Vue.js 2.0*
*iView 2.0*
*axios*

#### Back End
**Django 1.11.8**
- Because we are using django-users2 for simplify developing a user management application, which is only compatible with Django 1, in case migration to Django 2 is required, we will have to re-implement the user management function.

**Python 3.6.5 64bit**
- Currently, the official Tensorflow distribution runs only on 64 bit OS

**RabbitMQ**
- message broker between django and celery

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
