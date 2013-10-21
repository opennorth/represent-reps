# Represent API: Representatives

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected representatives and electoral districts. It provides a RESTful API to boundary, representative, and postcode resources.

This repository provides an API to elected officials. It depends on [represent-boundaries](http://github.com/rhymeswithcycle/represent-boundaries). It expects source data to be available at a provided URL, formatted as a JSON array -- for example, from [ScraperWiki](http://scraperwiki.com/).

The [represent-canada](http://github.com/opennorth/represent-canada) repository provides a full sample app.

API documentation is available at [represent.opennorth.ca/api/](http://represent.opennorth.ca/api/#representativeset).

## Configuration

Set `REPRESENTATIVES_BOUNDARYSERVICE_URL` to the base URL for a Represent boundaries API, e.g. `http://represent.opennorth.ca/`

## Adding data

Create a representative set using the Django admin. (See Django docs for how to set that up.)

Then, from the representative sets list in the admin, check the set you just created and choose the Update from ScraperWiki action.

This will pull from the linked scraper and creative Representative objects, which you can then check in the Django admin.

For more information on the format expected from scrapers, see the Represent [documentation](http://represent.opennorth.ca/api/#representative).

## Contact

Please use [GitHub Issues](http://github.com/opennorth/represent-canada/issues) for bug reports. You can also contact represent@opennorth.ca.