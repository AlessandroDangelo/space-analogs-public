# Space Analogs — Earth Dev Defense

**Where on Earth can we rehearse life on the Moon and Mars?**
NASA Space Apps Challenge 2026 · Ouro Preto, Brazil · challenge *“Identify Earth Locations that Analog the Permanent Moon
Base Locations and Mars”*.

- **Live website:** https://earthdevdefense.github.io
- **Code (this repository):** https://github.com/earthdevdefense/space-analogs

We compare 43 places on Earth with 12 targets (6 candidate base regions at the lunar south pole and 6 Mars landing
sites) using open data from NASA, ESA and USGS. Every place is cut into 9×9 km tiles on the same 40 m grid on all three
worlds, and we measure four groups with equal weight: terrain (slope, roughness, relief), ground cover, surface
temperature and geology. The result is a 0–100 similarity score per target and per mission type, plus two
complementary views: ZEUS (zero-shot AI clustering) and a Mars climate layer.

## Results in one paragraph
For **Mars**, the most similar places are Askja (Iceland), Devon Island/Haughton and the Changtang plateau (Tibet). For
the **Moon**, nothing on Earth comes close (scores around 50), mostly because of the extreme cold of the lunar south
pole, so lunar analogs must be combined by mission type. Validation: places in ESA’s Catalogue of Planetary Analogues
rank on top for the Moon (AUC 0.85, p = 0.001); analogs rank above cities and rainforest (AUC 0.89 Moon, 0.76 Mars).
**Limits:** the 43 places were chosen by the team (selection bias); the method finds terrain and environment analogs,
not mineralogical ones. Full list in `docs/LIMITACOES.md`.

## Repository map
| path | what |
|---|---|
| `src/` | pipeline (Python): terrain, ground cover, temperature, geology, ZEUS, similarity, validation, site export |
| `site/` | the static website (HTML/CSS/JS, no build) |
| `outputs/` | result tables by protocol version (`v1_7` is current) |
| `entrada/` | inputs: target list, published analog lists, place coordinates |
| `entrega_zeus/` | standalone ZEUS package |
| `METODOLOGIA.md`, `docs/` | full methodology, features and missions, limitations (in Portuguese) |

## How to run
Python 3.11:
```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt          # Windows; use .venv/bin/python on Linux/macOS
.venv/Scripts/python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python -m src.rodar_tudo --desde terreno     # full pipeline (downloads public data; NASADEM needs a free NASA Earthdata login)
python -m src.validacao
```
Earthdata login is done once in your own terminal (`earthaccess.login(strategy='interactive', persist=True)`); the code
never stores credentials. To see the website locally: `python -m http.server 8765 --directory site`.

## Data, licenses and privacy
- **Code:** MIT License (see `LICENSE`).
- **Third-party data keep their own licenses and credits** (NASA/USGS public domain; ESA WorldCover CC BY 4.0; AADC
  CC BY 4.0; Macrostrat CC BY 4.0; PGC citation required; ZEUS Apache-2.0). Full list on the website (Methodology →
  Data sources and credits) and in `src/exportar_site.py`.
- **Not included:** raw data from the Meteomatics API (hackathon account; its license does not allow redistribution).
  `entrada/terra_por_local.csv` here has only place names, types and coordinates.
- **Privacy (LGPD):** this repository has no personal contact data or photos; team contacts appear only on the website,
  with each member’s consent.

## Team
Earth Dev Defense — Pablo de Oliveira Passarini (team lead), Luís Gustavo de Oliveira Miranda, Henrique Ulhôa de Faria,
Icaro Luiz Lage Vasconcelos, Alessandro D’Angelo, Gabriel Correia Moreira.
