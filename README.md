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
If you're on a UNIX OS, run:
```
source venv\bin\activate
```
If you're on a Windows OS, run:
```
venv\Scripts\activate
```
## Running

Run the server.

```
python manage.py runserver
```
