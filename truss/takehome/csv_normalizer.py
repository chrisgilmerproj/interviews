#! /usr/bin/env python3

"""
Please write a tool that reads a CSV formatted file on `stdin` and
emits a normalized CSV formatted file on `stdout`. Normalized, in this
case, means:

* The entire CSV is in the UTF-8 character set.
* The Timestamp column should be formatted in ISO-8601 format.
* The Timestamp column should be assumed to be in US/Pacific time;
  please convert it to US/Eastern.
* All ZIP codes should be formatted as 5 digits. If there are less
  than 5 digits, assume 0 as the prefix.
* All name columns should be converted to uppercase. There will be
  non-English names.
* The Address column should be passed through as is, except for
  Unicode validation. Please note there are commas in the Address
  field; your CSV parsing will need to take that into account. Commas
  will only be present inside a quoted string.
* The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS
  format (where MS is milliseconds); please convert them to a floating
  point seconds format.
* The column "TotalDuration" is filled with garbage data. For each
  row, please replace the value of TotalDuration with the sum of
  FooDuration and BarDuration.
* The column "Notes" is free form text input by end-users; please do
  not perform any transformations on this column. If there are invalid
  UTF-8 characters, please replace them with the Unicode Replacement
  Character.

You can assume that the input document is in UTF-8 and that any times
that are missing timezone information are in US/Pacific. If a
character is invalid, please replace it with the Unicode Replacement
Character. If that replacement makes data invalid (for example,
because it turns a date field into something unparseable), print a
warning to `stderr` and drop the row from your output.

You can assume that the sample data we provide will contain all date
and time format variants you will need to handle.
"""

import argparse
import csv
import datetime
import io
import sys


# Offset between PST and EST
# Used instead of introducing an outside dependnecy pytz
TZ_OFFSET = -3


def dt_to_iso8601_est(dt_str):
    """
    * The Timestamp column should be formatted in ISO-8601 format.
    * The Timestamp column should be assumed to be in US/Pacific time;
      please convert it to US/Eastern.

    4/1/11 11:00:00 AM
    """
    dt_obj = datetime.datetime.strptime(dt_str, '%m/%d/%y %H:%M:%S %p')
    dt_obj = dt_obj + datetime.timedelta(hours=TZ_OFFSET)
    return datetime.datetime.isoformat(dt_obj)


def zip_to_five_digits(zip_code):
    """
    * All ZIP codes should be formatted as 5 digits. If there are less
      than 5 digits, assume 0 as the prefix.
    """
    return "{0:05d}".format(int(zip_code))


def uppercase_names(name):
    """
    * All name columns should be converted to uppercase. There will be
      non-English names.
    """
    return name.title()


def address_validation(address):
    """
    * The Address column should be passed through as is, except for
      Unicode validation. Please note there are commas in the Address
      field; your CSV parsing will need to take that into account. Commas
      will only be present inside a quoted string.
    """
    return address


def hms_to_seconds(hms_time):
    """
    * The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS
      format (where MS is milliseconds); please convert them to a floating
      point seconds format.
    """
    hours, minutes, seconds = hms_time.split(':')
    return float(hours) + 3600 + float(minutes) * 60 + float(seconds)


def total_time(foo_duration, bar_duration):
    """
    * The column "TotalDuration" is filled with garbage data. For each
      row, please replace the value of TotalDuration with the sum of
      FooDuration and BarDuration.
    """
    return foo_duration + bar_duration


def unicode_replacement(text):
    """
    * The column "Notes" is free form text input by end-users; please do
      not perform any transformations on this column. If there are invalid
      UTF-8 characters, please replace them with the Unicode Replacement
      Character.
    """
    return text


def normalizer(infile, outfile):
    """
    Normalize CSV data from infile and place in outfile.

    :param infile: A file-like object with input data
    :param outfile: A file-like object where data will be written
    :return: None
    """
    reader = csv.DictReader(infile)
    header = reader.fieldnames

    writer = csv.DictWriter(outfile, header)
    writer.writeheader()
    for row in reader:
        new_row = {}
        # For bad data or parsing errors drop row
        try:
            for key in header:
                value = row[key]
                new_value = None
                if key == 'Timestamp':
                    new_value = dt_to_iso8601_est(value)
                elif key == 'Address':
                    new_value = address_validation(value)
                elif key == 'ZIP':
                    new_value = zip_to_five_digits(value)
                elif key == 'FullName':
                    new_value = uppercase_names(value)
                elif key == 'FooDuration':
                    new_value = hms_to_seconds(value)
                elif key == 'BarDuration':
                    new_value = hms_to_seconds(value)

                # This works because we are iterating through the file's headers in order
                elif key == 'TotalDuration':
                    new_value = total_time(new_row['FooDuration'], new_row['BarDuration'])
                elif key == 'Notes':
                    new_value = unicode_replacement(value)
                new_row[key] = new_value
            writer.writerow(new_row)
        except Exception:
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CSV Normalizer')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r', encoding='UTF-8', errors='replace'),
                        default=io.TextIOWrapper(sys.stdin.buffer, encoding='UTF-8', errors='replace'))
    parser.add_argument('outfile', nargs='?',
                        type=argparse.FileType('w', encoding='UTF-8'),
                        default=sys.stdout)
    args = parser.parse_args()
    normalizer(args.infile, args.outfile)
