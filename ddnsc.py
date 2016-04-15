#!/usr/bin/env python

import base64
# from email.mime.text import MIMEText
import re
# import smtplib
import urllib2

from model import engine, Record


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# Setup the log levels.
class Level:
    OFF = 0
    LOW = 1
    MID = 2
    HIGH = 3

logLevel = 0


def setupUrl(theRows, theIp):
    """Function to setup the url based on the rows passed in."""

    for aRow in theRows:
        # Only update if the current ip is different from the stored one.
        if aRow.ip == theIp:
            continue

        aRow.ip = theIp

        # Format the url properly.
        aUrl = aRow.api.format(**aRow.__dict__)

        print "Updating " + aRow.subdomain

        # Update the ip with the url.
        aPage = updateIp(aUrl, aRow.username, aRow.password)

        # Do something with the response.
        manageResponse(aPage, aRow)


def updateIp(theUrl, theUser, thePass):
    """Update the ip."""

    # Setup the request header.
    request = urllib2.Request(theUrl)

    # User agent.
    userAgent = "Python-urllib/2.6"
    request.add_header("User-Agent", userAgent)

    # Username and password, if present.
    if theUser == "" or thePass == "":
        return

    encode_str = '%s:%s' % (theUser, thePass)
    base64string = base64.encodestring(encode_str).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    # Make the request.
    response = urllib2.urlopen(request)

    resp = response.read()

    print("\tresponse: " + resp)

    # Read the page.
    return resp


def manageResponse(theResp, theRow):
    """Manage the response we got from the dns provider."""

    good = ["good", "nochg"]
    bad = ["nohost", "badauth", "notfqdn", "badagent", "abuse", "911"]

    # Do stuff with the results.
    if any(s in theResp for s in good):
        # Select all the data.
        theRow.response = theResp

        # Commit the data.
        session.add(theRow)
        session.commit()
    elif theResp in bad:
        # Email the error and exit.
        # Create the message.
        # msg = MIMEMultipart("alternative")

        # # Update the msg.
        # msg["Subject"] = _myEmail["subject"].format(subdomain)
        # msg["From"] = _myEmail["from"]
        # msg["To"] = _myEmail["to"]

        # # Add the html to the message.
        # msg.attach(MIMEText(_myEmail["text"].format(theResp), "plain"))
        # msg.attach(MIMEText(_myEmail["html"].format(theResp), "html"))

        # # Send the email through gmail.
        # server = smtplib.SMTP("smtp.gmail.com:587")
        # server.ehlo()
        # server.starttls()
        # server.login(_myEmail["from"], _myEmail["pass"])
        # server.sendmail(_myEmail["from"], _myEmail["to"], msg.as_string())
        # server.quit()
        print("no good")
    else:
        # Log that this should never happen.
        print("What happened?")


def findIp():
    """Find the current ip of the server."""
    return urllib2.urlopen('https://api.ipify.org').read()


def addEntry(*theArgList):
    """Adds an entry to the database."""
    print 'Adding entry:'
    for aArg in theArgList:
        print '\t' + aArg

    # Create a new record.
    new_r = Record(*theArgList)

    # Add the record to the database and commit.
    session.add(new_r)
    session.commit()


def _setLogLevel(theNum):
    global logLevel
    logLevel = theNum


if __name__ == '__main__':
    # Setup the argument parser.
    import argparse

    aParser = argparse.ArgumentParser(description="DDNSc")
    aParser.add_argument("-v", "--verbose", action="count")
    aCommand = aParser.add_mutually_exclusive_group(required=False)
    aCommand.add_argument("-a", "--add", nargs="*")
    aCommand.add_argument("-u", "--update", action="store_true")
    aCommand.add_argument("-l", "--look", nargs="?", const="all")
    aCommand.add_argument('--test', action='store_true')

    aArgs = aParser.parse_args()

    _setLogLevel(aArgs.verbose)
    print "ii Log level is " + str(logLevel)

    if logLevel >= Level.HIGH:
        print aArgs

    if aArgs.update:
        # Get the current ip address.
        currentip = findIp()

        print("ii Found ip is " + currentip)

        setupUrl(session.query(Record).all(), currentip)
    elif aArgs.add:
        addEntry(*aArgs.add)
    elif aArgs.look:
        if aArgs.look == "all":
            for aRecord in session.query(Record).all():
                print aRecord.__dict__
        else:
            print aArgs.look
    elif aArgs.test:
        findIp()
    else:
        aParser.print_help()
