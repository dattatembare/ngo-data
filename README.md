# Project
This project could be used as a base project or template to start new project. It has 3 basic features, project config implementation,
Logging & decorators and Unit test launcher to run all unit tests in one shot.    
 
## Logging and decorators:
The logger implementation is based on standard logging module, with basic logging there are 3 decorators provided.

## Logging Features: 
* When `{time}` placeholder provided in logfile name then every run will generate the new log file with timestamp.
When `{time}` is not provided then logger functionality will work as usual.
* Custom log levels - Example provided to create the custom log levels. In this project `trace` and `perf` (performance)
log levels created.
* Handled double logging issue.

## Decorators: 
* trace - When trace decorator used on function, logs will be printed at start and end of the method call.
* timer - When timer decorator used on function, logs will be printed at start and end of the method call, with that method 
performance timings will be printed.
* exception - When exception decorator used on function, and when method will throw an exception, error message will be 
will be printed in error log file. Only read functionality implemented in this project, for write functionality check the documentation.

## Config:
INI style configs (using ConfigParser). ConfigParser helps to read and write .ini config file.

## Unit test Launcher:
Executes all unit tests (when module name start with `test_`) and generates text or html report.
To generate html report need to use `-r html` when running from commandline.

Command: `python -m test.unit_test_launcher -r html`

---------------------------------------------------------------------------------------------------------------

 # Run Application
    pip install -r requirements.txt
    
    ngo-data> python download_ngo.py
 