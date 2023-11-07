# VPN-SERVICE
 Test task for interview

##Fork/Clone

Create .env in ```sh vpn_service ``` directory

```sh
SECRET_KEY=f&h7zz*#&e%xg8*(qwlqo335wfz^5%!s5aaj=)z(+jh5zyzqft
DEBUG=False
```

##Start Project
```sh
docker build -t django-app .
```

```sh
docker run -d -p 8000:8000 django-app
```

Access the application at the address [http://localhost:8000/](http://localhost:8000/)

## Accessible urls

```sh
'/'
'/login'
'/logout'
'/signup'
'/services/links'
'/profile/',
'/<link_name><link>/v'
'/<link_name>/v'
```