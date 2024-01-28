# NOTES WEB APPLICATION

By Clement Gyasi Siaw

Video overview: [Watch Video Overview](https://youtu.be/8d4846Mvj2s)
Web App: [Notes Web Application](https://notes-web-app-3bc233b8164a.herokuapp.com)

## Scope

This Web Application allows users to create a web account, publish notes and delete these notes anytime they want from their account. The notes can be dates of events, paragraphs describing oneself or an important event, articles and other important information. 

## Running

In vs-code navigate to the root directory and create a virtual environment (venv) and activate the venv depending on the operating system. In the same root directory run `sqlite3 database.db` to open database.db with sqlite3. When you run `.schema ` in the SQLite prompt, database.db comes with the `users` and `notes` table. After running `flask run` in the terminal, open the given link in a browser to access the web application.

## Understanding

### app.py

Atop `app.py` are a bunch of imports, among them is Havard's CS50’s SQL module and a few helper functions. Other imports include `generate_password_hash` from `werkzeug.security` used for generating hashed passwords of users.
After configuring Flask, this file disables caching of responses, else the browser will not notice any changes made to the file. It then further configures Flask to store sessions on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask’s default. The file then configures CS50’s SQL module to use database.db which is a SQlite database. After that, there are a number of routes which will be discussed later in detail.

### helpers.py

This file also contains the `login_required` function. The function is used to automatically direct users to the login route if the user has not logged in or after a user logs out of the app.

### requirements.txt

That file simply prescribes the packages on which this app depends.

### static/

Contains `style.css` where some initial CSS lives.

### templates/

The templates folder contains all templates used to build the web app, stylized with Bootstrap. `layout.html` is the base template to which all other templates are linked. It defines a block, `main`, inside of which all templates shall go. It also includes support for Flask’s message flashing so that messages can be relayed from one route to another for the user to see. The other templates will be discussed in great detail later in this report.

### schema.sql

This files contains the schema and all other entities of the database. You can reset the database by running `.read schema.sql` in sqlite3.

### databse.db

This is the databse which contains all the relevant tables which will be used to manage all the data of the web application.

## Specification

### /sign_up and sign_up.html

The `/sign_up` route in `app.py` allows a user to register for an account via `sign_up.html`. The user is required to complete all fields. If a field is filled with wrong input or is left blank, a flash message is used to prompt the user for correction. Before a user submits the registration form, there is a check to ensure that, the email provided does not already exist in the database. Users' account information is stored on the `users` table in the database.

### login and login.html

The `/login` route is used to log users into their account via `login.html`. Validation is done to ensure that, the username and password provided by the user exists in the database. If a user's record exists, the user is successfully logged into their account and directed to the root directory `index.html`, which at this stage, contains an empty field to be filled with notes. The user's `id` from the database is then stored in Flask's `session` for identification.

### /index and index.html

`/index` displays an html form via `index.html`. This form is filled with notes of any kind and when submitted via POST, is displayed on the same page. Many notes can be added as much as possible.


### /logout

This route logs out users from their account by clearing Flask's `session`. They are then redirected back to the login page.