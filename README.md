## ⚙️ Installation & Setup

Follow the steps below to run this project locally:

```bash
# Clone the repository
git clone https://github.com/rahul9561/ERP-Inventory-Sales-Management-System.git

# Navigate into the project
cd ERP-Inventory-Sales-Management-System

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r ERP/requirements.txt

# Run migrations
python ERP/manage.py makemigrations
python ERP/manage.py migrate

# Create superuser
python ERP/manage.py createsuperuser

# Run server
python ERP/manage.py runserver
