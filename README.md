# HPC-ED Django Globus Portal Framework 1

HPC-ED Customized Django Globus Portal Framework 1

Used in https://search-pilot.operations.access-ci.org

### Development

For local development, install dependencies using `pipenv`:

```
pipenv install
```

**Note**: The psychopg2 lib isn't needed for local testing. It's also suggested to swap the database in settings.py to sqlite3 when testing.

Create a local settings file, such as `local_settings.py` with the following:

```
{
    "DJANGO_SECRET_KEY": "insecure-test-key",
    "DEBUG": true,
    "ALLOWED_HOSTS": ["*"],
    "STATIC_FILES": null,
    "STATIC_ROOT": null,
    "SOCIAL_AUTH_GLOBUS_KEY": "",
    "SOCIAL_AUTH_GLOBUS_SECRET": ""
}
```

And assign it to your env with: 

```
export APP_CONFIG=local_settings.py
```