# 冻结命题 v1

状态：AUTHOR_PROOF / PENDING_NONAUTHOR_REVIEW。总目标 PARTIAL。

基本对象为固定实标量 f:T-> [0,1]，允许非偶，K_f(i,j)=int f(theta)exp(2pi i(i-j)theta)dtheta，h(f)=lim H(K_f|[1,n])/n。H 是全部子集的 Shannon 熵，log 为自然对数。符号不随 n 改变。

## NC

对所有实 c,g∈W(T)（绝对可和 Fourier 系数），假设 c(theta+1/2)=c(theta)，int c=1/2，g(theta+1/2)=-g(theta)，g非零。令 a=2||c-1/2||_W<1，b=2||g||_W>0，R=(1-a)/(2b)，rho=(1+a)/2，M=-log(1-rho)-rho。也可用满足这些约束的范数上界 a,b。

对任意固定奇数 k>=1 满足 gamma=|ghat(k)|²>0，定义 T=min{R/2,2 gamma R³/sqrt(27M)}。对所有 n>=2k，函数 H_n(c+tg)+(2/3)(n-2k)gamma²t⁴ 在 [-T,T] 凹。故对所有 t0,t1∈[-T,T]、lambda∈[0,1]、m=(1-lambda)t0+lambda t1：

h(c+mg)-(1-lambda)h(c+t0g)-lambda h(c+t1g)
>= (2/3)gamma²[(1-lambda)t0⁴+lambda t1⁴-m⁴]。

非平凡弦严格。这里不冻结全合法区间或均值非 1/2 的更广结论。证明在 `proof.md` 第 3–7 节，两个精确应用在第 8 节。

## NC-channel

对所有严格二点 Hermitian 正收缩 A,B，各自非对角元非零；对任意 r∈(0,1)，不存在只依赖 A,B,r、与 C 无关的局部 Markov 矩阵 T_A,T_B，使对所有充分小复 2x2 交叉块 C：

(T_A tensor T_B)P_[A,C;C*,B] = P_[A,rC;rC*,B]。

证明在 `proof.md` 第 9 节。这里的否定只针对上述普适局部实现，不否定单一固定家族或非局部通道，更不否定熵凹性。

## 旧命题

旧全部量词和边界在 `previous_proof.md` 第 0–11 节原样保存；该文及 NC、NC-channel 都只具有作者证明状态。旧正文不因上传而自动获得非作者认证。
