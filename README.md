# Newest-Kogama-PID-Finder
Simple tool to track the last profile that was created, perhaps you can create rare ID's.

- Checks the given profile ID.
It retrieves the page content, searches for specific script tags to extract the creation date and breadcrumb data (used to determine the profile creation details). It returns a tuple indicating whether the profile was found, breadcrumb data, and the creation date.

- Converts date strings from UTC format to the system's local timezone and formats it for display.

- Determines the next profile ID to check based on how old the current profile is, using various thresholds to decide the step increment.

- Attempts to find the most recently created profile by iterating through profile IDs starting from a known recent ID and adjusting the algorythm's step size based on the profile creation times.

- Continuously checks profiles starting from a given ID, printing out details of each newly created profile.

- extra: Retrieves the last online timestamp for a specified profile ID or URL, converting it to the local timezone for display.


![Screenshot](https://github.com/xazitya/Newest-PID-Finder-/assets/82046838/52ebe511-3a5c-43ee-96bf-dab2d607e146)

- Requirements:

  -Python 3.11.9

  -bs4 (BeautifulSoup)

  -pytz


- Usage

  -python NewestPID.py
