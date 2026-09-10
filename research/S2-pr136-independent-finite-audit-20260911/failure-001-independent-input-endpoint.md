# Retained independent-audit failure 001

The first independent audit stopped before any DCT or certificate verdict at
the `j=64` cosine input check. The audit incorrectly applied monotonicity to
an enclosure straddling `pi`; its upper endpoint lies above `pi`. The frozen
author generator correctly special-cases `cos(pi)=-1` exactly. The repair is
limited to exact `j=0` and `j=64` identities in the independent checker. No
author source, evidence, arithmetic constant, tolerance, or predicate changed.
