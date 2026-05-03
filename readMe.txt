Prerequisites:
    - Python
        - version check 
            => python --version
    - webserver : uwicorn 
    - pydantic : for data validation
- Virtual environment:
    => python -m venv myenv
    => source myenv/bin/activate
    => deactivate
- Packages: after activation of virtual environment
    => pip install fastapi uvicorn
    => uvicorn main:app --reload
    
REST - Representation State Transfer
    - sending data in Representation format
        {eg:JSON}

SQL Alchemy:
    - pip install sqlalchemy
    - pip install psycopg2