# Rebar section loss from a measured diameter loss

Rust on rebar is not a rejection, and the code says how to test it rather than how it looks.
**ACI 318-19 26.6.1.2(b)** accepts rust, mill scale or both provided a hand-wire-brushed
representative test specimen still complies with the ASTM specification for the minimum dimensions
(including height of deformations) and the weight per unit length; A615 12.2 adds cross-sectional
area and tensile properties.

That leaves a caliper reading and a judgement. This file is the arithmetic in between: how much of a
bar's cross-section is gone, for a diameter loss you measured, bar size by bar size.

## The file

`rust-section-loss.csv` is long format, one row per bar size and diameter-loss step: six sizes
(#3, #4, #5, #6, #7, #8) and four steps (0.005 to 0.030 in), 24 rows.

| column | meaning |
|---|---|
| `bar_size` | US bar size designation |
| `nominal_diameter_in` | nominal diameter, inches |
| `nominal_area_in2` | nominal cross-sectional area, square inches |
| `nominal_weight_lb_per_ft` | nominal weight, pounds per foot |
| `diameter_loss_in` | measured diameter loss, inches (nominal minus the worst caliper reading) |
| `area_loss_pct` | share of the cross-section lost, percent |
| `tensile_capacity_grade60_lb` | nominal tensile capacity at Grade 60 (60,000 psi) |
| `tensile_loss_grade60_lb` | capacity given up by the area loss, pounds |

## The arithmetic

Area goes with the square of the diameter, so a diameter loss removes this share of the section:

    area_loss = 1 - (1 - diameter_loss / d)^2

For small losses this is close to `2 x diameter_loss / d`, which is why a 1% diameter loss is about a
2% area loss. Tensile capacity is area times yield, so at a given grade the area share is also the
capacity share: `tensile_loss = fy x A x area_loss`.

Worked example, #4 at Grade 60 (A = 0.20 in2, capacity 12,000 lb): a 0.010 in diameter loss is 4.0%
of the area, or 480 lb.

The same diameter loss costs a small bar more than a large one, because the loss is a larger fraction
of a smaller diameter. 0.010 in is 5.3% of a #3 and 2.0% of a #8.

## Using it

1. Wire brush a sample, or rely on the handling the bundle has already had. ACI 318-19
   R26.6.1.2(b) notes that a normal amount of rust increases bond and that normal rough handling
   removes rust loose enough to impair it.
2. Caliper three points around the bar, take the worst reading, subtract it from nominal.
3. Look up the row. Then look at the bar again for pits: a single pit is a notch rather than a
   percentage, and 1/16 in deep is 12.5% of a #4's diameter at that point.

## What this is not

- Not an assessment of steel already inside a structure. That is a cover survey, a half-cell
  potential map and a chloride test, and it needs an engineer.
- Not a capacity calculation for a pitted bar. 26.6.1.2(b) is pass or fail on a specimen.
- Not applicable unchanged to coated or alloy bar: A767 galvanised, A775 epoxy-coated and A955
  stainless each carry their own surface and damage rules.

## Provenance

Nominal diameters, areas and weights are the standard nominal values for US bar sizes. The clause
text and the argument around it -- why deformation height is part of the test, what a rust layer
costs against 75 years of service corrosion, and the three cases where a bar is scrap -- are written
up at:

https://rebarcount.com/what-is-rebar-made-of

`verify.py` recomputes every row from the diameters and exits non-zero if the CSV drifts.

## License

CC0 1.0. Copy it into a spec, a spreadsheet or a script; no attribution needed.
