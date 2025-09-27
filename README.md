# Best Harry Potter site ever!

## Application Architecture

The application consists of the following subsystems:
- API for working with the local database  
- RESTful API for accessing the local database API  
- Web application  

## Running the Application

To run the application, you need to start the RESTful API service for accessing the local database and then the web application.

To start the service, run the following commands:
```sh
cd app\web_api
python api.py
```
To start the web application, run the following commands:
```sh
cd app\web_app
python main.py
```

After executing these commands, the web application interface will be available at http://localhost:8080/.

## Data Sources

## WizardWorldAPI

API returning data from the Harry Potter universe.


https://wizard-world-api.herokuapp.com/swagger/index.html





## Архитектура приложения

Приложение состоит из следующих подсистем:
- API для работы с локальной базой данных;
- RESTful API для доступа к API локальной базы данных;
- веб приложение.

## Запуск приложения

Для запуска приложения необходимо запустить сервис с RESTful API для доступа к локальной базе данных и веб приложение.

Для запуска сервиса необходимо выполнить следующие команды:
```sh
cd app\web_api
python api.py
```

Для запуска веб приложения необходимо выполнить следующие команды:
```sh
cd app\web_app
python main.py
```

После выполнения указанных команд интерфейс веб приложения будет доступен по адресу http://localhost:8080/.

## Источники данных

### WizardWorldAPI

API returning data from the Harry Potter universe.


https://wizard-world-api.herokuapp.com/swagger/index.html
