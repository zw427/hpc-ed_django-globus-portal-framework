export APP_CONFIG='dgpf1/local_settings.py'
python dgpf1/manage.py migrate
python dgpf1/manage.py loaddata initial_providers
python dgpf1/manage.py runserver