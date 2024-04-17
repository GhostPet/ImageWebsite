<h1 align="center">
  <a href="https://github.com/GhostPet/ImageWebsite">
    Manga Website
  </a>
</h1>

<div align="center">
  Will be used for implementing image protection techniques
</div>

<div align="center">
<br />

[![license](https://img.shields.io/github/license/GhostPet/ImageWebsite?style=flat-square)](LICENSE)
[![made with ♡ by GhostPet](https://img.shields.io/badge/made_with_%E2%99%A1_by-GhostPet-orange?style=flat-square)](https://github.com/GhostPet)

</div>

---

<details open="open">
<summary style="font-size:1.4rem;"><b style="font-size:1.5rem;margin-left:0.5rem">Table of Contents</b></summary>

- [About](#about)
- [Getting Started](#getting-started)
  - [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [DB Connections](#db-connections)
  - [Heroku Server Connections](#heroku-server-connections)
- [Roadmap](#roadmap)
- [License](#license)

</details>

---

## About

A manga website created for being used for implementing image protection techniques.
This is a modified repo of the [Create A Flask Blog - Flask Friday](https://youtube.com/playlist?list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&si=RXuNuItgTL_ntbHJ) by [Codemy.com](https://www.youtube.com/@Codemycom)

## Getting Started

### Quick Start
The recommended method to install **Manga Website** is by using [Git](https://git-scm.com/download)'s bash terminal.

To install them, you can copy and paste the code below line by line:
```sh
python -m venv ImageWebsite 
source ImageWebsite/Scripts/activate

pip install -r requirements.txt
```

Then make sure you can connect the Db of your choice with filling the information in "app.py".

### Prerequisites

Create a virtual environment for the project and activate:

```sh
python -m venv ImageWebsite 
source ImageWebsite/Scripts/activate
```

Install the prequities:

- **Flask** 3.0.2 - [Flask 3.0.x Docs](https://flask.palletsprojects.com/en/3.0.x/)

- **Flask-WTF** 1.2.1 - [Flask-WTF 1.2.x Docs](https://flask-wtf.readthedocs.io/en/1.2.x/)

- **Flask-SQLAlchemy** 3.1.1 - [Flask-SQLAlchemy 3.1.x Docs](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)

- **Flask-Migrate** 4.0.7 - [Flask-Migrate lastest Docs](https://flask-migrate.readthedocs.io/en/latest/)

- **Flask-Login** 0.6.3 - [Flask-Migrate 0.6.3 Docs](https://flask-login.readthedocs.io/en/0.6.3/)

- **cryptography** 42.0.5 - [cryptography 42.0.5 Docs](https://cryptography.io/en/42.0.5/)

- **Flask-CKEditor** 0.5.1 - [Flask-CKEditor lastest Docs](https://flask-ckeditor.readthedocs.io/en/latest/)

To install them, you can copy and paste the code below:
```sh
pip install -r req.txt
```

### DB Connections
- **For SqLite connection:**
  You can change the app.py

- **For MySQL connection:**
  You can change the app.py. Afterwards, you may need to install these additional libraries.
  - **PyMySQL** 1.1.0 - [PyMySQL lastest Docs](https://pymysql.readthedocs.io/en/latest/) - For connecting the db with Flask-SQLAlchemy
    ```sh
    pip install PyMySQL
    ```
  - **mysql-connector-python** 8.3.0 - [mysql-connector-python Docs](https://dev.mysql.com/doc/connector-python/en/) - For creating a db without using additional tool
    ```sh
    pip install mysql-connector-python
    ```

  And to create a new db without using a tool like MySQL Workbench, you should create a new file, paste the code below inside, fill it with your db information, and execute the file. Then you can delete the file.
  ```py #2 create_db.py
  import mysql.connector
  mydb = mysql.connector.connect(host="", user="", passwd="") #Fill here
  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE users_db")
  mycursor.close()
  mydb.close()
  ```

- **For PostgreSQL connection:**
  You can change the app.py. Afterwards, you may need to install these additional libraries.
  - **psycopg2** 2.9.9 - [psycopg2 Docs](https://www.psycopg.org/docs/) - For connecting the db with Flask-SQLAlchemy
    ```sh
      pip install psycopg2
    ```
  > **Note:** PostgreSQL is not support the db.Text length.


For Db migrations, after the changes you may use the command below:
```sh
flask db migrate -m 'Comments'
flask db upgrade
```

### Heroku Server Connections

First you need to install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). After the installation, you must restart the terminal.
Then you can install this library.
- **gunicorn** 22.0.0 - [gunicorn 22.0.0 Docs](https://docs.gunicorn.org/en/22.0.0/)
  ```sh
    pip install gunicorn
  ```

Then you can use the following code to log in your heroku account and create an app:
```sh
  heroku login
  heroku create image-website
  heroku addons:create heroku-postgresql:essential-2 --app image-website
```

After your db created, you can get the connection link of it and change the information on "app.py".
```sh
  heroku config --app image-website
```

Then you can save the changes and push.
```sh
  git commit -am 'Tweaked app for Heroku'
  git push
  git push heroku main
```

## Roadmap

See the [open issues](https://github.com/GhostPet/ImageWebsite/issues) for a list of proposed features (and known issues).

## License

This project is licensed under the **MIT license**. Feel free to edit and distribute this website as you like.

See [LICENSE](LICENSE) for more information.