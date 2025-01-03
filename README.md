# Shopping Cart API

A FastAPI-based shopping cart service with OpenTelemetry integration and Redis-backed state management.

## Features

- RESTful API for shopping cart management
- Persistent cart storage using Redis
- Distributed tracing with OpenTelemetry
- Logging with OpenTelemetry integration
- Docker containerization
- Metrics collection and monitoring

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Redis**: Cart state management and persistence
- **OpenTelemetry**: Distributed tracing and monitoring
- **Docker**: Containerization and orchestration
- **Pydantic**: Data validation and settings management

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Redis
- OpenTelemetry Collector

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       └── cart.py
│   ├── config/
│   │   └── settings.py
│   ├── core/
│   │   ├── redis.py
│   │   └── telemetry.py
│   ├── models/
│   │   └── cart.py
│   ├── services/
│   │   └── cart_service.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
PROJECT_NAME=Shopping Cart API
VERSION=1.0.0
API_V1_STR=/api/v1
DEBUG=true
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# OpenTelemetry settings
OTEL_SERVICE_NAME=shopping-cart-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_TRACES_SAMPLER=parentbased_always_on
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp

# Business logic settings
MAX_CART_ITEMS=50
MAX_ITEM_QUANTITY=100
CART_EXPIRY_HOURS=24
```

## Installation & Running

1. Clone the repository:

```bash
git clone <repository-url>
cd shopping-cart-api
```

2. Build and start the services:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Add Item to Cart

```http
POST /cart/{user_id}/items?item={item_name}&quantity={quantity}
```

### Get Cart Contents

```http
GET /cart/{user_id}
```

### Clear Cart

```http
DELETE /cart/{user_id}
```

## Example Usage

### Add Item to Cart

```bash
curl -X POST "http://localhost:8000/cart/user123/items?item=book&quantity=2"
```

### Get Cart Contents

```bash
curl "http://localhost:8000/cart/user123"
```

### Clear Cart

```bash
curl -X DELETE "http://localhost:8000/cart/user123"
```

## Monitoring and Observability

The application includes comprehensive monitoring and observability features:

- **Metrics**: Exposed via OpenTelemetry collector on port 8889
- **Traces**: Collected and exported via OpenTelemetry collector
- **Logs**: Integrated with OpenTelemetry for structured logging
- **Dashboards**: Available through OpenObserve UI at port 5080

## Testing

To run the tests:

```bash
# TODO: Add testing instructions
```

## Cart Data Model

Each cart item contains:

- Item name
- Quantity
- Timestamp added
- Maximum limits configurable via environment variables

## Error Handling

The API includes comprehensive error handling for:

- Invalid quantities
- Cart not found
- Maximum cart item limits
- Redis connection issues

## Security Considerations

- CORS configuration via environment variables
- Rate limiting per user
- Cart expiration after configurable period
