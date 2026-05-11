# PythonAnywhere Deployment Guide for BloodConnect

## Step 1: PythonAnywhere Account Setup
1. Go to https://www.pythonanywhere.com
2. Sign up for a free or paid account
3. Your web domain will be: `yourusername.pythonanywhere.com`

## Step 2: Clone Your GitHub Repository
1. Open a new bash console in PythonAnywhere
2. Run these commands:

```bash
cd /home/yourusername
git clone https://github.com/tarekaloui066-cloud/bloodconnect.git
cd bloodconnect
```

## Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.11 bloodconnect
pip install -r requirements.txt
```

## Step 4: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Step 5: Configure Django Settings for Production
1. In Web tab, create new web app
2. Choose "Manual configuration"
3. Choose Python 3.11

## Step 6: Update WSGI Configuration
1. In the Web tab, edit WSGI configuration file
2. Replace the contents with the code from `wsgi_production.py`

## Step 7: Configure Allowed Hosts
Update `bloodconnect/settings.py`:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
```

## Step 8: Set Up Database
```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py loaddata fixtures/initial_data.json
```

## Step 9: Reload Web App
1. Go to PythonAnywhere Web tab
2. Click "Reload yourusername.pythonanywhere.com"

## Important Security Notes
- Change DEBUG to False in production
- Use environment variables for SECRET_KEY
- Set ALLOWED_HOSTS correctly
- Use HTTPS only

## Testing
Visit: `https://yourusername.pythonanywhere.com`
Admin: `https://yourusername.pythonanywhere.com/admin/`

## Troubleshooting
- Check error logs in PythonAnywhere Web tab
- Use `python manage.py check` to verify settings
- Review server log in Files tab
