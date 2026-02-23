# POSIX First

> Linux/BSD native — epoll, mmap, systemd

---

RULE: Use POSIX APIs directly for system operations
RULE: epoll (Linux) or kqueue (BSD) for async I/O
RULE: pthreads attributes when std::jthread insufficient
RULE: mmap for large allocations or shared memory
RULE: Systemd integration for services

```cpp
// File I/O - POSIX
int fd = open(path, O_RDONLY);
read(fd, buffer, size);
close(fd);

// Async I/O - epoll (Linux)
int epfd = epoll_create1(0);
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);
epoll_wait(epfd, events, max_events, timeout);

// Memory mapping
void* addr = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
munmap(addr, size);

// Systemd socket activation
int n = sd_listen_fds(0);
if (n > 0) {
    int fd = SD_LISTEN_FDS_START;
    // use socket passed by systemd
}
```

BANNED: Windows-specific APIs
