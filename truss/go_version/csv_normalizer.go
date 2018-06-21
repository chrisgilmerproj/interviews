package main

import (
	"bufio"
	"encoding/csv"
	"io"
	"log"
	"os"
)

func dtToISO8601Est(dt_str string) string {
	/*
	   * The Timestamp column should be formatted in ISO-8601 format.
	   * The Timestamp column should be assumed to be in US/Pacific time;
	     please convert it to US/Eastern.

	   4/1/11 11:00:00 AM
	*/
	// dt_obj = datetime.datetime.strptime(dt_str, '%m/%d/%y %H:%M:%S %p')
	// dt_obj = dt_obj + datetime.timedelta(hours=TZ_OFFSET)
	// return datetime.datetime.isoformat(dt_obj)
	return dt_str
}

func zipToFiveDigits(zip_code string) string {
	/*
	   * All ZIP codes should be formatted as 5 digits. If there are less
	     than 5 digits, assume 0 as the prefix.
	*/
	//return "{0:05d}".format(int(zip_code))
	return zip_code
}

func uppercaseNames(name string) string {
	/*
	   * All name columns should be converted to uppercase. There will be
	     non-English names.
	*/
	//return name.title()
	return name
}

func addressValidation(address string) string {
	/*
	   * The Address column should be passed through as is, except for
	     Unicode validation. Please note there are commas in the Address
	     field; your CSV parsing will need to take that into account. Commas
	     will only be present inside a quoted string.
	*/
	return address
}

func hmsToSeconds(hms_time string) string {
	/*
	   * The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS
	     format (where MS is milliseconds); please convert them to a floating
	     point seconds format.
	*/
	// hours, minutes, seconds = hms_time.split(':')
	// return float(hours) + 3600 + float(minutes) * 60 + float(seconds)
	return hms_time
}

func totalTime(foo_duration, bar_duration int) int {
	/*
	   * The column "TotalDuration" is filled with garbage data. For each
	     row, please replace the value of TotalDuration with the sum of
	     FooDuration and BarDuration.
	*/
	return foo_duration + bar_duration
}

func unicodeReplacement(text string) string {
	/*
	   * The column "Notes" is free form text input by end-users; please do
	     not perform any transformations on this column. If there are invalid
	     UTF-8 characters, please replace them with the Unicode Replacement
	     Character.
	*/
	return text
}

func main() {
	filename := "../takehome/problem_set/sample.csv"
	csvFile, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	var header []string
	r := csv.NewReader(bufio.NewReader(csvFile))
	w := csv.NewWriter(os.Stdout)
	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}
		// The header is expected and will come first
		if len(header) == 0 {
			header = record
			w.Write(header)
			w.Flush()
			if err := w.Error(); err != nil {
				log.Fatal(err)
			}
		} else {
			var newRecord []string
			var newElement string
			for index, element := range record {
				switch field := header[index]; field {
				case "Timestamp":
					newElement = dtToISO8601Est(element)
				case "Address":
					newElement = addressValidation(element)
				case "ZIP":
					newElement = zipToFiveDigits(element)
				case "FullName":
					newElement = uppercaseNames(element)
				case "FooDuration":
					newElement = hmsToSeconds(element)
				case "BarDuration":
					newElement = hmsToSeconds(element)
				case "TotalDuration":
					newElement = unicodeReplacement(element)
				case "Notes":
					newElement = unicodeReplacement(element)
				}
				newRecord = append(newRecord, newElement)
			}
			w.Write(newRecord)
			w.Flush()
			if err := w.Error(); err != nil {
				log.Fatal(err)
			}
		}
	}
}
