# Easy PID Motor Controller (EPMC) Setup Application
It contains source code of the Easy PID Motor Controller (EPMC) GUI application. Without the module, only the start page can be viewed.

![Screenshot 2025-05-08 150800](https://github.com/user-attachments/assets/e54d6d61-082f-4f94-b973-b93f00fe7d40)

### Running the GUI app (Using python virtual environment)

#

#### Prequisites
- This would run on **Linux (Ubuntu)**, **Windows**, and **MAC OS**

> [!NOTE]  
> For Windows and Mac Users, ensure you have the [**`CH340 serial converter`**](https://sparks.gogo.co.nz/ch340.html?srsltid=AfmBOooJ45evOXTZdp96-_eI1A2xCokPqFyJm0e_Ybx6LOwyY0qJ5Uux) driver installed.
>
> For Ubuntu Users - the **CH340** driver is installed by default.

- Ensure you have `python3` installed on your PC and also `pip`

- install python virtual environment
  > ```shell
  > sudo apt install python3-pip   # linux or mac users
  > ```
  > ```shell
  > sudo apt install python3-virtualenv   # linux or mac users
  > ```
  > *OR*
  > ```shell
  > pip install virtualenv   # windows users (ensure you have pip installed)
  > ```
  
- Ensure you have the **`EPMC Module`** connected to the PC.

#

#### Run / Build App [ Ubuntu or Mac Users ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
  > ```shell
  > git clone https://github.com/robocre8/epmc_setup_application.git
  > ```

- change directory into the root **`epmc_setup_application`** folder
  > ```shell
  > cd epmc_setup_application/
  > ```

- create a python virtual environment named **`.env`** in the root folder
  > ```shell
  > python3 -m venv .env
  > ```

- activate the virtual environment
  > ```shell
  > source .env/bin/activate
  > ```

- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  > ```shell
  > pip3 install -r requirements.txt
  > ```

- now you can run the app in the virtual environment
  > ```shell
  > python3 app.py
  > ```

- Now follow this tutorial on [how to use the **Easy PID Motor Controller** to setup velocity PID for a DC Motor](https://robocre8.gitbook.io/robocre8/epmc-tutorials/how-to-setup-dc-motor-pid-speed-control-with-the-epmc)

- build the application with pyinstaller (optional):
  > ```shell
  > pyinstaller app.py --onefile --name epmc_app_ubuntu_<OS-version-number> --hidden-import='PIL._tkinter_finder' --noconsole
  > ```
  > OR
  > ```shell
  > pyinstaller app.py --onefile --name epmc_app_mac_<OS-version-number> --hidden-import='PIL._tkinter_finder' --noconsole
  > ```
  
- once you are done using the application, just close and deactivate the environment
  ```shell
    deactivate
  ```

#

#### Run / Build App [ Windows ]
- Download (by clicking on the green Code button above) or clone the repo into your PC using **`git clone`**
  > you can use this command if you want to clone the repo:
  >
  > ```shell
  > git clone https://github.com/robocre8/epmc_setup_application.git
  > ```

- change directory into the root **`epmc_setup_application`** folder
  > ```shell
  > cd .\epmc_setup_application\
  > ```

- create a python virtual environment named **`.env`** in the root folder
  > ```shell
  > python -m venv .env
  > ```

- activate the virtual environment
  > ```shell
  > .\.env\Scripts\Activate.ps1 # In Powershel
  > ```
  > OR
  > ```shell
  > .\.env\Scripts\activate.bat # In CMD
  > ```

- you should see now that you are in the **`.env`** virtual environment

- install all required python modules
  > ```shell
  > pip install -r requirements.txt
  > ```

- now you can run the app in the virtual environment
  > ```shell
  > python app.py
  > ```

- Now follow this tutorial on [how to use the **Easy PID Motor Controller** to setup velocity PID for a DC Motor](https://robocre8.gitbook.io/robocre8/epmc-tutorials/how-to-setup-dc-motor-pid-speed-control-with-the-epmc)

- build the application with pyinstaller:
  > ```shell
  > pyinstaller app.py --onefile --name epmc_app_windows_<OS-version-number> --hidden-import='PIL._tkinter_finder' --noconsole
  > ```
  
- once you are done using the application, just close and dectivate the environment
  > ```shell
  > deactivate
  > ```
