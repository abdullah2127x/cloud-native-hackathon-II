"""Structured JSON logging configuration for MCP server"""

import json
import logging
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs JSON structured logs"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present in record
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "tool_name"):
            log_data["tool_name"] = record.tool_name
        if hasattr(record, "operation"):
            log_data["operation"] = record.operation
        if hasattr(record, "task_id"):
            log_data["task_id"] = record.task_id
        if hasattr(record, "error_type"):
            log_data["error_type"] = record.error_type

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for MCP server

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Suppress noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
