# Protocollo EduWISP v0 (prototipo)

🇬🇧 *EduWISP server-agents protocol, version 0 (prototype). English summary at the end.*

> **Stato:** prototipo. La versione 0 può cambiare senza compatibilità all'indietro. Gli schemi normativi sono in [`eduwisp_protocol/schemas/v0/`](../../eduwisp_protocol/schemas/v0/), gli esempi in [`examples/v0/`](../../examples/v0/).

## Principi

- **Indipendente dalla piattaforma** ([ADR-0011](https://eduwisp.github.io/docs/decisioni/0011-multipiattaforma/)): le impostazioni sono concetti comuni (`camera_disabled`), non API Android.
- **Minimizzazione** (RC-002): ogni campo ha una finalità; i campi non previsti vengono rifiutati (`additionalProperties: false`). Niente IMEI, MAC, posizione, numero di serie.
- **L'agente dichiara cosa sa fare** (RNF-015) e segnala le impostazioni che non riesce ad applicare.
- **Solo software libero** ([ADR-0009](https://eduwisp.github.io/docs/decisioni/0009-solo-software-libero/)): l'agente interroga il server periodicamente; nessun servizio di notifica proprietario.

## Trasporto

- HTTPS (TLS 1.3 in produzione), JSON in UTF-8.
- Percorso base: `/api/protocol/v0/`.
- Ogni messaggio contiene `"protocol_version": "0"`.
- Gli errori usano il messaggio [`error`](../../eduwisp_protocol/schemas/v0/error.schema.json).

## Flusso

```text
Tecnico della scuola         Server EduWISP                    Agente (DPC)
        │  crea token di          │                                  │
        │  registrazione ───────► │                                  │
        │ ◄──── QR code ───────── │                                  │
        │  ripristino di fabbrica + scansione QR ──────────────────► │
        │                         │ ◄── POST /enroll ─────────────── │  1
        │                         │ ──── device_token ─────────────► │
        │                         │ ◄── GET /policy ──────────────── │  2
        │                         │ ──── policy effettiva ─────────► │
        │                         │                  applica la policy│
        │                         │ ◄── POST /status ─────────────── │  3
        │                         │      (poi 2 e 3 periodicamente)  │
```

### 1. Registrazione — `POST /api/protocol/v0/enroll`

- Corpo: [`enrollment-request`](../../eduwisp_protocol/schemas/v0/enrollment-request.schema.json). Il token arriva all'agente tramite il QR code di provisioning.
- Risposta `201`: [`enrollment-response`](../../eduwisp_protocol/schemas/v0/enrollment-response.schema.json) con `device_id` e `device_token`.
- Errori: `400 invalid_request`, `403 invalid_token`, `403 token_expired`, `403 token_exhausted`.

### 2. Policy — `GET /api/protocol/v0/policy`

- Intestazione: `Authorization: Bearer <device_token>`.
- Risposta `200`: [`policy`](../../eduwisp_protocol/schemas/v0/policy.schema.json). `policy_version` cresce a ogni modifica.
- Errori: `401 unauthorized`, `403 device_retired`.

### 3. Stato — `POST /api/protocol/v0/status`

- Intestazione: `Authorization: Bearer <device_token>`.
- Corpo: [`status-report`](../../eduwisp_protocol/schemas/v0/status-report.schema.json).
- Risposta `204`.

## Impostazioni della v0

| Impostazione | Tipo | Significato |
|---|---|---|
| `camera_disabled` | booleano | Fotocamere disattivate |
| `screen_capture_disabled` | booleano | Acquisizione dello schermo disattivata |

## Sicurezza

- Il token di registrazione è casuale, ha una scadenza e un numero massimo di usi; il server ne conserva solo l'hash.
- Il `device_token` ha la forma `<device_id>.<segreto>`; il server conserva solo l'hash del segreto e lo confronta in tempo costante.
- In produzione: solo HTTPS. Da valutare nelle versioni successive: certificati client, rotazione delle credenziali.

---

### English summary

Version 0 (prototype) defines three calls under `/api/protocol/v0/`: `POST /enroll` (enrollment token from the provisioning QR code → `device_id` and `device_token`), `GET /policy` (platform-independent effective policy, `Authorization: Bearer <device_token>`), and `POST /status` (applied policy version, compliance, unsupported settings). Messages are JSON, validated by JSON Schema 2020-12 with no unknown fields allowed (data minimisation). The agent polls; no proprietary push services.
