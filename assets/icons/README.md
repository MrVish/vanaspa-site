# Icons

VĀNA uses **Phosphor Icons — Light weight** from CDN as the primary icon set. This is a
substitution — no set was specified in the brief. The light weight matches the brand's
quiet, thin-stroke sensibility.

## Usage

```html
<!-- From CDN -->
<script src="https://unpkg.com/phosphor-icons"></script>

<!-- In markup -->
<i class="ph-light ph-calendar"></i>
<i class="ph-light ph-clock"></i>
<i class="ph-light ph-map-pin"></i>
```

## Colour
Icons inherit `currentColor`. On Canopy they are Linen; on Cream they are Canopy; on
hover/active they shift to Terracotta.

## Size
- `16px` inline
- `20px` for buttons
- `24px` standalone

## No emoji. No unicode glyph icons.
The middle dot `·` is the only unicode character permitted as a typographic separator.

## If the client wants a custom set
Commission a bespoke 1.5px-stroke, 24×24 set matching the brand mark's line quality.
Drop the SVGs in this folder and swap the CDN reference.
