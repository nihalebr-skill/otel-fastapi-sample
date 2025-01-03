from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggingHandler
import logging
from app.config.settings import settings


def setup_telemetry():
    # Create resource
    resource = Resource.create({
        "service.name": settings.SERVICE_NAME,
        "service.instance.id": settings.INSTANCE_ID,
        "deployment.environment": settings.ENVIRONMENT
    })

    # Setup tracing
    trace_provider = TracerProvider(resource=resource)
    otlp_span_exporter = OTLPSpanExporter(
        endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        insecure=True
    )
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
    trace.set_tracer_provider(trace_provider)

    # Setup logging
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    log_exporter = OTLPLogExporter(
        endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        insecure=True
    )
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter))

    # Configure handler
    handler = LoggingHandler(level=logging.NOTSET,
                             logger_provider=logger_provider)
    logger = logging.getLogger("shopping.cart.api")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
