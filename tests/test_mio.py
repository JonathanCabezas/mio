import mio
import time
import logging


def test_mio():
    # Setup
    mio.install_logger("test.log", True)

    # Test
    with mio.Section("Orders synchronization"):
        with mio.Section("Connecting to the database"):
            logging.debug("Using IP: {}", "192.168.0.1")
            time.sleep(1)
            logging.info("Connected to database successfully")
            logging.info("Orders fetched successfully")

        with mio.Section("Processing orders"):
            logging.warning("Order {} has an unavailable product", "42")
            logging.error(
                "Failed to process order '{}' with error: {}", "123", "No customer"
            )

        logging.info("'{}' saved successfully", "orders.csv")

    # Teardown
