Token-based Authentication with React and DRF
---------------------------------------------
This is an example project for [my tutorial on authenticating users with React and Django](http://geezhawk.github.io/user-authentication-with-react-and-django-rest-framework). To test it out yourself, clone the repository and run:

Virtual env is recommended

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
