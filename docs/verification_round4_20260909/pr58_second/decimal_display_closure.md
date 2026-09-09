# PR58 Decimal Display Closure

Scope: exact textual patch `decimal_display_patch.diff`, from author head `5ab` to `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`, concerning only the displayed wording around `RESULT.md` (5.1).

## Original Presentation Issue

The original `RESULT.md` lines 244-250 said that `W(10)=E[b psi(u_10)]` lies inside an interval of width `< 5.83e-83` "whose upper endpoint is" followed by a decimal display. That wording could be read as claiming the printed decimal itself is the exact rational upper endpoint.

The independent `s10.json` evidence is exact rational: the upper endpoint has a negative numerator and positive denominator, and the outward decimal display begins

`-0.000000660768942182859172764829355178151999283911189738012952950341245049469295003033548294`.

The exact sign comes from the rational endpoint, not from trusting a rounded decimal.

## Patch Checked

The patch changes the sentence to:

`inside an interval of width < 5.83e-83 whose exact rational upper endpoint is negative and is printed approximately as`

followed by the same decimal display.

Status: CLOSED / CORRECT.

This repair closes the presentation concern. It explicitly separates the exact rational sign claim from the approximate decimal rendering. It does not alter formulas, numerical targets, code, output, or the underlying certificate claim.

This closure does not add any new mathematical theorem and does not certify material outside the original PR58 finite `s=10` display.
