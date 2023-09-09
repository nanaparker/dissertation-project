# dissertation-project
This repository contains files used for my Masters dissertation project, the Comprehensive Defence System, which involved the combination of features from the Anti-Virus and Vulnerability Scanner.

There are two primary components:
- The main Comprehensive Defence System, which allows the user to perform anti-virus and vulnerability assessment scans.
- A Real Time Detection system which, once activated, alerts the user of any malicious files which have been introduced to the system.

**Anti-Virus Scanner** 
This utilizes Signature-based detection and compares the hashes of files being scanned with malicious hashes in a stored file.

**Vulnerability Scanner**
Here, the system checks for the OS version and alert the user when the device would stop receiving updates (if it hasn't already)
Then it would check for folders containing whitespace including those vulnerable to the Unquoted Service Path vulnerability
Finally, it performs a port scan
