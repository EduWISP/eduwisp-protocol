# Changelog — eduwisp-protocol

## Non rilasciato / Unreleased

- Creazione del repository (fase di progettazione). / *Repository created (design phase).*
- Licenza AGPL-3.0-or-later con termini aggiuntivi (sezione 7), publiccode.yml e controllo DCO. / *AGPL-3.0-or-later licence with additional terms, publiccode.yml and DCO check.*
- Prototipo v0: schemi JSON di registrazione, policy, stato ed errore, esempi, specifica e test. / *v0 prototype: enrollment, policy, status and error schemas, examples, spec and tests.*
- Campi facoltativi `family_access` (policy) e `family_access_choice` (stato) per la scelta degli studenti maggiorenni (ADR-0018). / *Optional fields for adult students' family-access choice.*
- Campo facoltativo `apps` nella policy: elenco di app consentite con scadenza degli sblocchi temporanei (ADR-0019). / *Optional `apps` allowlist in the policy (ADR-0019).*
- Campi facoltativi `icon` e `install` (APK con impronta SHA-256) per le app obbligatorie (ADR-0020). / *Optional `icon` and `install` for required apps.*
