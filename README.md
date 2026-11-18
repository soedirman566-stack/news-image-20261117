# The World in One Picture — 17 November 2026

An entry for make.fun's **news-image-20261117** competition: sum up the
world news of Tuesday 17 November 2026 in a single image.

The image is a dark, editorial newspaper front page — a masthead, two
photographs with headline bars, and a strip of one-line headlines —
composed programmatically at 1024×1024.

## The day's stories it sums up

1. **Crimea Bridge down** (hero photograph) — Ukraine's strike collapsed
   a section of the Kerch Bridge linking Russia to Crimea, in what
   Zelenskyy called "an unprecedented operation"; Russia retaliated
   against Kyiv's Dnipro bridges.
2. **Hormuz ablaze** (second photograph) — two tankers were struck in
   the Strait of Hormuz as a third U.S. aircraft carrier, USS Theodore
   Roosevelt, reached the Middle East; Iran also fired drones at a U.S.
   radar site in Bahrain.
3. **Trump lands in Manila** — opening an Asia tour that ends in China
   with Xi–Putin three-way talks.
4. **Vulcan rocket fails** — a ULA Vulcan failure in flight destroyed
   40 Amazon Leo satellites.
5. **Nvidia reports** — its first earnings since Jensen Huang's exit,
   with tech stocks falling ahead of the numbers.
6. Footer line — JPMorgan Chase blamed a software bug, not a
   cyberattack, for a major banking outage.

## How it works

- `build_image.py` — a Python/Pillow program that composes the front
  page from the two photographs in `assets/` (cover-cropped into their
  panels) plus the masthead, headlines and sublines set in DejaVu Serif
  Bold / Sans. It writes the result to `entry.png`. Because a
  photographic PNG at 1024×1024 would exceed the contest's 1 MiB limit,
  the composed picture is saved as JPEG bytes (quality ~88) inside the
  file named `entry.png` — the contest detects the format from the
  magic bytes, so this is explicitly allowed. Final file: 1024×1024,
  ~200 KB.
- `main.py` — the competition entrypoint. The harness runs it offline
  and expects the image at `/output/entry.png`, identical on every run,
  so it simply copies the committed `entry.png` next to it into place
  (standard library only, deterministic). It fails loudly if the source
  image is missing or the copy is incomplete.
- `assets/` — the two source photographs used by `build_image.py`.

To rebuild the image: `python3 build_image.py`

## License

MIT — see `LICENSE`.
