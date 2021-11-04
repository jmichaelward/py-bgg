I <3 Python.

This project is exploratory only. Its purpose is to:

1. Help reacquaint myself with database schema design.
2. Learn how Python interacts with the database layer.
3. See how to handle routing and form submissions in Flask.

The code in this project is neither production ready, nor
anything I'm proud of or intend to show off. Rather, I'm keeping
it in a public repository here so I can demonstrate my dedication
to learning and practicing core programming concepts, and 
also so I have a version-controlled place where I can pick up
where I left off should I switch between development environments.

### If for some reason you want to follow along
1. Copy the .env.example file to .env in the same directory.
2. Enter a value for FLASK_SECRET_KEY in .env. If you'd like to use a database other than sqlite, enter
    the URL and credentials for your database into the DB_URL field.
2. Create a new MariaDB database named `py-bgg`.
3. Run `pip3 install -r requirements.txt` to download dependencies.
4. Run `flask db upgrade` to run the database migration steps.
5. Flask should recognize the app.py file in the root of the project. Run the project with `flask run`.
6. You should be able to visit http://127.0.0.1:5000 to see the main page, which includes links to creating user data,
    viewing users, and viewing imported games.
    
    
### Helpful Resources
Figured I might as well log some helpful resources I come across during my journey in this project.

1. [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

