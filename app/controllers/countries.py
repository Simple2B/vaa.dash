import pycountry


def country_choices():
    country_name = [country.name for country in pycountry.countries]
    return country_name
