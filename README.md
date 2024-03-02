To run the service (in a windows environment):
 - create a virtual environment (python -m venv venv)
 - install the required libraries referenced in requirements.txt (pip install -r requirements.txt)
 - activate the virtual environment (venv\scripts\activate)
 - run the server (uvicorn main:app)

From Postman or browser use the following calls 
http://127.0.0.1:8000/store/?url=https://www.yahoo.com	-> to input information (will return the id)
http://127.0.0.1:8000/redirect/?id=a	-> to redirect to a specific id
http://127.0.0.1:8000/statistics	-> to get the statistics
http://127.0.0.1:8000/get_title?id=a	-> to get the url title

