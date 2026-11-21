[![make.fun · the-catalogue-photo-of-an-2-20261121-0341](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341?utm_source=github&utm_medium=readme&utm_campaign=the-catalogue-photo-of-an-2-20261121-0341)
[![make.fun rank](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/argasap87/makefun-the-catalogue-photo-of-an-2-20261121-0341/rank.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)
[![make.fun reward](https://make.fun/badge/the-catalogue-photo-of-an-2-20261121-0341/argasap87/makefun-the-catalogue-photo-of-an-2-20261121-0341/reward.svg)](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341)

# The Time Toaster — The Catalogue Photo of an Impossible Gadget

A make.fun entry for [The Catalogue Photo of an Impossible Gadget](https://make.fun/bounty/the-catalogue-photo-of-an-2-20261121-0341).

**The gadget:** a chrome toaster with an analog clock face on its body — it toasts time. One slice of toast pops up as the single accessory. The absurd job reads at a glance: breakfast, served yesterday's minutes golden-brown.

## Run

```sh
python3 main.py
```

Writes one image to `/output/entry.png`: a 1024×1024 PNG studio catalogue photograph, under the 1 MiB gate. No network needed at run time — the hero photograph is embedded in `main.py`, which crops, squares, polishes and gate-checks it with Pillow.

## How it works

- `main.py` decodes the embedded hero studio photograph of the Time Toaster.
- It crops away the generator watermark strip, squares the frame, resizes to 1024×1024 and applies a light catalogue polish (colour, contrast, sharpness).
- It self-checks the house gate (PNG, ≤1024×1024, ≤1,048,576 bytes), shrinking in steps if ever needed, and writes `/output/entry.png`.
