"""
* Requires library pytest-django (pip install pytest-django)
* Also requires an env for the settings file: DJANGO_SETTINGS_MODULE=dgpf1.settings
    This should probably be configured in setup.cfg, or Pipfile if supported

Run with:
pytest dgpf1/tests.py

"""
import pytest
from django.core.management import call_command
from dgpf1 import facet_modifiers

# Populate the database for this entire test session, with initial provider data.
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'initial_providers.json')


@pytest.mark.django_db
def test_facet_modifiers_lookup_known_provider_id():
    facets = [
        {
            "field_name": "Provider_ID",
            "buckets": [{"value": "urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:897"}]
        }
    ]
    updated_facets = facet_modifiers.lookup_replace_provider_id(facets)
    assert updated_facets[0]["buckets"][0]["custom_display_value"] == "Linked In"


@pytest.mark.django_db
def test_facet_modifiers_lookup_unknown_provider_id():
    facets = [
        {
            "field_name": "Provider_ID",
            "buckets": [{"value": "does_not_exist"}]
        }
    ]
    updated_facets = facet_modifiers.lookup_replace_provider_id(facets)
    assert updated_facets[0]["buckets"][0]["custom_display_value"] == "Other"
