# cpi-latam
`cpi-latam` is a Python library designed to simplify the retrieval of Consumer Price Index (CPI) values from the central banks of countries in Latin America

Available countries:
- Perú 🇵🇪
- Colombia 🇨🇴

## Installation
```python
pip install cpilatam
```
## Usage
```python
from cpilatam import DF_CPI

# Retrieve CPI data for Peru
print(DF_CPI["peru"])

# Retrieve CPI data for Colombia
print(DF_CPI["colombia"])
```
## Update CPI Data
Keep your CPI data up-to-date by using the following update function:
```python
from cpilatam import update
update()
```
### Notes:
- Ensure you have an active internet connection for successful data retrieval.
- The library is currently designed to support data from Peru and Colombia only. Future updates may include additional countries.
- For the latest features and improvements, check the GitHub repository.
