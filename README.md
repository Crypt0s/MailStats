MailStats
=========

A collection of scripts that allow a user to download an IMAP folder and perform statistical analysis on the resulting set of emails.


Potential Issues
================

> Only Tested on GMAIL
> Uses SSL IMAP (Changable) in the downloader
> Have not tested memory usage


Requirements
============
Needs ZODB to run (this is how it stores the mail messages to disk)
Should be as easy as:
    yum install python-ZODB3


HOW TO RUN
==========

Set your settings in settings.py
run downloader to download the emails to disk
run stats.py to get some statistics from the ZODB database of emails
