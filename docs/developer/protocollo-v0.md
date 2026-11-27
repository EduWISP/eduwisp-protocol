# Protocollo EduWISP v0 (prototipo)

🇬🇧 *EduWISP server-agents protocol, version 0 (prototype). English summary at the end.*

> **Stato:** prototipo. La versione 0 può cambiare senza compatibilità all'indietro. Gli schemi normativi sono in [`eduwisp_protocol/schemas/v0/`](../../eduwisp_protocol/schemas/v0/), gli esempi in [`examples/v0/`](../../examples/v0/).

## Principi

- **Indipendente dalla piattaforma** ([ADR-0011](https://eduwisp.org/docs/decisioni/0011-multipiattaforma/)): le impostazioni sono concetti comuni (`camera_disabled`), non API Android.
- **Minimizzazione** (RC-002): ogni campo ha una finalità; i campi non previsti vengono rifiutati (`additionalProperties: false`). Niente IMEI, MAC, posizione, numero di serie.
- **L'agente dichiara cosa sa fare** (RNF-015) e segnala le impostazioni che non riesce ad applicare.
- **Solo software libero** ([ADR-0009](https://eduwisp.org/docs/decisioni/0009-solo-software-libero/)): l'agente interroga il server periodicamente; nessun servizio di notifica proprietario.

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
| `vpn_config_disabled` | booleano | Configurazione di VPN vietata: le app VPN non possono attivarsi |
| `private_dns_config_disabled` | booleano | Modifica del DNS privato vietata |

## App consentite

Campo facoltativo `apps` nella policy ([ADR-0019](https://eduwisp.org/docs/decisioni/0019-app-consentite/)), per gli agenti che dichiarano la capacità `apps:allowlist`:

- `mode`: `allowlist` (si usano solo le app in `allowed`) oppure `blocklist` (si bloccano solo le app in `blocked`, quando l'istituto non usa l'elenco di app consentite);
- `allowed`: identificativi delle app consentite (per Android il nome del pacchetto), ciascuno con un'eventuale scadenza `until` per gli sblocchi temporanei e `required: true` per le app obbligatorie;
- `blocked`: app vietate dalla piattaforma (social, VPN, Tor...), sempre sospese in entrambe le modalità.

L'agente sospende le app da bloccare tranne quelle protette (l'agente stesso, la schermata Home, le tastiere attive), vieta le installazioni da fonti sconosciute, richiude le app sbloccate alla scadenza anche senza rete e segnala allo studente le app obbligatorie non ancora installate (rapporto: `apps_required` con motivo `pending`). Un agente che non sa applicare l'elenco lo segnala come `apps` non supportato. Nessun elenco delle app installate viene inviato al server.

Esempio: [`policy-apps.json`](../../examples/v0/policy-apps.json).

## Accesso dei familiari agli studenti maggiorenni

Campi facoltativi, aggiunti senza cambiare versione: gli agenti che non li conoscono continuano a funzionare ([ADR-0018](https://eduwisp.org/docs/decisioni/0018-interfaccia-per-ruoli/)).

- Nella **policy**, `family_access` compare solo se il dispositivo è affidato a uno studente maggiorenne: `{"choice_requested": true, "granted": null}`. `granted` è la scelta registrata (`null` = non ancora fatta: i familiari non hanno accesso).
- L'agente mostra la scelta allo studente e la fa **confermare con il blocco schermo** del dispositivo.
- Nel **rapporto di stato**, `family_access_choice` riporta la scelta: `{"granted": false, "decided_at": "<data e ora>"}`. Il server la accetta solo se l'aveva chiesta e se è più recente di quella registrata, e la scrive nel registro delle operazioni.

Esempi: [`policy-family-access.json`](../../examples/v0/policy-family-access.json), [`status-report-family-access.json`](../../examples/v0/status-report-family-access.json).

## Sicurezza

- Il token di registrazione è casuale, ha una scadenza e un numero massimo di usi; il server ne conserva solo l'hash.
- Il `device_token` ha la forma `<device_id>.<segreto>`; il server conserva solo l'hash del segreto e lo confronta in tempo costante.
- In produzione: solo HTTPS. Da valutare nelle versioni successive: certificati client, rotazione delle credenziali.

---

### English summary

Version 0 (prototype) defines three calls under `/api/protocol/v0/`: `POST /enroll` (enrollment token from the provisioning QR code → `device_id` and `device_token`), `GET /policy` (platform-independent effective policy, `Authorization: Bearer <device_token>`), and `POST /status` (applied policy version, compliance, unsupported settings). Messages are JSON, validated by JSON Schema 2020-12 with no unknown fields allowed (data minimisation). Optional `apps` (policy) carries the app allowlist with optional unlock expiry (ADR-0019). Optional `family_access` (policy) and `family_access_choice` (status) let an adult student decide on their device, confirmed with the screen lock, whether family members keep access (ADR-0018). The agent polls; no proprietary push services.
