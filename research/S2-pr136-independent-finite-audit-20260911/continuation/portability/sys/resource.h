#ifndef S2_WINDOWS_SYS_RESOURCE_H
#define S2_WINDOWS_SYS_RESOURCE_H

// Windows-only compatibility for the author's end-of-run telemetry.
// The production arithmetic does not depend on getrusage or ru_maxrss;
// peak working set is recorded by the external PowerShell monitor instead.
#define RUSAGE_SELF 0

struct rusage {
    long ru_maxrss;
};

inline int getrusage(int, rusage* usage) {
    if (usage) usage->ru_maxrss = 0;
    return 0;
}

#endif
