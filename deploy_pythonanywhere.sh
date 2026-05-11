#!/bin/bash
# Quick deployment script for PythonAnywhere
# Usage: bash deploy_pythonanywhere.sh yourusername

if [ -z "$1" ]; then
    echo "Usage: bash deploy_pythonanywhere.sh yourusername"
    echo "Example: bash deploy_pythonanywhere.sh tarekaloui066"
    exit 1
fi

USERNAME=$1
PROJECT_DIR="/home/$USERNAME/bloodconnect"
VENV_NAME="bloodconnect"

echo "🚀 Deploying BloodConnect to PythonAnywhere..."
echo "Username: $USERNAME"
echo "Project: $PROJECT_DIR"
echo ""

# Step 1: Clone repository
echo "📥 Step 1: Cloning repository..."
cd /home/$USERNAME
git clone https://github.com/tarekaloui066-cloud/bloodconnect.git || echo "Repository already exists"

# Step 2: Navigate to project
cd $PROJECT_DIR

# Step 3: Create and activate virtual environment
echo "🐍 Step 2: Setting up virtual environment..."
mkvirtualenv --python=/usr/bin/python3.11 $VENV_NAME 2>/dev/null || true
workon $VENV_NAME

# Step 4: Install dependencies
echo "📦 Step 3: Installing dependencies..."
pip install -r requirements.txt

# Step 5: Collect static files
echo "📁 Step 4: Collecting static files..."
python manage.py collectstatic --noinput

# Step 6: Run migrations
echo "🗄️  Step 5: Running migrations..."
python manage.py migrate

# Step 7: Information
echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "⚠️  NEXT STEPS IN PYTHONANYWHERE WEB TAB:"
echo "1. Add new web app"
echo "2. Choose 'Manual configuration' and Python 3.11"
echo "3. Update WSGI file with content from wsgi_production.py"
echo "4. Set PYTHONHOME and PYTHONPATH:"
echo "   PYTHONHOME=/home/$USERNAME/.virtualenvs/$VENV_NAME"
echo "5. Source code: $PROJECT_DIR"
echo "6. Update ALLOWED_HOSTS in settings.py"
echo "7. Click Reload"
echo ""
echo "📝 Update ALLOWED_HOSTS in: $PROJECT_DIR/bloodconnect/settings.py"
echo "ALLOWED_HOSTS = ['${USERNAME}.pythonanywhere.com']"
echo ""
echo "🔗 Visit: https://${USERNAME}.pythonanywhere.com"
