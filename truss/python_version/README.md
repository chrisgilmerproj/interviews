# CSV Nornalizer

Nornalize CSV data

## Quick Start

You will need python3 to run this code.  No dependencies should be necessary.

```
$ ./csv_normalizer.py sample.csv
$ ./csv_normalizer.py sample-with-broken-utf8.csv
```

You can also choose to run it this way:

```
$ python3 csv_normalizer.py sample.csv
$ python3 csv_normalizer.py sample-with-broken-utf8.csv
```

## Optional File Out

If you don't want the data to go to stdout then just include another filename:

```
$ ./csv_normalizer.py sample.csv outfile.csv
```

## Help

Help information is available with the `-h` flag:

```
$ ./csv_normalizer.py -h
usage: csv_normalizer.py [-h] [infile] [outfile]

CSV Normalizer

positional arguments:
  infile
  outfile

  optional arguments:
    -h, --help  show this help message and exit
```
