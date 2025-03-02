# Login Page
Required Libraries to Install OAuth:

pip install authlib request

Set Up Google OAuth Client:

 1. Go to Google Cloud Console.
 2. Navigate to APIs and Services ⇒ Credentials.
 3. Create Credentials ⇒ OAuth 2.0 Client ID.
 4. Add Redirect URIs (your callback function).
 5. Copy Google Client ID and Secret and save them as environment variables.

Cloning the Project from GitHub to VM Instance in GCP:

 1. Install necessary packages:
    sudo apt install python3-pip python3-venv git mysql-client -y
 2. Clone the repository:
    git clone https://github.com/Git-hub-ID/repo.git
 3. Install dependencies:
    pip install -r requirements.txt
 4. Set up environment variables:
    touch .env
    nano .env
    (Copy and paste the environment variables)  

example of .env file:

secret_key=
host=
database_URL=
MySQL_password=
MySQL_user=
MySQL_database=
email_pass=
email_id=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
    
Set Up MySQL Database:

 1. Start MySQL:
    sudo systemctl start mysql
 2. Secure MySQL installation:
    sudo mysql_secure_installation
 3. Log into MySQL and create a database:
    mysql -u root -p
    CREATE DATABASE Db_Name;
    FLUSH PRIVILEGES;
 4. Initialize the database:
    flask app modelEarth_login init-db
