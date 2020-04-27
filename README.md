# Cmuxovik v1.2 (work in progress)

## What is Cmuxovik?

Cmuxovik is a web app allowing users to share funny short sentences _("cmuxes", from Russian "стих" [stih] — verse)_ which follow a certain logic. Examples of cmuxes (currently Russian only):

- целый час олень и я кушали соления
- поднял прокурор про кур ор
- пандемия: теперь панд ем и я
- ведь мы ведьмы
- промежуток промеж уток
- etc.


## Tech used

The app is built using the following stack:

- Django
- PostgreSQL
- Nginx
- Docker


## Running the app locally

1. Make sure [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) are installed. 
1. Clone the repository, `cd` into its root directory.
1. Find the file `.env.dev.example` in the root directory, copy it into `.env.dev`
1. Inside the `.env.dev` file:
    1. Add a `SECRET_KEY`. You can generate one by running: 
    
        ```python -c 'import os; print(os.urandom(24).hex())'```
    
    2. Add your GMail credentials into `EMAIL_USER` and `EMAIL_PASS` to test the "Forgot Password" functionality.  
    3. (optional) Change the `DJANGO_SUPERUSER_*` parameters to your taste. The superuser with these parameters will be created automatically.
1. To launch containers with the app, run `docker-compose up -d`
1. Open the app at [localhost:8000](http://localhost:8000)
    1. To give your user moderator permissions (i.e. confirm/edit/delete cmuxes), go to the admin panel, select your user in the Authors model, tick the "is moderator" checkbox, and save.  
1. To stop the containers, run `docker-compose down -v`. The data is not persisted between runs.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)