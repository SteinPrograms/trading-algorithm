import logging
# Create the logger
def logger(name):
    return logging.getLogger(name)

# Always use basic config for logging because it is the best
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)