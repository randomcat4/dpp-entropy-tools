// Complete-event DPP conditional entropy curvature, author interval certificate.
// Build: g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp certify_nodes.cpp -o certify_nodes
// No std::log/sin/cos is used. Transcendental inputs/log2 are rationally enclosed
// by make_inputs.py; logarithms use a 16-term atanh expansion with a proven tail.
#include <algorithm>
#include <array>
#include <atomic>
#include <cfenv>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <mutex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <set>
#include <omp.h>
#include <sys/resource.h>

static_assert(sizeof(double)==sizeof(uint64_t),"binary64 required");
static_assert(std::numeric_limits<double>::is_iec559,"IEEE 754 required");
inline double up(double x) {
    if (!std::isfinite(x)) throw std::runtime_error("nonfinite arithmetic");
    if (x==0.0) return std::numeric_limits<double>::denorm_min();
    uint64_t u; std::memcpy(&u,&x,8); if(x>0) ++u; else --u;
    std::memcpy(&x,&u,8); return x;
}
inline double dn(double x) {
    if (!std::isfinite(x)) throw std::runtime_error("nonfinite arithmetic");
    if (x==0.0) return -std::numeric_limits<double>::denorm_min();
    uint64_t u; std::memcpy(&u,&x,8); if(x>0) --u; else ++u;
    std::memcpy(&x,&u,8); return x;
}
struct I { double l,h; I():l(0),h(0){} explicit I(double x):l(x),h(x){} I(double a,double b):l(a),h(b){if(a>b)throw std::runtime_error("reversed interval");} };
inline I operator+(I a,I b){return I(dn(a.l+b.l),up(a.h+b.h));}
inline I operator-(I a,I b){return I(dn(a.l-b.h),up(a.h-b.l));}
inline I operator-(I a){return I(-a.h,-a.l);}
inline I operator*(I a,I b){
    double p=a.l*b.l,q=a.l*b.h,r=a.h*b.l,s=a.h*b.h;
    return I(dn(std::min(std::min(p,q),std::min(r,s))),up(std::max(std::max(p,q),std::max(r,s))));
}
inline I inv(I a){if(a.l<=0&&a.h>=0)throw std::runtime_error("division across zero");return I(dn(1.0/a.h),up(1.0/a.l));}
inline I operator/(I a,I b){return a*inv(b);}
inline I square(I a){
    double p=a.l*a.l,q=a.h*a.h;
    return I(a.l<=0&&a.h>=0?0.0:dn(std::min(p,q)),up(std::max(p,q)));
}
const I LOG2(0x1.62e42fefa39eep-1,0x1.62e42fefa39f0p-1);
std::array<I,16> ODD;
I log_i(I a){
    if(a.l<=0)throw std::runtime_error("nonpositive logarithm");
    int e=0;
    // Scaling is by exact powers of two; the interval encloses the scaled input.
    while(a.l+a.h>3.0){a=I(a.l*0.5,a.h*0.5);++e;}
    while(a.l+a.h<1.5){a=I(a.l*2.0,a.h*2.0);--e;}
    if(a.l<0.7||a.h>1.6)throw std::runtime_error("log range too wide");
    I y=(a-I(1))/(a+I(1));
    if(y.l< -0.25||y.h>0.25)throw std::runtime_error("atanh tail range");
    I yy=square(y),p=ODD[15];
    for(int j=14;j>=0;--j)p=ODD[j]+yy*p;
    return I(2)*y*p+I(-0x1p-68,0x1p-68)+I(double(e))*LOG2;
}
struct J {I v,d,h; J():v(),d(),h(){} explicit J(double x):v(x),d(),h(){} J(I a,I b,I c):v(a),d(b),h(c){} };
inline J operator+(const J&a,const J&b){return J(a.v+b.v,a.d+b.d,a.h+b.h);}
inline J operator-(const J&a,const J&b){return J(a.v-b.v,a.d-b.d,a.h-b.h);}
inline J operator-(const J&a){return J(-a.v,-a.d,-a.h);}
inline J operator*(const J&a,const J&b){return J(a.v*b.v,a.v*b.d+a.d*b.v,a.v*b.h+a.d*b.d+a.h*b.v);}
inline J jinv(const J&a){I r=inv(a.v),r2=square(r);return J(r,-a.d*r2,square(a.d)*r2*r-a.h*r2);}
inline J operator/(const J&a,const J&b){return a*jinv(b);}
struct State { J x,y,z; };
struct Acc { I curv,m0,m1,m2; uint64_t leaves=0; };
inline Acc plus(const Acc&a,const Acc&b){return {a.curv+b.curv,a.m0+b.m0,a.m1+b.m1,a.m2+b.m2,a.leaves+b.leaves};}
struct Eval {
    J q; int depth;
    Eval(I t,int r):q(t*I(0.0625),I(0.0625),I(0)),depth(r){}
    J weight(const State& Q,int a,int b,J&det,J&A,J&C,J&zq)const{
        A=J(a*0.5)-Q.x; C=J(b*0.5)-Q.y; zq=Q.z-q;
        det=A*C-zq*zq;
        return J(double(a*b))*det;
    }
    State next(const J& det,const J&A,const J&C,const J&zq)const{
        const J bb(0.125),bb2(0.015625);
        J rd=jinv(det);
        return {bb2*C*rd,(q*q*C+J(0.25)*q*zq+bb2*A)*rd,
                bb*(q*C+bb*zq)*rd};
    }
    Acc run(int level,const State&Q,const J&p)const{
        if(level==depth){
            I b0(0),b1(0),b2(0);
            for(int a:{-1,1})for(int b:{-1,1}){
                J det,A,C,zq; J g=weight(Q,a,b,det,A,C,zq);
                if(g.v.l<=0)throw std::runtime_error("nonpositive complete event");
                I lg=log_i(I(4)*g.v);
                b0=b0-g.v*lg;
                b1=b1-g.d*lg;
                b2=b2-g.h*lg-I(0.5)*square(g.d)/g.v;
            }
            // J.h is the coefficient of dt^2, i.e. half the second derivative.
            // The factor 1/2 per original coordinate cancels the factor 2 here.
            I c=p.h*b0+p.d*b1+p.v*b2;
            return {c,p.v,p.d,p.h,1};
        }
        std::array<Acc,4> acc; int i=0;
        for(int a:{-1,1})for(int b:{-1,1}){
            J det,A,C,zq; J g=weight(Q,a,b,det,A,C,zq);
            if(g.v.l<=0)throw std::runtime_error("nonpositive branch weight");
            State R=next(det,A,C,zq);
            acc[i++]=run(level+1,R,p*g);
        }
        return plus(plus(acc[0],acc[1]),plus(acc[2],acc[3]));
    }
    Acc operator()()const{return run(0,State{},J(1));}
};
struct Node {int id;I t;};
int main(int argc,char**argv){
    try{
        if(argc<3){std::cerr<<"usage: certify_nodes nodes.tsv out.tsv [threads=1] [only_id=-1] [wall_cap=1800]\n";return 2;}
        std::fesetround(FE_TONEAREST);
        if(std::fegetround()!=FE_TONEAREST)throw std::runtime_error("rounding mode");
        for(int j=0;j<16;++j)ODD[j]=I(1)/I(double(2*j+1));
        int threads=argc>3?std::stoi(argv[3]):1, only=argc>4?std::stoi(argv[4]):-1;
        double cap=argc>5?std::stod(argv[5]):1800;
        if(threads<1||threads>4)throw std::runtime_error("1..4 threads only");
        std::ifstream fi(argv[1]);if(!fi)throw std::runtime_error("missing input");
        std::vector<Node> nodes;int id;std::string lo,hi;
        while(fi>>id>>lo>>hi){if(only>=0&&id!=only)continue;nodes.push_back({id,I(std::stod(lo),std::stod(hi))});}
        std::set<int> done;
        {std::ifstream old(argv[2]);std::string line;while(std::getline(old,line)){if(line.empty()||line[0]=='#')continue;std::istringstream is(line);int j;if(is>>j)done.insert(j);}}
        nodes.erase(std::remove_if(nodes.begin(),nodes.end(),[&](Node n){return done.count(n.id);}),nodes.end());
        std::ofstream out(argv[2],std::ios::app);if(!out)throw std::runtime_error("output open");
        std::mutex mu;std::atomic<bool> stopped(false),failed(false);
        auto start=std::chrono::steady_clock::now();
        double cpu0=double(std::clock())/CLOCKS_PER_SEC;
        omp_set_num_threads(threads);
        #pragma omp parallel for schedule(dynamic,1)
        for(size_t k=0;k<nodes.size();++k){
            if(stopped.load()||failed.load())continue;
            if(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>cap){stopped=true;continue;}
            try{
                std::fesetround(FE_TONEAREST);
                auto t0=std::chrono::steady_clock::now();
                const Node n=nodes[k];Acc a=Eval(n.t,9)();
                if(!(a.m0.l<=1&&a.m0.h>=1&&a.m1.l<=0&&a.m1.h>=0&&a.m2.l<=0&&a.m2.h>=0))throw std::runtime_error("normalization jets not enclosed");
                if(a.leaves!=262144)throw std::runtime_error("missing complete future word");
                double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
                std::lock_guard<std::mutex> lk(mu);
                out<<n.id<<" "<<std::hexfloat<<a.curv.l<<" "<<a.curv.h<<" "<<a.m0.l<<" "<<a.m0.h<<" "<<a.m1.l<<" "<<a.m1.h<<" "<<a.m2.l<<" "<<a.m2.h<<std::defaultfloat<<" "<<std::setprecision(10)<<secs<<" "<<a.leaves<<"\n";out.flush();
                std::cout<<n.id<<" ["<<std::setprecision(15)<<a.curv.l<<","<<a.curv.h<<"] width="<<a.curv.h-a.curv.l<<" seconds="<<secs<<std::endl;
            }catch(const std::exception&e){std::lock_guard<std::mutex> lk(mu);std::cerr<<"NODE_FAILURE "<<nodes[k].id<<" "<<e.what()<<std::endl;failed=true;}
        }
        struct rusage ru;getrusage(RUSAGE_SELF,&ru);
        double wall=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout<<"SUMMARY wall="<<wall<<" cpu="<<(double(std::clock())/CLOCKS_PER_SEC-cpu0)<<" max_rss_kib="<<ru.ru_maxrss<<" threads="<<threads<<" stopped="<<stopped<<" failed="<<failed<<std::endl;
        return failed?1:stopped?3:0;
    }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}
