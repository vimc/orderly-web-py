# orderly-web-py

[![Build Status](https://travis-ci.com/vimc/orderly-web-py.svg?branch=master)](https://travis-ci.com/vimc/orderly-web-py)
[![codecov.io](https://codecov.io/github/vimc/orderly-web-py/coverage.svg?branch=master)](https://codecov.io/github/vimc/orderly-web-py?branch=master)

Python client for [OrderlyWeb](https://github.com/vimc/orderly-web). 

Initial use case is to run a report only. 

## Usage

Instantiate the `OrderlyWebAPI` class, providing base url and bearer token as parameters:

```
api = OrderlyWebAPI('http://localhost:8080', 'H2AAbjvhjbbhbhjlh')
```
The bearer token must be obtained externally to this client. Use the 
[Montagu Python client](https://github.com/vimc/montagu-py) to obtain a token by 
authenticating with Montagu. 

To run a report:
```
api.run_report(report_name, report_paraneters)
```
where report_parameters is a dictionary or JSON string.


## Development

Clone the repo anywhere and install dependencies with (from the repo root):
```
pip3 install --user -r requirements.txt
```

Run dependencies (a local copy of Montagu API and database, and OrderlyWeb) with `scripts/run-dev-dependencies.sh`. This will also
add a test user to Montagu.

## Testing

Run dependencies as described above, then run `pytest`