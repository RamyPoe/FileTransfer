#### Allows User to transfer files over any network

___

## Installation and Setup Instructions

Clone down this repository. Tested on `Windows 10` . Setup instructions will be for `Windows 10`. Make sure dependency `glob2` is installed via `pip`; alternatively use the compiled executable.

#### Send/Client

Place the files which you want to send in the `send` folder. To send a directory, make sure it is zipped. 
Server IP will be requested via console. Runs on PORT `6437`.

#### Receive/Server

Run the `client.py`/`receive.exe` file and the server IP will be shared in the console.
When all the files have been received, you will be notified in the console. The files can be found in the `recv` directory.


## Reflection

 - Application of a simple buffer system
   - Allows you to send files of 2GB (hasn't been tested with anything more)
 - Use of TCP sockets in Python
 - Use of threading for animated console output
 - Reading and writing of files to/from the OS
