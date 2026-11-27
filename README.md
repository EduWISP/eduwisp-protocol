<p align="center"><img src="https://raw.githubusercontent.com/EduWISP/.github/main/branding/eduwisp-mark.svg" alt="EduWISP" height="72"></p>

# eduwisp-protocol

**Protocollo server-agente** · *Server-agent protocol*

Specifica aperta e versionata del protocollo tra il server EduWISP e gli **agenti di qualsiasi piattaforma** (il primo è il DPC Android): messaggi comuni, profili per piattaforma, dichiarazione delle capacità dell'agente, sicurezza e test di conformità.

> 🧪 **Stato: prototipo v0.** Prima bozza della specifica e degli schemi JSON: vedi [docs/developer/protocollo-v0.md](docs/developer/protocollo-v0.md). La progettazione è nella [documentazione EduWISP](https://eduwisp.org/docs/moduli/android/).

🇬🇧 *Open, versioned specification of the protocol between the EduWISP server and **agents on any platform** (the Android DPC first): common messages, platform profiles, agent capability declaration, security and conformance tests. **Status: design phase**, no code yet. See the [design docs](https://eduwisp.org/docs/en/modules/android/).*

## Documentazione / Documentation

- Progettazione / Design: <https://eduwisp.org/docs/moduli/android/>
- Mappa dei repository / Repository map: <https://eduwisp.org/docs/architettura/repository/>
- Documentazione del modulo / Module docs: [`docs/user/`](docs/user/) · [`docs/developer/`](docs/developer/)

## Uso / Usage

```bash
pip install -e .
python -c "from eduwisp_protocol import validate; validate('policy', {...})"
pytest
```

## Dipendenze / Dependencies

Nessuna. / *None.*

## Privacy

Dati personali previsti e regole: [PRIVACY.md](PRIVACY.md). Il rispetto della normativa su privacy e minori è un vincolo bloccante ([ADR-0008](https://eduwisp.org/docs/decisioni/0008-conformita-normativa/)).

## Responsabile del modulo / Module owner

Cerchiamo persone che vogliano prendere in carico questo modulo! Proponiti in [Discussions](https://github.com/EduWISP/docs/discussions). / *Want to own this module? Say hi in Discussions.*

## Contribuire / Contributing

Vedi [CONTRIBUTING](https://github.com/EduWISP/.github/blob/main/CONTRIBUTING.md) e il [Codice di condotta](https://github.com/EduWISP/.github/blob/main/CODE_OF_CONDUCT.md). **Mai dati personali reali** di studenti, famiglie o personale.

## Licenza / License

**AGPL-3.0-or-later**, con termini aggiuntivi di attribuzione e tutela del nome (sezione 7): vedi [LICENSE](LICENSE) e [NOTICE.md](NOTICE.md). Chi usa o modifica EduWISP deve sempre indicare «Basato su EduWISP» e non può usare il nome e il logo per versioni modificate. Licenza scelta secondo le [linee guida AgID](https://eduwisp.org/docs/decisioni/0006-licenza/) per il software usato via rete.

*AGPL-3.0-or-later with additional attribution and trademark terms (section 7): see LICENSE and NOTICE.md.*

I contributi richiedono il [DCO](https://github.com/EduWISP/.github/blob/main/CONTRIBUTING.md#dco) (`git commit -s`).
