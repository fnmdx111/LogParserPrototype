Log parser prototype
====================

Usage
-----

e.g.
    log = log_parser.main()
    sum(map(lambda x: log.time_slices[x].requests['line!live'].request_count,
            range(24)))
and such


