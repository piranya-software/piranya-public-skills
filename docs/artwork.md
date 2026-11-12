# Piranya artwork

`assets/piranya-icon.png` is the canonical public-distribution icon, derived from the official Piranya logo with the owner's explicit approval to reuse and adjust it to fit. It is not a new logo or rebrand.

## Source and integrity

- Source URL: https://support.piranya.dk/piranya-logo.png
- Source SHA-256: `dd09da91de0350d53bc7e393315f304bf14250dc4d092d1ac2d05ff7393f6922`
- Source format: PNG, RGBA, 1770 × 1695 pixels.
- The official https://piranya.dk/favicon.png was also inspected: PNG, RGBA, 167 × 159 pixels, SHA-256 `d00d1cf49d2f6626228025747c7e10d0c22f5a4c20e89c54cee6ab1cb54a1a74`. The higher-resolution official support logo was selected instead of enlarging the favicon. No unrelated social-preview image was used.
- Output SHA-256: `aadb3ad69a6664d3634a4cd9fb626494d429644cdfbb548ed3ad1c522d4c92e3`
- Output format: PNG, RGBA, 512 × 512 pixels; 48,843 bytes.

## Transformation and validation

Python with Pillow 13.0.0 converts the source to RGBA, then resizes the complete image with `Image.Resampling.LANCZOS` to 512 × 490 pixels. The dimensions use a common aspect-fit scale, with the height rounded to the nearest whole pixel. There is no cropping, independent-axis stretching, recoloring or redrawing.

The resized image is pasted without a mask at `(0, 11)` onto a transparent RGBA 512 × 512 canvas, preserving the source alpha. PNG encoding uses `optimize=False` and `compress_level=9`, without ancillary metadata. Repeating the encoding produced identical bytes in the checked environment.

Validation decoded the actual source and output PNGs and checked dimensions, mode and pixel transparency. Output alpha ranges from 0 to 255, with 144,116 fully transparent pixels and nonzero-alpha bounds `(0, 11, 512, 501)`. No native image-vision review was performed; these are decoded-image and pixel checks, not a claim of visual review.

## Rights

The Piranya logo remains copyrighted brand artwork of its respective rights holder. The owner's approval covers reuse and fit adjustment for this distribution; this document grants no new logo license or trademark rights. The repository's MIT license for public skills, documentation and tooling does **not** implicitly license the logo. Copyright and trademark rights in the logo are distinct from the MIT-licensed code and remain reserved to their respective holders.
