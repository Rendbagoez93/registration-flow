"""Structlog-based logging configuration for Django."""

import logging
import sys

import structlog

SENSITIVE_KEYS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "secret",
    "authorization",
    "csrf_token",
}

# Event name or "path" that identifies a health-check ping.
HEALTH_CHECK_MARKERS = {
    "health_check_ping",
    "/healthz",
    "/health/",
    "/ping/",
}


def mask_sensitive_data(logger, method_name, event_dict):
    """Replace sensitive values with a masked placeholder before rendering."""
    for key in list(event_dict.keys()):
        if key.lower() in SENSITIVE_KEYS:
            event_dict[key] = "***MASKED***"
    return event_dict


def highlight_warnings_and_errors(logger, method_name, event_dict):
    """Wrap WARNING/ERROR/CRITICAL events in an ANSI highlight for the dev console."""
    level = event_dict.get("level", "").lower()
    event = event_dict.get("event", "")

    if level in ("error", "critical"):
        event_dict["event"] = f"\033[1;97;41m {event} \033[0m"
    elif level == "warning":
        event_dict["event"] = f"\033[1;30;43m {event} \033[0m"

    return event_dict


class DropRepeatedEvents:
    """Drop an event once the same event name + level + fields has been logged before."""

    def __init__(self):
        self._seen = set()

    def __call__(self, logger, method_name, event_dict):
        fingerprint = (
            event_dict.get("event"),
            event_dict.get("level"),
            tuple(
                sorted(
                    (k, str(v))
                    for k, v in event_dict.items()
                    if k not in ("event", "level", "timestamp")
                )
            ),
        )
        if fingerprint in self._seen:
            raise structlog.DropEvent
        self._seen.add(fingerprint)
        return event_dict


class HealthCheckOnce:
    """Log the first health-check ping, then drop the rest for this process."""

    def __init__(self):
        self._already_logged = False

    def __call__(self, logger, method_name, event_dict):
        is_health_check = (
            event_dict.get("event") in HEALTH_CHECK_MARKERS
            or event_dict.get("path") in HEALTH_CHECK_MARKERS
        )
        if is_health_check:
            if self._already_logged:
                raise structlog.DropEvent
            self._already_logged = True
        return event_dict


# Shared by structlog's own loggers and Django's stdlib loggers (django.request,
# django.db.backends, etc.) so everything gets the same treatment.
shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),   # timestamp
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    mask_sensitive_data,                            # mask sensitive values
    HealthCheckOnce(),                               # health check once
    DropRepeatedEvents(),                             # skip repeated events
    highlight_warnings_and_errors,                     # highlight WARNING/ERROR
]


def configure_structlog(log_level: str) -> None:
    """Configure structlog; call once from settings, after LOGGING is applied."""
    structlog.configure(
        processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level.upper())),
        cache_logger_on_first_use=True,
    )


def build_logging_config(log_level: str) -> dict:
    """Return Django's LOGGING dict, routed through the shared structlog processors."""
    log_level = log_level.upper()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored_console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "colored_console",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level,
            },
            "django": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }
