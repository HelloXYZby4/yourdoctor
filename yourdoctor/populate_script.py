import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourdoctor.settings')


import django
django.setup()


from yd_webapp.models import Patients


