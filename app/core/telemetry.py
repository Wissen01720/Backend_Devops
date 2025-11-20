"""OpenTelemetry configuration for Axiom integration"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.core.config import settings


def setup_telemetry(app):
    """
    Configure OpenTelemetry tracing and export to Axiom
    
    Args:
        app: FastAPI application instance
    """
    # Only setup if Axiom is configured
    if not settings.axiom_api_token or not settings.axiom_dataset:
        print("⚠️  Axiom no configurado - Telemetría deshabilitada")
        print("   Configura AXIOM_API_TOKEN y AXIOM_DATASET en .env para habilitar telemetría")
        return None
    
    # Define the service name resource for the tracer
    resource = Resource(attributes={
        SERVICE_NAME: settings.service_name,
    })
    
    # Create a TracerProvider with the defined resource
    provider = TracerProvider(resource=resource)
    
    # Configure the OTLP/HTTP Span Exporter with Axiom headers and endpoint
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"https://{settings.axiom_domain}/v1/traces",
        headers={
            "Authorization": f"Bearer {settings.axiom_api_token}",
            "X-Axiom-Dataset": settings.axiom_dataset
        }
    )
    
    # Create a BatchSpanProcessor with the OTLP exporter
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    
    # Set the TracerProvider as the global tracer provider
    trace.set_tracer_provider(provider)
    
    # Instrument FastAPI automatically
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument SQLAlchemy (if database is configured)
    if settings.database_url:
        try:
            SQLAlchemyInstrumentor().instrument()
        except Exception as e:
            print(f"⚠️  No se pudo instrumentar SQLAlchemy: {e}")
    
    print(f"✅ OpenTelemetry configurado - enviando trazas a Axiom dataset: {settings.axiom_dataset}")
    
    # Return tracer for manual instrumentation if needed
    return trace.get_tracer(__name__)


# Export tracer for manual instrumentation in other modules
tracer = None
