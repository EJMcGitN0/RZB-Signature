# RZB Signature

Gmail email signature for Eric McCollom, Rogue Zerobyte.

- Live page with a **Copy signature** button: https://ejmcgitn0.github.io/RZB-Signature/
- Images are served from GitHub Pages (`assets/`). The signature HTML points at those
  absolute URLs, so renaming or moving a file in `assets/` breaks every email already sent.

## Install in Gmail

1. Open the live page and click **Copy signature**.
2. Gmail → Settings (gear) → See all settings → General → Signature → Create new.
3. Click in the signature box, paste, and set it as the default for new emails and replies.
4. Scroll down and click **Save Changes**.

## Changing the images

Source images are in `source/`. Regenerate the PNGs (needs Pillow, macOS fonts):

```bash
python3 source/make_assets.py source assets
```

Images are rendered at 2x their display size, with the round crop baked in because Outlook
ignores CSS `border-radius`. To change an image, keep the same file name or update `index.html`.
