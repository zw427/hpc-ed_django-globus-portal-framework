import logging
from django.conf import settings

log = logging.getLogger(__name__)


def __lookup_provider_name(provider_id: str) -> str:
    for provider in settings.AVAILABLE_PROVIDERS:
        if provider["id"] == provider_id:
            return provider["name"]
    log.warning(f"Provider {provider_id} is unknown and needs to be "
                "configured in settings.AVAILABLE_PROVIDERS!")
    return "Other"


def lookup_replace_provider_id(facets: dict) -> dict:
    """Replace all values within the Provider_ID with nice names from
    the lookup table above"""
    for facet in facets:
        if facet["field_name"] == "Provider_ID":
            for bucket in facet["buckets"]:
                bucket["value"] = __lookup_provider_name(bucket["value"])
    return facets
