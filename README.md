# Mirtronstructdb: A comprehensive database of mirtrons with predicted secondary structures



* Contact: Ruibang Luo, Shumin Li  
* Email: rbluo@cs.hku.hk, lishumin@connect.hku.hk
----

## Introduction

Mirtrons, a vital category of non-canonical microRNAs (miRNAs) originating from exon-intron boundaries through splicing mechanisms, play crucial roles in cellular processes. However, existing databases lack the latest data and structural information, hindering understandings of mirtron formation and functions.

MirtronStructDB is an online database addressing these gaps by incorporating over 350 novel mirtrons. Significantly, it provides corresponding predicted RNA secondary structures, offering a deeper understanding of the functional roles and mechanisms of all mirtrons. This enhances previous repositories, offering a total of 4,209 mirtron records spanning 25 species from 46 publications. Our database contributes for unraveling patterns and functions in mirtrons across species and diverse structural features. MirtronStructDB allows users to freely browse, search, visualize, and download data via a user-friendly interface.

In this repo, we provide the source code of the implementation of mirtronStructDB based on the flask framework.

## Online availability (recommended)

[MirtronStructDB](http://www.bio8.cs.hku.hk/msdb/) is available through the online web application


## Run it locally (not recommended)

### 1. Clone the repo
```bash
git clone https://github.com/HKU-BAL/msdb-flask/
```
### 2. Create the environment
  ```bash
  cd msdb-flask
  conda env create -f msdb.yml
  ```
### 3. Init the database

```bash
mkdir db
flask db init
flask db migrate -m "db init"
flask db upgrade
```
### 4. Congigurations

```bash
export IMG_DIR=YOUR_MIRTRON_HIGH_RESOLUTION_PATH
export SECRET_KEY=YOUR_SECRET_KEY
export MAIL_USERNAME=YOUR_MAIL_ADDR
export MAIL_PASSWORD=YOUR_MAIL_PSW
export ADMIN_MAIL=ADMIN_MAIL_ADDR
```

### 4. Run the app
```bash
gunicorn -w 2 -b 0.0.0.0:5555 wsgi:app --daemon
#change the port as you preferred

```
And open http://localhost:5555/ to access the application.

## New data submission
* If you would like to report new mirtron samples, please [contact admins](http://www.bio8.cs.hku.hk/msdb/contact)
