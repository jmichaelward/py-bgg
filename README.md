I <3 Python.

This project is exploratory only. It's purpose is to:

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
1. Copy the .env.example file to .env in the same directory and 
    fill in your local database credentials.
2. Create a new MariaDB database named `py-bgg` and import the `database-setup.sql` file.
3. Run `pip3 install -r requirements.txt` to download dependencies.
4. Consider making the main.py file executable with `chmod +x main.py` (Optional)
5. Start the app by running `./main.py` (if you did step 4) or `python3 main.py` if you didn't.
6. You should be able to visit http://127.0.0.1:5000 to see the main page, or http://127.0.0.1:5000/add-user to 
    add a user to the database (that's pretty much it thus far, jas of 4/6/20).
    
    
### Helpful Resources
Figured I might as well log some helpful resources I come across during my journey in this project.

1. [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

