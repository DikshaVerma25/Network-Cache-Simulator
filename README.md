# Network-Cache-Simulator

An event-driven simulator for a network cache system.
An institutional network
connected to the wider Internet via an access link. 

- There are **N** files (e.g., web page objects), originally residing in far-
away Internet (origin) servers. **N** is large, e.g., **N = 10000**.
- The institutional users make requests for the files.
- For the intended objective, there is no need to distinguish the origin
servers. You can assume there is a single origin server. Similarly,
you can assume there is a single user.
- The user makes file requests according to a Poisson process with rate
**λ** requests per second. Each request is for file **_i_** with probability pi.
- We care about the response time, which is the duration from the
time of the request till the time the file is received by the user.
- There is a cache server in the institution network. A user request
goes to the cache first. If the cache contains the requested file, it
transmits the file to the user.

- If the cache does not have the requested file, the request goes to the
origin server in the Internet. After the origin server replies with the
requested file, the file goes to the cache first and is cached, and then
goes to the user.
- File i has a size S<sub>_i_</sub>, which is a sample drawn from a Pareto distribu-
tion (heavy tail), FS, with mean **μ** (e.g., **μ** = 1 MB).
- The probability p<sub>_i_</sub> reflects the popularity of file i. The pi’s are gen-
erated as follows. For _i_ = 1,...,N, draw q<sub>_i_</sub> independently from
another Pareto distribution, F<sub>_p_</sub>. Let p<sub>_i_</sub> = q<sub>_i_</sub> / ∑j q<sub>_j_</sub>, so that each p<sub>_i_</sub>
is a probability.
- Suppose the resource limitation is at the access link in the in-bound
direction. Its bandwidth is denoted R<sub>_a_</sub>, which is a constant (e.g.,
R<sub>_a_</sub> = 15 Mbps). We do not need to model the out-bound bandwidth,
since the small request messages do not consume much bandwidth.
- The institution network bandwidth is R<sub>_c_</sub> everywhere, which is a
constant (e.g., R<sub>_c_</sub> = **100** or **1000** Mbps).
- In the in-bound direction at the access link, there is a first-in-first-
out (_FIFO_) queue with infinite capacity. The returned files enter the
_FIFO_ queue and will be transmitted by the access link in order.
- Assume the propagation time within the institution network is **0**.
- The round-trip (propagation) time between the institution network
and the origin server is **_D_**, which is a random variable with a log-
normal distribution.
- If a file _i_ is served from the cache, the response time includes only
the transmission time from the cache, which is equal to S<sub>_i_</sub>/R<sub>_c_</sub>.
- If a file _i_ is not in the cache at the time of a request, the following
count towards the response time: the round-trip time in the Internet
**D**, the queueing delay at the **FIFO** queue, the transmission time at
the access link, and the transmission time from the cache.
Note that after file _i_ is completely transmitted from the access
link, it is immediately cached at the cache server (which may involve
replacing some cached files). After an additional time S<sub>_i_</sub>/R<sub>_c_</sub>, it is
received by the user.
# Project Objective: Evaluate Cache Replacement Policies
- The cache storage capacity is **C**, with **C** < ∑**N**
_i_=1 S<sub>_i_</sub>.
- Replacement Policies: Oldest First/Least-Popular First; Largest First;
some combinations of the above. You are encouraged to do some
quick research on other replacement policies and evaluate additional
policies. You can even design and evaluate your own replacement
policy.
- Performance metric: the average response time experienced by the
user.
