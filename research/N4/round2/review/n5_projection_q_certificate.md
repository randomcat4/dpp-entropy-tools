# N5 Projection q Entropy Certificate

Status: CONFIRMED. This is only the projection-law entropy gate for the
five-point exploratory reason in `top_layer_budget.md`; it is not a face
counterexample or a concavity claim.

Frame: `U = H(a)H(b)[:,0:3]`, with `H(w)=I-2ww^T/(w^T w)`,
`a=(1,2,3,4,5)`, and `b=(2,-1,3,-2,1)`.

For the ten three-row sets, exact `q_S=det(U_S)^2` is:

| S | q_S |
|---|---:|
| 123 | 123201/1092025 |
| 124 | 374544/1092025 |
| 125 | 1296/43681 |
| 134 | 144/3025 |
| 135 | 49284/1092025 |
| 145 | 254016/1092025 |
| 234 | 576/9025 |
| 235 | 30276/1092025 |
| 245 | 28224/1092025 |
| 345 | 3136/43681 |

Exact sum: `1`.

Executable artifact: `n5_projection_q_check.py`.

Run artifact: `n5_projection_q_certificate.json`.

Run metadata: PID `54680`, exit status `0`, script SHA-256
`b5d8cba12817158463c1eb9b0e6dfe7c1d6e87319e727e1ea9ce4f4ffdd07033`,
Python `3.12.14`, log interval calls `10`.

Using rational atanh-series log intervals with 180 terms for
`H(q)=-sum_S q_S log q_S`, the certified interval is contained in
`[1.9001618764609496, 1.9001618764609496]` at the printed precision. In particular,

`H(q) - 3/2 > 0.4001618764609496 > 0`.

Therefore the strict gate `H(q)>3/2` is confirmed for this rational frame.
