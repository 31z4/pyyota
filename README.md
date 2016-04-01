# pyyota

[Yota](http://www.yota.ru/en/) is a Russian mobile broadband services provider and smartphone manufacturer. This is a very simple Python module for interacting with it.

## Usage

```python
from yota import Yota

yota = Yota('username', 'password')

# List offers
print(yota.offers)

# Get current tariff
print(yota.tariff)

# Set new tariff
yota.tariff = 'POS-MA29-0016'
```
