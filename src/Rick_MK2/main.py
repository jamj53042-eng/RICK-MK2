from src.logger import get_logger
from src.config import Config

logger = get_logger(__name__)

def main():
    logger.info("Rick backbone starting up...")
    config = Config()
    logger.info(f"Loaded config: {config}")
    logger.success("Rick's backbone is alive and ready!")

if __name__ == "__main__":
    main()
