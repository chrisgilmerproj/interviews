package main

import (
	"bufio"
	"encoding/csv"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

func dtToISO8601Est(dtStr string) string {
	/*
	   * The Timestamp column should be formatted in ISO-8601 format.
	   * The Timestamp column should be assumed to be in US/Pacific time;
	     please convert it to US/Eastern.

	   4/1/11 11:00:00 AM
	*/
	PDT, _ := time.LoadLocation("America/Los_Angeles")
	dtObj, _ := time.ParseInLocation("1/_2/06 3:04:05 PM", dtStr, PDT)
	EST, _ := time.LoadLocation("America/New_York")
	return dtObj.In(EST).Format(time.RFC3339)
}

func zipToFiveDigits(zipCode string) string {
	/*
	   * All ZIP codes should be formatted as 5 digits. If there are less
	     than 5 digits, assume 0 as the prefix.
	*/
	padSize := 5 - len(zipCode)
	return strings.Repeat("0", padSize) + zipCode
}

func uppercaseNames(name string) string {
	/*
	   * All name columns should be converted to uppercase. There will be
	     non-English names.
	*/
	return strings.Title(name)
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

func hmsToSeconds(hmsTime string) string {
	/*
	   * The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS
	     format (where MS is milliseconds); please convert them to a floating
	     point seconds format.
	*/
	time := strings.Split(hmsTime, ":")
	hours, _ := strconv.ParseFloat(time[0], 64)
	minutes, _ := strconv.ParseFloat(time[1], 64)
	seconds, _ := strconv.ParseFloat(time[2], 64)
	total := hours + 3600 + minutes*60 + seconds
	return strconv.FormatFloat(total, 'f', -1, 64)
}

func totalTime(fooDuration, barDuration string) string {
	/*
	   * The column "TotalDuration" is filled with garbage data. For each
	     row, please replace the value of TotalDuration with the sum of
	     FooDuration and BarDuration.
	*/
	newFoo, _ := strconv.ParseFloat(fooDuration, 64)
	newBar, _ := strconv.ParseFloat(barDuration, 64)
	return strconv.FormatFloat(newFoo+newBar, 'f', -1, 64)
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
	var header []string
	r := csv.NewReader(bufio.NewReader(os.Stdin))
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
					// This works because of the order of CSV fields
					newElement = totalTime(newRecord[4], newRecord[5])
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
