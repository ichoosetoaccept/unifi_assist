import os
from pathlib import Path
from typing import Optional
import structlog
import logging
import sys
from structlog.stdlib import BoundLogger
from structlog.processors import JSONRenderer


def setup_logging(
    name: str = "unifi_assist",
    log_level: Optional[str] = None,
    log_to_file: Optional[bool] = None,
    log_dir: str = "logs",
) -> BoundLogger:
    """Setup structured logging configuration.

    Args:
        name: Logger name
        log_level: Override log level from env
        log_to_file: Override file logging from env
        log_dir: Directory for log files
    """
    # Get settings from environment or use defaults
    level = log_level or os.getenv("UNIFI_ASSIST_LOG_LEVEL", "INFO").upper()
    to_file = (
        log_to_file
        if log_to_file is not None
        else bool(int(os.getenv("UNIFI_ASSIST_LOG_TO_FILE", "0")))
    )

    # Configure standard logging for console
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    # Base processors for all outputs
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Console-specific processors
    console_processors = shared_processors.copy()
    if sys.stdout.isatty():
        console_processors.append(structlog.dev.ConsoleRenderer())
    else:
        console_processors.append(JSONRenderer())

    # File handlers if enabled
    if to_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        # JSON log file handler
        json_handler = logging.FileHandler(
            log_path / f"{name}.json.log", encoding="utf-8"
        )
        json_handler.setLevel(level)
        json_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=JSONRenderer(),
                foreign_pre_chain=shared_processors,  # type: ignore
            )
        )

        # Human-readable log file handler
        readable_handler = logging.FileHandler(
            log_path / f"{name}.readable.log", encoding="utf-8"
        )
        readable_handler.setLevel(level)
        readable_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processor=structlog.dev.ConsoleRenderer(colors=False),
                foreign_pre_chain=shared_processors,  # type: ignore
            )
        )

        # Add both handlers
        logging.getLogger().addHandler(json_handler)
        logging.getLogger().addHandler(readable_handler)

    # Configure structlog
    structlog.configure(
        processors=console_processors,  # type: ignore
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(name)  # type: ignore[no-any-return]
