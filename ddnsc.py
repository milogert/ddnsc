#!/bin/python2

import base64
from email.mime.text import MIMEText
import logging
import re
import smtplib
import urllib
import urllib2
import MySQLdb

from collections import defaultdict


"""
  Right now the only options for variables in the url are:

    {domain}
    {subdomain}
    {ip}
    {extras}

  More will come in the future.
"""


def setupUrl(theRows, theIp):
  """Function to setup the url based on the rows passed in."""

  aDict = {} 

  # Loop through each row.
  for aRow in theRows:

    aDict["subdomain"] = aRow[1]
    aDict["domain"] = aRow[2]
    aDict["username"] = aRow[3]
    aDict["password"] = aRow[4]
    aDict["ip"] = aRow[5]
    aDict["api"] = aRow[7]

    # Only update if the current ip is different from the stored one.
    if aDict["ip"] != theIp:

      aDict["ip"] = theIp

      # Format the url properly.
      aUrl = aDict["api"].format(**aDict)

      print("Setup url as: ", aUrl)

      # Update the ip with the url.
      aPage = updateIp(aUrl, aDict["username"], aDict["password"])

      # Do something with the response.
      manageResponse(aPage, aDict)


def updateIp(theUrl, theUser, thePass):
  """Update the ip."""

  # Setup the request header.
  request = urllib2.Request(theUrl)

  # User agent.
  userAgent = "Python-urllib/2.6"
  request.add_header("User-Agent", userAgent)

  # Username and password, if present.
  if theUser != "" and thePass != "":
    base64string = base64.encodestring('%s:%s' % (theUser, thePass)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

  # Make the request.
  response = urllib2.urlopen(request)

  resp = response.read()

  print("Got the response of " + resp)

  # Read the page.
  return resp


def manageResponse(theResp, theDict):
  """Manage the response we got from the dns provider."""

  good = ["good", "nochg"]
  bad = ["nohost", "badauth", "notfqdn", "badagent", "abuse", "911"]

  # Do stuff with the results.
  if any(s in theResp for s in good):
    # Make a cursor.
    c = _myConn.cursor()

    # Select all the data.
    data = (theDict["ip"], theResp, theDict["username"], theDict["password"],)
    result = c.execute(
      """
          UPDATE ddns__credentials
          SET ip = %s, response = %s
          WHERE username = %s AND password = %s
      """,
      data
    )

    # # Commit the data.
    _myConn.commit()

    print("We are good.")

    print(theResp)
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
  request = urllib2.urlopen("https://freegeoip.net/json/").read()
  return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)[0]




# Open db connection.

# Query.

# Loop through each result.

  # Curl on setup.

  # Send an email if config'd.

  # Log response

# Close database.








if __name__ == '__main__':
  # Create a new object.
  #ddncs = DDNSClient()

  # Get the current ip address.
  currentip = findIp()

  print("ii Found ip is " + currentip)

  # Make a cursor.
  c = _myConn.cursor()

  # Select all the data.
  c.execute("""
    SELECT *
    FROM ddns__credentials;
  """)

  # Get all the data.
#  for row in c.fetchall():
#    if currentip != row[3]:
#      updateIp(currentip, row[0], row[1], row[2], row[3])

  setupUrl(c.fetchall(), currentip)

  # Close the database.
  _myConn.close()
