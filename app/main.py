from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from app.core.telemetry import setup_telemetry
from app.api.routes import cart

# Initialize FastAPI
app = FastAPI(title="Shopping Cart API")

# Setup telemetry
logger = setup_telemetry()

# Initialize instrumentations
LoggingInstrumentor().instrument(set_logging_format=True)
RequestsInstrumentor().instrument()

# Add correlation ID middleware


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    with trace.get_tracer(__name__).start_as_current_span("request_middleware") as span:
        correlation_id = request.headers.get("X-Correlation-ID")
        if correlation_id:
            span.set_attribute("correlation_id", correlation_id)
        response = await call_next(request)
        return response

# Include routers
app.include_router(cart.router)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
