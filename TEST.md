# Unit Test

## Required packages
* pytest
* requests
* voluptuous

Note: Home Assistant is not required, there is a simple mock version of homeassistant in the tests directory. The unit test is only for testing the AvanzaStockSensor without Home Assistant, i.e. it mostly tests the api.

## Run
```python
python -m pytest tests/
```