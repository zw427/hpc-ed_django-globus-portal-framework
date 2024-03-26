import logging
from django.conf import settings
from provider.models import Provider

log = logging.getLogger(__name__)


def lookup_replace_provider_id(facets: dict) -> dict:
    """Replace all values within the Provider_ID with nice names from
    the lookup table above"""
    for facet in facets:
        if facet["field_name"] == "Provider_ID":
            for bucket in facet["buckets"]:
                try:
                    bucket["custom_display_value"] = Provider.objects.get(Provider_ID=bucket["value"]).Provider_Name
                except Provider.DoesNotExist:
                    log.warning(f"Provider {bucket['value']} is unknown and needs to be "
                                "added to the database!")
                    bucket["custom_display_value"] = "Other"
    return facets
