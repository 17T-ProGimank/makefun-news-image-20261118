# The World Today — 18 November 2026

Entry for the make.fun bounty `news-image-20261118`: sum up the world's
news of Wednesday 18 November 2026 in one image.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). It uses no network and no
randomness, so two runs write byte-identical files.

## The image

A newspaper front page, 1024×1024 PNG, 140,276 bytes, drawn locally with
`draw_image.py` (Python + Pillow, DejaVu fonts — build-time tools only;
nothing is needed at grade time beyond the PNG itself). Every word is real
typeset text, so nothing is garbled.

Stories, all of which happened or were first reported on 18 November 2026:

1. **APEC, Shenzhen** — Xi meets Putin; Trump joins them Thursday for the
   first-ever US–China–Russia summit. Quad leaders meet in Manila.
2. **Gulf** — US jets hit an Iranian missile site on Qeshm Island; Iran
   fires drones at US bases in Kuwait and Bahrain; a tanker is hit in
   the Strait of Hormuz.
3. **Ukraine** — part of the Crimean Bridge road span collapses after a
   second day of strikes; Russia confirms the damage.
4. **US Senate** — Democrat Mary Peltola beats Dan Sullivan in Alaska;
   Democrats take a 56–44 majority, their largest since 2009.
5. **Nvidia** — record quarter, revenue $115.8bn (+103%); the board
   rules out Jensen Huang returning as CEO.
6. **Voyager 1** — first human-made object one light-day from Earth,
   about 16 billion miles away.
7. **Cyclone Akvan** — strengthening in the Bay of Bengal, landfall due
   Friday on the Andhra Pradesh coast.

Footer ticker: US loses measles-free status after 26 years; Ebola in
DR Congo passes 11,000 cases; COP31 climate talks open in Antalya;
Philippines trade deal.

Sources checked against the day's briefings: Open Chronicle, The Daily
Short, Zark News, Morning Brief World, US Brief, Raj Global Studies.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png
```

To redraw the image from scratch: `python3 draw_image.py`.

## License

MIT — see `LICENSE`.
