**Setup config.py file with correct credentails**

**Use windows task scheduler to run main.py everyday**

Folder core contains necessary functions.

main.py gets all csv files from given source folder (from config.py) and loads them to sql server.
While loading transferred rows/files will be shown in the terminal

use requirements.txt for necessary modules

Explaining in details:
1. Windows Task Scheduler
To create a task with basic settings on Windows 10, use these steps:
  1. Open start
  2. Search Task Scheduler, and click Windows Task Scheduler
     
  ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/ccf78998-8742-47ad-acb7-6d9c280723ef)
  
  4. Click new task
  
  ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/0b50ceb5-c9f3-4408-83c6-1d82b36c4fe5)
  
  5. Write name and optional description
  
  ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/ae1451d0-5791-4f29-84e6-e2774da8f650)
  
  6. Move to triggers and click create new. And adjust start time and choose appropriate schedule.
     Tip: also tick terminating task if it is running for a long time
  
  ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/44e7c3f5-ae13-4b2c-a4cd-42fde5c9af5f)
  
  7. Move to actions. Choose execute program, browse and select your file.
  
  ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/8c1b7a83-0353-4ab7-9bb6-d9e5c2a42a5b)
  
  8. Click ok. Done
  
     ![image](https://github.com/futurelider01/Sample-ETL-process/assets/146430607/69cd3981-efa9-4364-b23f-903eba2e21ed)



2. Main function:
  1. main function get source either folder containging files or can get certain csv files from given source (just need to write path)
  2. function check it size if it is larger than 5MB than it call chunking method of ingesting, otherwise it call just ingest method (ingests at once)
  3. Every loading will logged and if it fails it will send email to admin reporting about failure specifying table and error occured. If sending email also fails, it will be logged to monitoring in the worst case.
  4. Everyday it will create monitoring_(executed date).csv and will write all information about ETL process: how much time spent, how much rows transferred, which file is loading to which table.

3. About .env
  1. Create ssms login, password, server name, database name.
  2. Create sender email and login, and reciever,
