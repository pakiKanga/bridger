
# Bridger
Required Use Cases:
* Find relevant subjects for a student
* Sell textbooks
* Buy textbooks

## Requirements
First, ensure you have virtualenv installed. This will be used to isolate the python environment and have consistency amongst all members. The project uses Python 3. For initial setup, do the following.

```
cd <bridger-location> //Where all the files and folders are
virtualenv venv
pip install -r requirements.txt
```

## Running

How to run the server.

If you're on a UNIX OS, run:
```
source venv\bin\activate
```
If you're on a Windows OS, run:
```
venv\Scripts\activate
```
----
Finally, run:
```
python manage.py runserver
```

To stop the server:
```
ctrl+c
deactivate
```
Remember to always reactivate virtualenv before running the application.

## Important Files and Folders
 - templates
	 - Contains all the html files.
- static
	- Contains all the css, js and media.
- views.py
	- Contains all the back-end code for each module and renders the relevant HTML contents.
