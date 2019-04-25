# Inventory Management

A python module to help manage inventory in TOTVS ERP

#### Setup the project:

To properly setup, it's necessary to create a INI 
file named `app_config.ini` with structure like 
the one presented bellow:

````ini
[ERP_SERVER]
driver = name of the driver, like: SQL Server
server = pointer to the server, like: db.domain.com
database = standard database
uid = user identification
pwd = password
````

After that, just click in `run_app.bat`  
Author: Arnold Souza (arnoldporto@gmail.com), 2018
