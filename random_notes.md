# Random Notes

## Heap

- Heap is allocated with `mmap` and is aligned to [`HEAP_MAX_SIZE`](https://github.com/bminor/glibc/blob/a704fd9a133bfb10510e18702f48a6a9c88dbbd5/malloc/arena.c#L71-L73), defined to be [`2 * DEFAULT_MMAP_THRESHOLD_MAX`](https://github.com/bminor/glibc/blob/a704fd9a133bfb10510e18702f48a6a9c88dbbd5/malloc/arena.c#L31). [`DEFAULT_MMAP_THRESHOLD_MAX`](https://man7.org/linux/man-pages/man3/mallopt.3.html) is `4*1024*1024*sizeof(long)` on 64-bit systems, which is `0x2000000`, so the per-thread heap that's mmap'd will always be aligned to `0x4000000`.


