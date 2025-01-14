import logging
from langsmith import Langsmith
from prometheus_client import start_http_server, Summary, Counter

# Initialize Langsmith for monitoring and observability
langsmith = Langsmith(api_key="your_langsmith_api_key")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Total number of requests')

def log_request(request):
    logger.info(f"Received request: {request}")

def log_response(response):
    logger.info(f"Sending response: {response}")

def log_error(error):
    logger.error(f"Error occurred: {error}")

def monitor_request(func):
    def wrapper(*args, **kwargs):
        REQUEST_COUNT.inc()
        with REQUEST_TIME.time():
            try:
                response = func(*args, **kwargs)
                log_response(response)
                return response
            except Exception as e:
                log_error(e)
                raise e
    return wrapper

# Start Prometheus server
start_http_server(8001)

# Example usage of Langsmith for monitoring
def example_function():
    langsmith.track_event("example_event", {"key": "value"})

example_function()
