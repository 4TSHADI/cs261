# Installation
- First clean your installation directory using the `./clean.sh` command.
- Then run `./setup.h` command to initialise the virtual environment, install the given requirements (specified in requiresments.txt) and start the flask server.
- To just run the flask server use the `./run.sh` command.

# GitHub
GitHub is a online code repository sharing platform. It is very useful for collaborative development. I suggest you become very familar with the basics you need, all briefly mentioned here. If you need more of a tutorial, the GitHub docs are great: https://docs.github.com/en/get-started/quickstart/hello-world).
<!-- TODO -->


# Helpful
## Database manipulation
- More comprehensive documentation here: https://sqlite.org/cli.html
- There is some template data in the `db_init()` function in the `db_schema.py` file. This data can be inserted into the database by changing the `resetdb` boolean to `True` in the `cwk.py` file.
- You can view the data in the database by clicking on the `database.sqlite` file in VS Code. This should open a window where you can view each table. (Might need to install an extension).
- You can open up the interactive database command line by typing `sqlite3 database.sqlite` in the command line in the directory the database is in. To exit this interactive command line press `Ctrl+D`.
- When in the interactive database command line here are a few useful commands:
  - `.tables` - lists all tables in the database.
  - `select * from <tablename>;` - print all rows in table.