Required Libreries to install OAuth:
pip install authlib request

Set up Google OAUth client:
Google counsel ⇒ APIs and service ⇒ Credential ⇒ Create Credentials ⇒ OAuth 2.0 Client ID 
Add Redirect URIs (your callback function) 

copy Google clint ID and Secret save it as enviorment veriable.

Cloning the project from github to vm instance in GCP:
1. sudo apt install python3-pip python3-venv git mysql-client -y
2. git clone https://github.com/Git-hub-ID/repo.git
3. pip install -r requirements.txt (to install dependencies)
4. touch .env → nano .env (copy and past the environment variables)
5. Set up MySQL database: sudo systemctl start mysql → sudo mysql_secure_instrallation → mysql -u root -p → CREATE DATABASE Db_Name; → FLUSH PREVILEGES;
6. flask app modelEarth_login init-db (to initialize the database)



