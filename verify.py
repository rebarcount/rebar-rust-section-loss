#!/usr/bin/env python3
"""Recompute rust-section-loss.csv from the nominal diameters and check it has not drifted.

Usage: python3 verify.py
Exits 0 if every row agrees with the formula, 1 otherwise.
"""
import csv
import sys

FY = 60000.0          # psi, Grade 60
PCT_TOL = 0.05        # percentage points
LB_TOL = 10.0         # pounds, matches the rounding in the CSV


def expected(d, a, dd):
    pct = (1.0 - (1.0 - dd / d) ** 2) * 100.0
    return pct, a * FY * pct / 100.0


def main():
    bad = 0
    rows = 0
    with open("rust-section-loss.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows += 1
            d = float(r["nominal_diameter_in"])
            a = float(r["nominal_area_in2"])
            dd = float(r["diameter_loss_in"])
            pct, lb = expected(d, a, dd)
            if abs(float(r["area_loss_pct"]) - pct) > PCT_TOL:
                print("pct drift %s %s in: csv %s vs %.2f" % (r["bar_size"], dd, r["area_loss_pct"], pct))
                bad += 1
            if abs(float(r["tensile_loss_grade60_lb"]) - lb) > LB_TOL:
                print("lb drift  %s %s in: csv %s vs %.0f" % (r["bar_size"], dd, r["tensile_loss_grade60_lb"], lb))
                bad += 1
            if abs(float(r["tensile_capacity_grade60_lb"]) - a * FY) > 1:
                print("cap drift %s: csv %s vs %.0f" % (r["bar_size"], r["tensile_capacity_grade60_lb"], a * FY))
                bad += 1
    print("%d rows checked, %d mismatches" % (rows, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
