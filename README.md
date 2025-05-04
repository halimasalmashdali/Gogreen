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
            tree_icon.png
            ...
        Poppins-SemiBold.ttf
    cache/
         ...
    screens/
            home_screen.kv
            leaderboard_screen.kv
            login_screen.kv
            map_screen.kv
            profile_screen.kv
            reg_screen.kv
            treetracker_screen.kv
            welcome_screen.kv

    .gitignore
    GoGreen.db
    main.py
    README.md
    requirements.txt
    users_test_db.py
```

## Getting Started

To run the GoGreen app locally, follow these steps:

1. Clone the repository:

   ```bash
   https://github.com/halimasalmashdali/Gogreen.git
   ```

2. Install the required dependencies:
   - First create Virtual Environment:
      ``` bash
      python -m venv venv
   - Download all requirements 
      ```bash
      pip install -r requirements.txt
     
3. Download Kivy Garden:
   
      - Run these commands on your terminal
     ``` bash
   pip install kivy_garden.mapview
   garden install mapview
     ```
4. Run the app
   - Run the main.py to create database and start using the app
   ```bash
   main.py
   ```

The app widget should automatically open in your screen
6. Create test users and trees if needed
   - Run the users_test_db.py to get random users with random amount of trees registered
   ```bash
   users_test_db.py 
   ```


## Features

- **User Authentication:** Secure user registration and login with password.
- **Dynamic Challenges List:** Automatically updates the chellenges list with new messages.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.

## Project Architecture

### `main.py`

Holds all screen actions and connections
Entry point for running the server. Initializes the Kivy app and database communication events.

### `assets/`

Directory where all photos and fonts used in app are saved.
### `GoGreen.db`

Database file. Saves registration information for both users and trees in separate tables

### `screens/`

Directory in which all Kivy code is written.

### `cache/`

Directory where the map photos are saved. Directory is created automatically


## ⛏️ Built With <a name = "tech_stack"></a>

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=flat&logo=sqlite&logoColor=white)


