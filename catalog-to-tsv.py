#!/usr/bin/env python3
import requests
import sys

'''
WARNING: This is the ugliest and least elegant code I have ever written. Please do not take this to be representative of my value as a human being.

This file scrapes data from collegecatalog.uchicago.edu to find course information for the supplied major,
then prints out the information in tsv format, which can be directed to a file.
By default, this script formats the course number as a link for copy/pasting to Excel or Google Sheets.
The `--nolink` argument can be supplied to stop this.
This script relies on a bunch of fixed strings and assumptions about what data the server will send over.
It is therefore very vulnerable to any changes in formatting on the website.
Please do not read this code and think less of me because of it; I promise the code I write is normally nicer.

Usage is simply `catalog-to-tsv.py [subject]` with an optional --nolink argument.
Since it's 2am and I have actual work to do, the --nolink thing can only be used as the second argument.
Also, the name of the subject comes from the URL of the catalog page.
For example, English is 'englishlanguageliterature' and not 'english'.

Each entry lists, in order:
- The course number
- The course name
- Whether the course is offered in fall, then winter, then spring, then summer
- Whether the years the course is offered in alternate
- Instructors
- Prerequisites
- Equivalent courses
- The number of units
- Notes

The data also has a header row.
'''

catalog_url = 'http://collegecatalog.uchicago.edu/thecollege/'
if len(sys.argv) == 1:
    print('usage: catalog-to-tsv.py <major> [--nolink]')
    exit()
major = sys.argv[1]
nolink = False
if len(sys.argv) > 2:
    if sys.argv[2] == '--nolink':
        nolink = True
    else:
        print('usage: catalog-to-tsv.py <major> [--nolink]')
url = catalog_url + major + '/'
pagetext = requests.get(url).text

if 'We’ve recently redesigned the College Catalog website, and many pages have been updated and moved.' in pagetext:
    print('Error: Please supply a valid major name (get these from the URLs of the college catalog pages).')
    exit()

lines = pagetext.split('\n')

# Searches through occurrences of a certain string to mark the start of each course description.
entries = []
for i in range(len(lines)):
    if 'class="courseblocktitle' in lines[i]:
        entries.append(i)

# Parses the page text to find the endpoint of class descriptions.
# Super inefficient since it goes through the whole thing almost 3 times but whatever
# This prevents weirdness later on
last = 0
for line in lines:
    if '<div class="contacts">' in line:
        last = lines.index(line)
        break
entries.append(last)

# Extracts info
courses = []
for entry in entries[:len(entries) - 1]:
    # First, cleans up the line with the course number, title, and units.
    s = lines[entry]
    s = s.replace('<p class="courseblocktitle"><strong>', '') \
         .replace('</strong></p><p class="courseblockdesc">', '') \
         .replace(' Units', '') \
         .replace('.', '') \
         .replace('&#160;', ' ') \
         .replace('\xa0', ' ') \
         .replace('\u2029', '')
    # The number/title/units are separated by 2 spaces.
    # Sequences are not necessary, so to filter them out, these lines see if the part of the string before
    # the first double-space is greater than 10, which is the length of a course number.
    # If it is, then it gets filtered out.
    if s.index('  ') > 10:
        # print('Sequence filtered:', s)
        continue

    # Here the "info" list gets created which contains all the information for this entry.
    # It starts out with the number, title, and units for a given course.
    splitstring = s.split('  ')
    info = splitstring[0:2]

    # If the nolink argument was not supplied, then the course number become formatted as a link.
    # This link links to a search on the college catalog, which supplies the course description.
    if not nolink:
        info[0] = '=HYPERLINK("' + \
                'http://collegecatalog.uchicago.edu/search/?P={}'.format(info[0].replace(' ', "%20")) + \
                '", "' + \
                info[0] + \
                '")'

    # Next, the script searches through all the lines between the current and next entry;
    # this part appends 'Y' or 'N' four times, depending on if the course is offered in fall/winter/spring/summer.
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'Terms Offered' in lines[i]:
            # This checks that the terms offered is not 'TBD' or 'TBA' or whatever.
            if 'Autumn' in lines[i] or 'Winter' in lines[i] or 'Spring' in lines[i] or 'Summer' in lines[i]:
                for term in ['Autumn', 'Winter', 'Spring', 'Summer']:
                    if term in lines[i]:
                        info.append('Y')
                    else:
                        info.append('N')
    
    # If there is nothing under 'terms offered,' then this line appends empty strings to make the lengths match.
    while len(info) < 6:
            info.append('')

    # Again, search through lines, this time to find if the given class is given in alternating years.
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'alternate years' in lines[i].lower() or 'alternating years' in lines[i].lower():
            # Append yes if yes...
            info.append('Y')
            break
    
    # ... and no if no.
    while len(info) < 7:
        info.append('N')

    # Same thing but for instructors.
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'Instructor(s)' in lines[i]:
            filtered = lines[i].replace('&#160;', ' ').replace('\xa0', ' ').replace('<br />', ' ')
            words = filtered.split()
            instructors = []
            for word in words[1:]:
                if word == 'Terms':
                    break
                instructors.append(word)
            info.append(' '.join(instructors))

    # Again, appends empty strings in case instructor names are not given.
    while len(info) < 8:
        info.append('')

    # Same again for prerequisites
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'Prerequisite(s):' in lines[i]:
            info.append(lines[i][lines[i].index('Prerequisite(s):'):].replace('Prerequisite(s): ', '') \
                                                                     .replace('<br />', '') \
                                                                     .replace('\u2029', '') \
                                                                     .replace('</p><p class="courseblockdetail">', '') \
                                                                     .replace('<br/>', ''))
            break

    # in case prereqs not found etc etc
    while len(info) < 9:
        info.append('')

    # equivalent courses
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'Equivalent Course(s)' in lines[i]:
            info.append(lines[i][lines[i].index('Equivalent Course(s):'):].replace('Equivalent Course(s): ', '') \
                                                                          .replace('<br />', ''))
            break

    # you know
    while len(info) < 10:
        info.append('')

    # Here it finally appends the number of units. I put it here since basically every course is 100 units so it doesn't really matter.
    info.append(splitstring[2])

    # and same thing for extra notes.
    for i in range(entry, entries[entries.index(entry) + 1]):
        if 'Note(s)' in lines[i]:
            info.append(lines[i].replace('Note(s): ', '') \
                                .replace('<br />', '') \
                                .replace('<br/>', '') \
                                .replace('</p><p class="courseblockdetail">', ''))
            break

    # Append all the course information to the course list.
    # A final thingy to make all the entries the same length is no longer needed, since this is the last thing.
    courses.append(info)

# And finally, print everything out in tsv format.
print('"Number"\t"Title"\t"F"\t"W"\t"S"\t"S"\t"Alt"\t"Instructors"\t"Prerequisites"\t"Equivalent Courses"\t"Units"\t"Notes"')
for course in courses:
    for i in range(len(course) - 1):
        print(course[i], end='\t')
    print(course[len(course) - 1], end='\n')
