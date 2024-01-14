#Arranca la aplicacion#Si este proyecto se ejecuta como archivo principal ($python app.py)
from app import app
from models.SharedModels import db

#Creara todas las tablas. 
with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug = True) #con debug=True autocarga los cambios. 