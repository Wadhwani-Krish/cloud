# Login Page
Required Libraries to Install OAuth:
sh
pip install authlib request
Set Up Google OAuth Client:
Go to Google Cloud Console.
Navigate to APIs and Services ⇒ Credentials.
Create Credentials ⇒ OAuth 2.0 Client ID.
Add Redirect URIs (your callback function).
Copy Google Client ID and Secret and save them as environment variables.
Cloning the Project from GitHub to VM Instance in GCP:
Install necessary packages:
sh
sudo apt install python3-pip python3-venv git mysql-client -y
Clone the repository:
sh
git clone https://github.com/Git-hub-ID/repo.git
Install dependencies:
sh
pip install -r requirements.txt
Set up environment variables:
sh
touch .env
nano .env
(Copy and paste the environment variables)
Set Up MySQL Database:
Start MySQL:
sh
sudo systemctl start mysql
Secure MySQL installation:
sh
sudo mysql_secure_installation
Log into MySQL and create a database:
sh
mysql -u root -p
CREATE DATABASE Db_Name;
FLUSH PRIVILEGES;
Initialize the database:
sh
flask app modelEarth_login init-db
