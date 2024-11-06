# Easy PID Motor Controller (EPMC) Setup Application
It contains source code of the Easy PID Motor Controller (EPMC) GUI application. The application requires that you have the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**) is connected to your PC. Without the module, only the start page can be viewed.

## Running the GUI app (Using python virtual environment)
### Prequisite
- This should run on linux (ubuntu), windows, and MAC

> [!NOTE]  
> For Windows and Mac Users, ensure you have the **`CH340 serial converter`** or the **`FTDI`** driver installed. (depending on the module you are using)

- Ensure you have `python3` installed on your PC and also `pip`

- install python virtual environment
  ```shell
    pip3 install virtualenv   //linux or mac
  ```
  ```shell
    pip install virtualenv   //windows
  ```
- Ensure you have the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**) interfaced with the geared dc motors and connected to the PC.




#### Run App First Time [ linux or mac ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
	>  ```git clone https://github.com/samuko-things-company/epmc_setup_application.git```

- change directory into the root **`epmc_setup_application`** folder

- create a python virtual environment named **`.env`** in the root folder 
  ```shell
    python3 -m venv .env
  ```
- activate the virtual environment
  ```shell
    source .env/bin/activate
  ```
- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  ```shell
    pip3 install -r requirements.txt
  ```
- now you can run the app [follow the [blog tutorial]() on how to setup the PID of the Motor(s) connected to the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**)]
  ```shell
    python3 app.py 
  ```
- build the application with pyinstaller:
  ```shell
    pyinstaller app.py --onefile --icon epmc_icon.ico --name epmc_app
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

#### Run App [ linux or mac ]
- change directory into the root **`epmc_setup_application`** folder

- activate the virtual environment
  ```shell
    source .env/bin/activate
  ```
- you should see now that you are in the **`.env`** virtual environment

- now you can run the app [follow the [blog tutorial]() on how to setup the PID of the Motor(s) connected to the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**)]
  ```shell
    python3 app.py 
  ```
- build the application with pyinstaller:
  ```shell
    pyinstaller app.py --onefile --icon epmc_icon.ico --name epmc_app
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

#

#### Run App First Time [ Windows ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
	>  ```git clone https://github.com/samuko-things-company/epmc_setup_application.git```

- change directory into the root **`epmc_setup_application`** folder

- create a python virtual environment named **`.env`** in the root folder 
	```shell
    python3 -m venv .env
  ```
- activate the virtual environment
  ```shell
    env/Scripts/activate.bat //In CMD  or
    env/Scripts/Activate.ps1 //In Powershel
  ```
- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  ```shell
    pip install -r requirements.txt
  ```
- now you can run the app [follow the [blog tutorial]() on how to setup the PID of the Motor(s) connected to the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**)]
  ```shell
    python app.py 
  ```
- build the application with pyinstaller:
  ```shell
    pyinstaller app.py --onefile --icon epmc_icon.ico --name epmc_app
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```

#### Run App [ Windows ]
- change directory into the root folder **`epmc_setup_application`**

- activate the virtual environment
  ```shell
    env/Scripts/activate.bat //In CMD   or
    env/Scripts/Activate.ps1 //In Powershel
  ```
- you should see now that you are in the **`.env`** virtual environment

- now you can run the app [follow the [blog tutorial]() on how to setup the PID of the Motor(s) connected to the **`L298N EPMC MODULE`** (or a **`CUSTOM EPMC INTERFACE BOARD`**)]
  ```shell
    python app.py 
  ```
- build the application with pyinstaller:
  ```shell
    pyinstaller app.py --onefile --icon epmc_icon.ico --name epmc_app
  ```
- once you are done using the application, just close and dectivate the environment
  ```shell
    deactivate
  ```