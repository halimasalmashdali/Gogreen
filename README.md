# GoGreen App

GoGreen is a Android/IOS app written with Kivy library in Python. It provides a seamless and interactive platform for users to complete different eco-friendly challenges.

## Project Structure

```
GoGreen/
    assest/
        photos/
            decor.png
            login_photo.png
            logo.png
            ...
    screens/
            login_screen.kv
            reg_screen.kv
            welcome_screen.kv
            ...
    .gitignore
    main.py
    README.md
    requirements.txt
    users.db
```

## Getting Started

To run the GoGreen app locally, follow these steps:

1. Clone the repository:

   ```bash
   https://github.com/halimasalmashdali/Gogreen.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   - Create a `.env` file in the project root.
   - Add the following lines to the `.env` file:

     ```env
     DATABASE_URL=sqlite:///users.db
     ```

4. Run the app:

   ```bash
   python main.py
   ```


The app widget should automatically open in your screen

## Features

- **User Authentication:** Secure user registration and login with password.
- **Dynamic Challenges List:** Automatically updates the chellenges list with new messages.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.

## Project Architecture

### `main.py`

Holds all screen actions and connections
Entry point for running the server. Initializes the Kivy app and database communication events.

### `.env`

Configuration settings for the app, including the secret keys and database URI.

### `database.py`

Database models and schema definition using SQLAlchemy. Includes user, challanges and news models.

### `screens`

Directory in which all Kivy code is written.

### `assets`

Directory where all assets such as font and images are stored

### `server.py`


## ⛏️ Built With <a name = "tech_stack"></a>

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=flat&logo=sqlite&logoColor=white)


