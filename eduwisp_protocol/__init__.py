# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
"""Protocollo EduWISP server-agenti: schemi JSON e funzioni di validazione.

EduWISP server-agents protocol: JSON schemas and validation helpers.
"""

import json
from functools import cache
from importlib import resources

from jsonschema import Draft202012Validator

PROTOCOL_VERSION = "0"

#: Nomi dei messaggi definiti dalla versione 0 del protocollo.
MESSAGES = (
    "enrollment-request",
    "enrollment-response",
    "policy",
    "status-report",
    "error",
    "app-request",
)


class ProtocolError(ValueError):
    """Messaggio non conforme allo schema del protocollo."""

    def __init__(self, message_name: str, errors: list[str]):
        self.message_name = message_name
        self.errors = errors
        super().__init__(f"{message_name}: " + "; ".join(errors))


@cache
def load_schema(message_name: str, version: str = PROTOCOL_VERSION) -> dict:
    """Restituisce lo schema JSON di un messaggio."""
    if message_name not in MESSAGES:
        raise KeyError(f"Messaggio sconosciuto: {message_name}")
    path = resources.files(__package__) / "schemas" / f"v{version}" / f"{message_name}.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate(message_name: str, data: object, version: str = PROTOCOL_VERSION) -> None:
    """Valida un messaggio; solleva ProtocolError con l'elenco degli errori."""
    validator = Draft202012Validator(load_schema(message_name, version))
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ProtocolError(
            message_name,
            [f"{'/'.join(str(p) for p in e.path) or '(radice)'}: {e.message}" for e in errors],
        )
