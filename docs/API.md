# API Reference

## Base URL

```
http://localhost:8000/api
```

## Signal Endpoints

### Upload Signal

```http
POST /signals/upload
```

**Request Body**:
```json
{
  "ap_mac": "00:11:22:33:44:55",
  "ap_ssid": "WiFi-Network",
  "rssi": -50,
  "frequency": 2400,
  "channel": 6,
  "signal_quality": 85.0
}
```

**Response**:
```json
{
  "id": 1,
  "status": "recorded"
}
```

### Get Live Signals

```http
GET /signals/live?limit=10
```

**Response**:
```json
[
  {
    "ap_mac": "00:11:22:33:44:55",
    "rssi": -50,
    "timestamp": "2026-05-27T10:30:00Z"
  }
]
```

### Get Signal History

```http
GET /signals/history?ap_mac=00:11:22:33:44:55&limit=100
```

## Location Endpoints

### Update Location

```http
POST /location/update
```

**Request Body**:
```json
{
  "room": "Living Room",
  "x_coord": 5.5,
  "y_coord": 4.2,
  "confidence": 0.92,
  "movement_state": "stationary"
}
```

### Get Current Location

```http
GET /location/current
```

**Response**:
```json
{
  "room": "Living Room",
  "x": 5.5,
  "y": 4.2,
  "confidence": 0.92,
  "movement_state": "stationary"
}
```

### Get Location History

```http
GET /location/history?limit=50
```

## Calibration Endpoints

### Start Calibration

```http
POST /calibration/start
```

**Request Body**:
```json
{
  "house_name": "My House"
}
```

**Response**:
```json
{
  "calibration_id": 1,
  "status": "started"
}
```

## Health Check

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-27T10:30:00Z"
}
```

## WebSocket Events

### Connect

```
ws://localhost:8001
```

### Location Update Event

```json
{
  "event": "location_update",
  "data": {
    "room": "Living Room",
    "x": 5.5,
    "y": 4.2,
    "confidence": 0.92,
    "timestamp": "2026-05-27T10:30:00Z"
  }
}
```

### Signal Update Event

```json
{
  "event": "signal_update",
  "data": {
    "ap_mac": "00:11:22:33:44:55",
    "rssi": -50,
    "timestamp": "2026-05-27T10:30:00Z"
  }
}
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request body"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error message"
}
```
