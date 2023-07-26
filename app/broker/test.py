import base64
import requests
import time
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Set up authentication
API_KEY='E524odtbfT7OVAAlbtk5kaMEpvluagydPEJhIs6djrgwB5Cd8ikzwQHYy9fXDX5'
PRIVATE_KEY_PATH='Private_key.txt'

# Load the private key.
# In this example the key is expected to be stored without encryption,
# but we recommend using a strong password for improved security.
with open(PRIVATE_KEY_PATH, 'rb') as f:
    private_key = load_pem_private_key(data=f.read(),
                                       password=None)

# Set up the request parameters
params = {
    'symbol':       'BTCEUR',
    'side':         'BUY',
    'type':         'MARKET',
    'quantity':     '0.0008000',
}

# Timestamp the request
timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
params['timestamp'] = timestamp

# Sign the request
payload = '&'.join([f'{param}={value}' for param, value in params.items()])
signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
params['signature'] = signature

# Send the request
headers = {
    'X-MBX-APIKEY': API_KEY,
}
response = requests.post(
    'https://api.binance.com/api/v3/order',
    headers=headers,
    data=params,
)
print(response.json())