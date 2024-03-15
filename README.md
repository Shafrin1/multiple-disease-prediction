# Multiple-disease-prediction
Nehru college B.Tech 2024

1. Python version =  3.11.8

2. The requirements file is attached in the folder.To install the requirements follow this command,
    pip install -r requirements.txt


3. code for updating the database

  * After deleting the db file from instance folder, type this code in the vs code terminal.

  >>>  python
  >>>  from heart_prob import db
  >>>  from heart_prob.models import db
  >>>  db.create_all()
  >>>  from heart_prob.models import registration
  >>>  obj=registration(email="admin@gmail.com",password="admin",usertype="admin")
  >>>  db.session.add(obj)
  >>>  db.session.commit()
  >>>  exit()
