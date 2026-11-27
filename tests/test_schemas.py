# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Michele Salerno e i contributori di EduWISP
import json
from pathlib import Path

import pytest

from eduwisp_protocol import MESSAGES, ProtocolError, load_schema, validate

EXAMPLES = Path(__file__).resolve().parent.parent / "examples" / "v0"


@pytest.mark.parametrize("name", MESSAGES)
def test_schemi_validi(name):
    from jsonschema import Draft202012Validator

    Draft202012Validator.check_schema(load_schema(name))


@pytest.mark.parametrize("name", MESSAGES)
def test_esempi_conformi(name):
    validate(name, json.loads((EXAMPLES / f"{name}.json").read_text(encoding="utf-8")))


def test_campo_sconosciuto_rifiutato():
    data = json.loads((EXAMPLES / "status-report.json").read_text(encoding="utf-8"))
    data["imei"] = "non deve essere accettato"
    with pytest.raises(ProtocolError) as exc:
        validate("status-report", data)
    assert "imei" in str(exc.value)


def test_versione_sbagliata_rifiutata():
    with pytest.raises(ProtocolError):
        validate(
            "policy",
            {
                "protocol_version": "1",
                "policy_version": 1,
                "settings": {},
                "poll_interval_seconds": 900,
            },
        )


def test_messaggio_sconosciuto():
    with pytest.raises(KeyError):
        load_schema("inesistente")


@pytest.mark.parametrize(
    "name,file",
    [
        ("policy", "policy-family-access.json"),
        ("status-report", "status-report-family-access.json"),
        ("policy", "policy-apps.json"),
    ],
)
def test_esempi_accesso_familiari(name, file):
    validate(name, json.loads((EXAMPLES / file).read_text(encoding="utf-8")))


def test_scelta_dei_familiari_senza_campi_in_piu():
    data = json.loads((EXAMPLES / "status-report-family-access.json").read_text(encoding="utf-8"))
    data["family_access_choice"]["nome_genitore"] = "non deve essere accettato"
    with pytest.raises(ProtocolError):
        validate("status-report", data)


def test_app_identificativo_non_valido():
    data = json.loads((EXAMPLES / "policy-apps.json").read_text(encoding="utf-8"))
    data["apps"]["allowed"].append({"id": "../etc/passwd"})
    with pytest.raises(ProtocolError):
        validate("policy", data)


def test_capacita_app_consentite():
    data = json.loads((EXAMPLES / "enrollment-request.json").read_text(encoding="utf-8"))
    data["capabilities"].append("apps:allowlist")
    validate("enrollment-request", data)
    data["capabilities"].append("apps:qualsiasi")
    with pytest.raises(ProtocolError):
        validate("enrollment-request", data)


def test_app_vietate_senza_elenco_consentite():
    validate(
        "policy",
        {
            "protocol_version": "0",
            "policy_version": 1,
            "poll_interval_seconds": 900,
            "settings": {},
            "apps": {"mode": "blocklist", "allowed": [], "blocked": ["com.snapchat.android"]},
        },
    )
