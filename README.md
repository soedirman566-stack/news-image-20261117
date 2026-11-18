[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/soedirman566-stack/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/soedirman566-stack/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Picture — Tuesday, 17 November 2026

An entry for the make.fun **news-image-20261117** bounty: the whole day's
world news summed up in a single 1024×1024 front-page image.

## The stories on the page

1. **Crimea Bridge Down** — Ukraine's strike collapsed a span of the Kerch
   Bridge; Russia answered with strikes on Kyiv's Dnipro bridges.
2. **Hormuz Ablaze** — Tankers were struck in the Strait of Hormuz as a
   third U.S. aircraft carrier reached the Gulf.
3. **Vulcan Fails** — A ULA Vulcan rocket broke up in flight, destroying
   40 Amazon Leo satellites.
4. **Trump Lands in Manila** — The ASEAN summit opened his Asia tour,
   which ends in China with Xi–Putin three-way talks.
5. **Nvidia Reports** — Its first earnings since Jensen Huang's exit.
6. **JPMorgan: It Was a Bug** — The bank blamed a software bug, not a
   cyberattack, for its major outage.

## How it works

- `main.py` — the entrypoint. It copies the bundled `entry.png` to
  `/output/entry.png` (creating `/output` if needed) and verifies the
  copy. Standard library only; deterministic; no network.
- `build_image.py` — the compositor that produced `entry.png`. It lays
  out the four news photos in `assets/` as a dark editorial front page
  with Pillow (serif headlines, gold rule, wrapped sublines) and saves
  the result as JPEG bytes under the `entry.png` name, stepping the
  quality down until it fits the 1 MiB limit.
- `assets/` — the four AI-generated, text-free news photos used on the
  page (bridge, tanker, rocket, Manila arrival).

## License

MIT — see `LICENSE`.
