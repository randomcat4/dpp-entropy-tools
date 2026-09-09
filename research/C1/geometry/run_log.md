# Arithmetic run log

All substantive arithmetic ran in the isolated geometry server directory.
No GPU, no package installation, and no other agent's process was stopped.
The shareable commands below use relative files and an interpreter variable;
they contain no access endpoint or credential.

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python probe.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python sparse_probe.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python sparse_detail.py

Python 3.12.3, mpmath 1.3.0, Linux x86_64. probe.py PID 163575,
100 decimal digits, exit 0; sparse_probe.py PID 163959, 110 decimal
digits, exit 0; sparse_detail.py PID 164324, 100 decimal digits, exit 0.
The detail script records deliberately retained failed theory predictions.
Full inputs and resulting values are in the corresponding JSON outputs.

An initial probe run PID 163533 completed, but its shell status recorder
was improperly escaped across shells. It was rerun once solely to obtain
an unambiguous exit record; the retained run is PID 163575. All owned jobs
have exited. No timed or recurring continuation was created.
