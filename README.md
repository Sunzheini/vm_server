## Virtual Machine Control REST Server

# Functionalities
This is a project created with Django Framework in Pycharm IDE.

A django server on a special LabNet pc, which accepts commands both ways:
1. By using the React frontend;
2. By using the provided endpoints (check put the urls.py files).

It has the following functionalities:
1. Providing a Login functionality;
2. Accepting command to control virtual machines installed on the same pc, where
this server is hosted;
3. Accepting uploaded python scripts, which can be then executed on the same
pc, where this server is hosted;
4. You can add and edit (POST/PUT, in postman: body --> raw --> JSON) like this:
"""
{
"username":"Daniel Zorov",
"password":"1",
"is_admin": false
}
"""
5. You can use the following commands in the terminal if you wish to debug working with the vm:
source: https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-controlvm.html
VBoxManage startvm VM000180                      starts - working
VBoxManage controlvm VM000180 poweroff           hard poweroff - working
VBoxManage controlvm VM000180 acpipowerbutton    soft poweroff with ACPI - not working
VBoxManage controlvm VM000180 savestate          save state - working
"""
Currently the project uses savestate when closing the vm.


# Environment variables
In terminal: pip install python-decouple
In settings.py: from decouple import config, Csv
Add the needed variables
Create a dir 'env' in the main dir and a file inside called '.env'
point the path in Edit Configurations -> Path to ".env" files like this:
`C:/Appl/Projects/Python/1350-FBW_lab_pc_rest_api_server_backend/envs/.env`
and add the needed variables


# Running the project
1. Install Oracle VirtualBox and add its installation directory to the PATH variable
2. Open cmd: pip install pywin32 and pip install virtualbox with admin
rights. Install Oracle Virtual Box in Appl.
3. Install sdk using this guide:
https://pypi.org/project/virtualbox/#:~:text=Go%20to%20VirtualBox's%20downloads%20page,install%20using%20your%20system%20Python.
Note: use the C:/Appl directory to put the downloaded sdk and then install
as per the guide. If you are having issues from Python dir: \Lib\site-packages
delete python-certifi-win32-init.pth and distutils-precedence.pth.
4. Download a windows image:
a) Windows 11 from the official Microsoft website:
https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/
b) Or Windows 10 from the FTP server:
file://festo.net/DFS05/DE/Data/Berkheim/VT/ORG_EA/PD_EA/07_Software/Windows_10/
5. Use the image to make a virtual machine in Oracle VirtualBox.
a) the recommended settings for the VMs: ram16, chipset ICH9, pointing 
device mouse, enable io apic, processors 6, enable pae/nx.
b) bridged adapter (test the internet: should be working home). With NAT it shows
as if it has internet access, however zscaler is not allowing anything.
c) shut down the VM.
6. Create a shared folder: Settings of the VM --> Shared Folders -->
Select C:/Temp --> Select: Auto-Mount --> Ok. create a folder server_code inside Temp and there
put the services folder from this project.
7. Start the VM. In cmd run:
d) download and install python;
f) download and install VS Code / Notepad++ in the VM. Inside VS Code install
python (from microsoft);
a) python.exe -m pip install --upgrade pip;
b) pip install flask;
c) pip install psutil
d) Control Panel --> Windows Defender Firewall --> disable both;
e) Network and internet settings --> Sharing options -->
Network discovery should be on.

Check if the Temp folder is seen. Copy the server_code folder to the desktop. Now
using task scheduler create a task to start service_manager.py immediately after login:

Create Task --> Name: python_service_manager, Run with the highest privileges -->
Configure for: Windows 10 --> Triggers --> New -->
Begin the task: At log on --> --> Actions --> New --> 
Program/script: browse and select pythonw.exe as the program --> 
"Add arguments" field, specify the path to the service_manager.py (e.g., "C:\path\to\service_manager.py") -->
Conditions --> Uncheck: Start the task if only the computer is on AC power --> Ok;

Restart.

8. The service should be starting automatically and each 5 sec should open cmd.exe, notepad++ and Flask server.
9. Change the network settings inside the VM to match the network of the pc. This 
will disable the internet access, but will enable pinging between the 2 machines. The pc on festo wifi 
was: 179.23.139.26 and I changed the ip of the vm to 179.23.139.29 and subnet mask to 255.255.254.0
and it worked
10. Now test the ping. Home it is a ping between 192.168.0.102 and 192.168.0.107 (which is obtained
automatically by the vm).

11. The virtual machine can have the option to be accessed remotely by:
a) Installing the Oracle VM Extension Pack; 
b) Go to the settings of the virtual machine --> Display --> Remote Display and check Enable server. You can
see the port there.

12. Create a VENV and install the dependencies from the requirements.txt file;
13. Examine the contents in setting.py and adjust as see fit to your settings;
14. Run the server with `python manage.py runserver or by Pycharm IDE;
15. The server is hosted on http://localhost:8000/;
16. For the VMS: Have the Oracle software already running, the recommended settings for the VMs:
ram16, chipset ICH9, pointing device mouse, enable io apic, processors 6, enable pae/nx.


# Structure
1. The project is divided into several apps, which provide unique functionalities: login, control
of virtual machines and execution of python scripts, respectively;
2. The controllers folder must provide the logic for the factual control of the 
virtual machines using `virtualbox` and the execution of python scripts using `python3`;
3. The core folder contains the decorators for control of method execution: timing, logging, etc.. Also
the main engine class which connects the controllers with the views. The views are made abstract,
combining the common logic into the view_templates.py file;
4. The media_files folder contains the uploaded python scripts;
5. Then each one of the apps is structured as per the Django principles: models, views, urls, etc.;
