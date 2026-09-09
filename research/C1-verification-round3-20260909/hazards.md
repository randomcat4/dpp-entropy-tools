# Known review hazards

1. PR43 previously had incompatible reading maps. v2 of this review freezes
   the author's unified v3.1 statement at an exact commit.
2. Some unchanged PR43 generated inputs still describe symmetric reversible
   conductances. The current fixed LP uses directed stationary flows without
   detailed balance. C2 acknowledged this distinction publicly in issue #45.
3. The helper's displayed state bit strings put matrix coordinate 1 at the
   rightmost bit. Any independent certificate needs the explicit map.
4. The two nested PR43 verifiers are both required for its existing replay;
   the older task command list alone is not the complete handoff.
5. A requested full closed-interval probability lower bound can conflict with
   a zero-probability endpoint. C2 has requested an endpoint contract rather
   than guessing it. This does not block interior analytic proof review.
6. PR41's missing-edge coordinate and Fisher identities do not settle its
   remaining acceleration inequality.
7. PR43's correlated-family descriptive condition and all theorem quantifiers
   are reviewed literally, independently of the presence of a valid fixture.

Items 2–5 are already tracked in public computation issue #45. This packet
does not start a duplicate computation or expand those unresolved contracts.
