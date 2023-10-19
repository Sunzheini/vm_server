# vm_server
 A django server on a virtual machine, which accepts commands and executes corresponding python scripts

1. In the office, the React Server is accessed with Google Chrome: http://localhost:3000/users, not https!
2. Add:

Add the ips below to ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
Add your IP to the field Host in Edit Configurations
Change the urls inside the react app not to 127.. but real ip in: 
loginService.js, userService.js, vmService.js, App.js (for the login)

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',          # added
    '127.0.0.1',
    '172.23.139.33',    # added my ip in the network

    '172.23.139.27',    # external ip
    '172.23.138.56',    # external ip
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Allow requests from React app during development
    "http://172.23.139.33:3000",  # Allow requests from React app during development
]

3. To run the project:


