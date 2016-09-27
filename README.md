Food Compass
---------------------------------------------
App that helps you decide where you and your buddies should go eat

Features -
    a. Add and review restaurants
    b. Create polls and submit votes

SETUP -
Virtual env is recommended!

1. `pip install -Ur requirements.txt`
2. `npm install`
3. `npm run build`
4. `python manage.py createsuperuser` - create a super user
5. `python manage.py runserver`


Quick Tutorial -
1. `Go to http://127.0.0.1:8000/app/` or `Go to http://localhost/app/` - depending on your dev environment
2. `Login with the super user to get started on creating restaurants` - restaurants can be submitted by staff users
3. `Post a couple of reviews`
4. `Create a poll and add restaurants as choice`
5. `Submit votes on the homepage`
6. `Log out of the super user and register a non-admin user from http://127.0.0.1:8000/app/ or http://localhost/app/`
7. Play around with the non-admin user!

Contribution/Credits - token-based Authentication with React and DRF (Token Authentication Login - React basic setup forked from - https://github.com/geezhawk/django-react-auth)
