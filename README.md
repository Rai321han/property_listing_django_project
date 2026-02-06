cd django-property-listing

# Quick setup (option 1)
chmod +x setup.sh
./setup.sh

# Manual setup (option 2)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py import_properties sample_properties_data.csv
python manage.py runserver