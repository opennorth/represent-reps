# Represent Representatives

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected officials and electoral districts. It provides a [REST API](http://represent.opennorth.ca/api/) to boundary, representative, and postcode resources.

This repository provides an API to elected officials. API documentation is available at [represent.opennorth.ca/api/](http://represent.opennorth.ca/api/#representativeset).

The [represent-canada](http://github.com/opennorth/represent-canada) repository provides a master Django project, and points to packages which add boundary, postal code, and map features.

## Configuration

Set `REPRESENTATIVES_BOUNDARYSERVICE_URL` to the base URL for a Represent Boundaries API, e.g. `http://represent.opennorth.ca/`

## Adding data

Create a representative set using the Django admin site and then run the "Update from data source" action.

## Bugs? Questions?

This project's main repository is on GitHub: [http://github.com/rhymeswithcycle/represent-reps](http://github.com/rhymeswithcycle/represent-postcodes), where your contributions and forks are greatly welcomed. Please submit bug reports, feature requests, and feedback to [represent-canada](http://github.com/opennorth/represent-canada).

Released under the MIT license
