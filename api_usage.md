# Store Finder API

## Endpoint: /nearest-stores/

### Parameters
- `latitude` (float) – required
- `longitude` (float) – required
- `product` (string) – optional

### Sample Request
`GET /nearest-stores/?latitude=-1.25&longitude=36.68&product=bread`

### Sample Response
```json
[
  {
    "store_name": "QuickMart",
    "distance_km": 2.1,
    "available": true
  }
]
