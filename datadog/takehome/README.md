# Log Reader

Create a log reader that collects interesting stats.  See `PROBLEM.md` for more info.

## Quickstart

In one window start a log writer:

```
$ ./log_writer.py
```

In another window start the log reader:

```
$ ./log_reader.py
```

You should be able to start and stop the `log_writer.py` process and the reader should still work.

## Notes

- Without access to an apache server I ended up spending time writing my own mock-apache log service for testing.
- The stats per section could be better but for my minimal example it works ok
- There is no high-traffic warning, that is left to a future update but would work similar to the stats logic
- Tests should be easy to create now that I have a writer.  It would be simple enough to put it into an io.IOString
  object and use that as the test.
- I'd prefer to rewrite this with asyncio and manage the reading of the file in a separate thread from the stats
  display
- No time to use docker for testing, though it would have been fun.  I'd have liked to set up a docker compose
  file with both a simple apache server and the log parser, cross mount the log directory, and ship as a simple
  command line docker tool.
