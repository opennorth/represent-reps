# Represent Representatives

[Represent](https://represent.opennorth.ca/) is the open database of Canadian elected officials and electoral districts. It provides a [REST API](https://represent.opennorth.ca/api/) to boundary, representative, and postcode resources.

This repository provides an API to elected officials. API documentation is available at [represent.opennorth.ca/api/](https://represent.opennorth.ca/api/#representativeset).

The [represent-canada](https://github.com/opennorth/represent-canada) repository provides a master Django project, and points to packages which add boundary, postal code, and map features.

## Configuration

Set `REPRESENTATIVES_BOUNDARYSERVICE_URL` to the base URL for a Represent Boundaries API, e.g. `https://represent.opennorth.ca/`

## Adding data

Create a representative set using the Django admin site and then run the "Update from data source" action.

## Bugs? Questions?

This project's main repository is on GitHub: [https://github.com/rhymeswithcycle/represent-reps](https://github.com/rhymeswithcycle/represent-postcodes), where your contributions and forks are greatly welcomed. Please submit bug reports, feature requests, and feedback to [represent-canada](https://github.com/opennorth/represent-canada).

Released under the MIT license
