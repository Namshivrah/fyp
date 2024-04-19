# utils.py

def set_database_for_region(region):
    # Define a mapping between regions and database aliases
    region_to_database = {
        'default': 'default',
        'central': 'one',
        'eastern': 'two',
        'western': 'three',
        'northern': 'four',
    }

    # Validate that the provided region is in the mapping
    if region not in region_to_database:
        # Handle the case when the region is not recognized
        raise ValueError(f"Invalid region: {region}")

    # Use Django's `using` attribute to set the database alias for the request
    database_alias = region_to_database[region]
    return database_alias
