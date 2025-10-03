# Forms Demo

This is a demo project for using forms in Flask applications.

## Running

- Set up a Python virtual environment
  - `python -m venv venv`
  - `venv\scripts\activate`
- Install project dependencies
  - `pip install -r requirements.txt`
- Create your `.env` file
- Run the app with `flask run`

## Developing Your Own Version

To develop your own version of this project, you can `clone` or `fork` this repo.

- `git clone <repo url>` makes a copy of the repo, but still considers the upstream (parent) repo to be this repo. This is fine for development and testing, but the remote repo still belongs to me.
- Forking the repo makes a copy of the repo on _your_ GitHub account, meaning that you have full control of it from that point forward. This is the better approach when you want to make your own version of an existing project, as opposed to contributing to the original one.

## Branches

- `main`: Includes all the regular demo code, with a profile page and matching results page.
- `HistoryPage`: Adds a page to show all (in-memory) submissions to the profile form.
- `WTForms`: Adds integration for the [WTForms](https://wtforms.readthedocs.io/en/3.2.x/) library (via [Flask_WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)) for more powerful validation and input widgets.
