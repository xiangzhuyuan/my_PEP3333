## [Thread Support](#id35)

Thread support, or lack thereof, is also server-dependent.
Servers that can run multiple requests in parallel, **should** also
provide the option of running an application in a single-threaded
fashion, so that applications or frameworks that are not thread-safe
may still be used with that server.
