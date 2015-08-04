import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

import pymysql.cursors


## Model Class ###############################################################
class Model:
  """
    Right now the only options for variables in the url are:

      {domain}
      {subdomain}
      {ip}
      {extras}

    More will come in the future.
  """

  # Email dictionary.

  def __init__(self):
    self._myEmail = {
        "text": "Error in update DDNS.\n\nError is: {}",
        "html": "Error in updating DDNS.\n\nError is: <pre>{}</pre>",
        "subject": "DDNS Update Error: {}",
        "from": "server@milogert.com",
        "pass": "servergothacked",
        "to": "milo@milogert.com"
    }

    self.myDbConn = pymysql.connect(
        host='milogert.com',
        user='milo',
        passwd='locatetimefarduck',
        db='personal',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # Set the edited status as false. This is for reloading rows.
    self.myEdited = False

  def __del__(self):
    """Destructor."""

    # Close the connection.
    self.myDbConn.close()

  def setEdited(self, theBool):
    """Method to tell the view if the model has been edited or not."""
    self.myEdited = theBool

  def getEdited(self):
    """Get the edited status of the model."""
    return self.myEdited

  def getRows(self):
    try:
      with self.myDbConn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `ddns__credentials`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except ValueError:
      # TODO
      pass

  def getRow(self, theKey):
    try:
      with self.myDbConn.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `ddns__credentials` where subdomain = %s"
        cursor.execute(sql, (theKey))
        result = cursor.fetchone()
        return result
    except ValueError:
      # TODO
      pass

  def addEntry(
      self,
      theSub,
      theDomain,
      theIp,
      theProvider,
      theUsername,
      thePassword,
      theApi,
      theExtras
  ):
    try:
      with self.myDbConn.cursor() as cursor:
        # Read a single record
        sql = """
          INSERT
          INTO `ddns__credentials`
          (`subdomain`, `domain`, `ip`, `provider`, `username`, `password`, `api`, `extras`)
          VALUES
          (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            theSub,
            theDomain,
            theIp,
            theProvider,
            theUsername,
            thePassword,
            theApi,
            theExtras
        ))

        self.myDbConn.commit()
    except ValueError:
      # TODO
      pass

  def updateEntry(
      self,
      theId,
      theSub,
      theDomain,
      theIp,
      theProvider,
      theUsername,
      thePassword,
      theApi,
      theExtras
  ):
    try:
      with self.myDbConn.cursor() as cursor:
        # Read a single record
        sql = """
          UPDATE `ddns__credentials`
          SET
          `subdomain`=%s,
          `domain`=%s,
          `ip`=%s,
          `provider`=%s,
          `username`=%s,
          `password`=%s,
          `api`=%s,
          `extras`=%s
          WHERE `id`=%s
        """
        cursor.execute(sql, (
            theSub,
            theDomain,
            theIp,
            theProvider,
            theUsername,
            thePassword,
            theApi,
            theExtras,
            theId
        ))

        self.myDbConn.commit()
    except ValueError:
      # TODO
      pass


  def deleteEntries(self, theIdList):
    """Method to delete entries in the database."""

    try:
      with self.myDbConn.cursor() as cursor:
        # Read a single record
        sql = "DELETE FROM `ddns__credentials` WHERE id in (%s)"
        s = ', '.join(list(map(lambda x: '%s', theIdList)))
        sql = sql % s
        print(sql)
        print(theIdList)
        print(sql % tuple(theIdList))
        cursor.execute(sql, (theIdList))

        self.myDbConn.commit()
    except ValueError:
      # TODO
      pass


  def setupUrl(self, theRows):
    """Function to setup the url based on the rows passed in."""

    # Loop through each row.
    for aRow in theRows:
      # Only update if the current ip is different from the stored one.
      if aRow["ip"] != findIp():
        # Format the url properly.
        aUrl = aRow["api"].format(**aRow)

        print("Setup url as: ", aUrl)

        # Update the ip with the url.
        aPage = updateIp(theUrl, aRow["username"], aRow["password"])

        # Do something with the response.
        manageResponse(aPage)


  def _updateIp(theUrl, theUser, thePass):
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

    # Read the page.
    return response.read()


  def _manageResponse(theResp):
    """Manage the response we got from the dns provider."""

    good = ["good", "nochg"]
    bad = ["nohost", "badauth", "notfqdn", "badagent", "abuse", "911"]

    # Do stuff with the results.
    if any(s in theResp for s in good):
      # Make a cursor.
      # c = _myConn.cursor()

      # Select all the data.
      # data = (currentip, theResp, username, password,)
      # result = c.execute(
      #   """
      #       UPDATE ddns__credentials
      #       SET ip = %s, response = %s
      #       WHERE username = %s AND password = %s
      #   """,
      #   data
      # )

      # # Commit the data.
      # _myConn.commit()

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


  def _findIp():
    """Find the current ip of the server."""
    request = urllib2.urlopen("http://checkip.dyndns.org").read()
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)[0]
##############################################################################


## MainWindow class ##########################################################
class MainWindow(tk.Toplevel):

  def __init__(self, master):
    # These are the headers to us up top.
    self.headers = ('subdomain', 'domain', 'ip', 'provider', 'response')

    tk.Toplevel.__init__(self, master)
    self.protocol('WM_DELETE_WINDOW', self.master.destroy)
    self.title("DDNS Client")
    # tk.Label(self, text='My Money').pack(side='left')
    # self.moneyCtrl = tk.Entry(self, width=8)
    # self.moneyCtrl.pack(side='left')

    # Menu bar.
    aMenuBar = tk.Menu(self)

    # File menu.
    aMenuFile = tk.Menu(aMenuBar, tearoff=0)
    aMenuBar.add_cascade(menu=aMenuFile, label='File')
    aMenuFile.add_command(label="Quit", command=master.destroy)

    # Edit menu.
    aMenuEdit = tk.Menu(aMenuBar, tearoff=0)
    aMenuBar.add_cascade(menu=aMenuEdit, label='Edit')
    aMenuEdit.add_command(label="Add...", command=self.startAdd)

    # Actually add the menu bar.
    self["menu"] = aMenuBar

    # Create the container to hold everything.
    container = ttk.Frame(self)
    container.pack(fill='both', expand=True, padx=10, pady=10)

    # create a treeview with dual scrollbars
    self.myTree = ttk.Treeview(container, columns=self.headers, show="headings")
    vsb = ttk.Scrollbar(container, orient="vertical", command=self.myTree.yview)
    hsb = ttk.Scrollbar(container, orient="horizontal", command=self.myTree.xview)
    self.myTree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    # self.myTree.bind('<1>', select_cmd)
    self.myTree.grid(column=0, row=0, rowspan=10, sticky='nsew')
    vsb.grid(column=1, row=0, rowspan=10, sticky='ns')
    hsb.grid(column=0, row=10, sticky='ew')

    aBtnAdd = ttk.Button(container)
    aBtnAdd.configure(text="Add", command=self.startAdd)
    aBtnAdd.grid(column=2, row=1, padx=25, pady=10)

    aBtnEdit = ttk.Button(container)
    aBtnEdit.configure(text="Edit", command=self.startEdit)
    aBtnEdit.grid(column=2, row=2, padx=25, pady=10)

    aBtnDelete = ttk.Button(container)
    aBtnDelete.configure(text="Delete", command=self.startDelete)
    aBtnDelete.grid(column=2, row=3, padx=25, pady=10)

    # Separator.
    aSep = ttk.Separator(container)
    aSep.grid(column=0, columnspan=3, row=11, padx=25, pady=25, sticky="ew")

    aBtnUpdate = ttk.Button(container)
    aBtnUpdate.configure(text="Update")
    aBtnUpdate.grid(column=2, row=12, padx=25, pady=25)

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

    # Create a model to use.
    # self.myModel = Model()

    # Initialize the table, since everything is created.
    self._setRows()


  def _setRows(self):
    # Get the rows from the database.
    aRows = myGlobalModel.getRows()

    # Setup the headers.
    for col in self.headers:
      self.myTree.heading(
          col,
          text=col,
          command=lambda c=col: self._sortby(self.myTree, c, 0)
      )
      # adjust the column's width to the header string
      self.myTree.column(col, width=tkFont.Font().measure(col.title()))

    # Setup the actual content.
    for item in aRows:
      ins = self.normalizeData(item)
      self.myTree.insert('', 'end', values=ins)
      # adjust column's width if necessary to fit each value
      for ix, val in enumerate(ins):
        col_w = tkFont.Font().measure(val)
        if self.myTree.column(self.headers[ix], width=None) < col_w:
          self.myTree.column(self.headers[ix], width=col_w)

    # Sort the rows by subdomain by default.
    self._sortby(self.myTree, "subdomain", False)


  def _sortby(self, tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: self._sortby(tree, col, \
        int(not descending)))


  def _clearRows(self):
    """Clear all the rows from the table."""
    for i in self.myTree.get_children():
      self.myTree.delete(i)


  def normalizeData(self, data):
    ret = []
    for item in self.headers:
      ret.append(data[item])
    return ret


  def startAdd(self):
    aAdd = AddEditWindow(self)

    # Make the window modal.
    aAdd.transient(self)
    aAdd.grab_set()
    self.wait_window(aAdd)

    if myGlobalModel.getEdited():
      # Update the table regardless.
      self._clearRows()
      self._setRows()

      # Set the edited status back.
      myGlobalModel.setEdited(False)


  def startEdit(self):
    try:
      if len(self.myTree.selection()) > 1:
        raise IndexError

      item = self.myTree.selection()[0]
      aKey = self.myTree.item(item, "values")[0]
      aRow = myGlobalModel.getRow(aKey)
      aEdit = AddEditWindow(self, aRow, True)

      # Make the window modal.
      aEdit.transient(self)
      aEdit.grab_set()
      self.wait_window(aEdit)

      if myGlobalModel.getEdited():
        # Update the table regardless.
        self._clearRows()
        self._setRows()

        # Set the edited status back.
        myGlobalModel.setEdited(False)
    except IndexError:
      tkMessageBox.showinfo("Select a Single Row", "Please select one single row.")


  def startDelete(self):
    try:
      # Get the perinent data.
      items = self.myTree.selection()
      aIdList = []

      for i, item in enumerate(items):
        aKey = self.myTree.item(item, "values")[0]
        aRow = myGlobalModel.getRow(aKey)

        # Extract the id.
        aIdList.append(aRow["id"])

      # Call the dialog.
      if tkMessageBox.askyesno("Delete Entry(ies)", "Should we delete the selected entries?"):
        myGlobalModel.deleteEntries(aIdList)

        # Update the table if we pressed yes.
        self._clearRows()
        self._setRows()
    except IndexError:
      tkMessageBox.showinfo("Select a Single Row", "Please select one single row.")

##############################################################################


## MainWindow class ##########################################################
class AddEditWindow(tk.Toplevel):

  def __init__(self, master, theRow=None, isEdit=False):
    tk.Toplevel.__init__(self, master)

    if isEdit:
      self.title("Editing " + theRow["subdomain"])
    else:
      self.title("Adding a New Entry")

    # Disable resizing.
    self.resizable(False, False)

    # Set the size.
    # self.minsize()
    self.isEdit = isEdit

    container = ttk.Frame(self)
    container.pack(fill='both', expand=True)

    # Create string variables to hold the value and to trace.
    self.aStrSub = tk.StringVar(container)
    self.aStrDomain = tk.StringVar(container)
    self.aStrIp = tk.StringVar(container)
    self.aStrProvider = tk.StringVar(container)
    self.aStrUsername = tk.StringVar(container)
    self.aStrPassword = tk.StringVar(container)
    self.aStrApi = tk.StringVar(container)

    # Add a trace to each one.
    self.aStrSub.trace('w', self._filledOut)
    self.aStrDomain.trace('w', self._filledOut)
    self.aStrIp.trace('w', self._filledOut)
    self.aStrProvider.trace('w', self._filledOut)
    self.aStrUsername.trace('w', self._filledOut)
    self.aStrPassword.trace('w', self._filledOut)
    self.aStrApi.trace('w', self._filledOut)

    # Create all the widgets.
    aLblSub = tk.Label(container, text="Subdomain", anchor=tk.W, padx=10, pady=10)
    self.aEntSub = tk.Entry(container, textvariable=self.aStrSub)
    aLblDomain = tk.Label(container, text="Domain", anchor=tk.W, padx=10, pady=10)
    self.aEntDomain = tk.Entry(container, textvariable=self.aStrDomain)
    aLblIp = tk.Label(container, text="IP Address", anchor=tk.W, padx=10, pady=10)
    self.aEntIp = tk.Entry(container, textvariable=self.aStrIp)
    aLblProvider = tk.Label(container, text="Provider", anchor=tk.W, padx=10, pady=10)
    self.aEntProvider = tk.Entry(container, textvariable=self.aStrProvider)
    aLblUsername = tk.Label(container, text="Username", anchor=tk.W, padx=10, pady=10)
    self.aEntUsername = tk.Entry(container, textvariable=self.aStrUsername)
    aLblPassword = tk.Label(container, text="Password", anchor=tk.W, padx=10, pady=10)
    self.aEntPassword = tk.Entry(container, textvariable=self.aStrPassword)
    aLblApi = tk.Label(container, text="Api", anchor=tk.W, padx=10, pady=10)
    self.aEntApi = tk.Entry(container, textvariable=self.aStrApi)
    aLblExtras = tk.Label(container, text="Extras", anchor=tk.W, padx=10, pady=10)
    self.aEntExtras = tk.Entry(container)
    self.aBtnSave = ttk.Button(container)
    self.aBtnSave.configure(text="Save Entry", command=self.saveEntry)
    aSep = ttk.Separator(container)
    aBtnCancel = tk.Button(container, text="Cancel", command=self.destroy)

    # Load values if editing is enabled.
    if theRow is not None:
      print("Loading values to edit:", theRow)
      self.aEntSub.insert(0, theRow["subdomain"])
      self.aEntDomain.insert(0, theRow["domain"])
      self.aEntIp.insert(0, theRow["ip"])
      self.aEntProvider.insert(0, theRow["provider"])
      self.aEntUsername.insert(0, theRow["username"])
      self.aEntPassword.insert(0, theRow["password"])
      self.aEntApi.insert(0, theRow["api"])
      self.aEntExtras.insert(0, theRow["extras"])
      self.aId = theRow["id"]

    # Pack everything into the grid.
    aLblSub.grid(column=0, row=0)
    self.aEntSub.grid(column=1, row=0, padx=10, pady=10)
    aLblDomain.grid(column=0, row=1)
    self.aEntDomain.grid(column=1, row=1, padx=10, pady=10)
    aLblIp.grid(column=0, row=2)
    self.aEntIp.grid(column=1, row=2, padx=10, pady=10)
    aLblProvider.grid(column=0, row=3)
    self.aEntProvider.grid(column=1, row=3, padx=10, pady=10)
    aLblUsername.grid(column=0, row=4)
    self.aEntUsername.grid(column=1, row=4, padx=10, pady=10)
    aLblPassword.grid(column=0, row=5)
    self.aEntPassword.grid(column=1, row=5, padx=10, pady=10)
    aLblApi.grid(column=0, row=6)
    self.aEntApi.grid(column=1, row=6, padx=10, pady=10)
    aLblExtras.grid(column=0, row=7)
    self.aEntExtras.grid(column=1, row=7, padx=10, pady=10)
    aSep.grid(column=0, columnspan=2, row=8, padx=25, pady=25, sticky="ew")
    self.aBtnSave.grid(column=1, row=9, padx=10, pady=10)
    aBtnCancel.grid(column=2, row=9, padx=10, pady=10)

    # Finally, set the button.
    self._filledOut()


  def _filledOut(self, *args):
    """This is intended to check if all the proper fields are filled out."""

    # Get the status of all the fields.
    aVerify = (
        self.aEntDomain.get() and
        self.aEntIp.get() and
        self.aEntProvider.get() and
        self.aEntUsername.get() and
        self.aEntPassword.get() and
        self.aEntApi.get()
    )

    # Get the regex of the ip address field.
    import re
    r = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}$")
    aVerify = aVerify and r.match(self.aEntIp.get())

    # Set the button to enabled or disabled.
    if aVerify:
      self.aBtnSave.config(state="normal")
    else:
      self.aBtnSave.config(state="disable")


  def saveEntry(self):
    """Pass all the collected data to the model."""

    # Collect all the data.
    aSub = self.aEntSub.get() if self.aEntSub.get() else ""
    aDomain = self.aEntDomain.get()
    aIp = self.aEntIp.get()
    aProvider = self.aEntProvider.get()
    aUsername = self.aEntUsername.get()
    aPassword = self.aEntPassword.get()
    aApi = self.aEntApi.get()
    aExtras = self.aEntExtras.get() if self.aEntExtras.get() else ""

    # Save the data appropriately.
    if(self.isEdit):
      myGlobalModel.updateEntry(
        self.aId,
        aSub,
        aDomain,
        aIp,
        aProvider,
        aUsername,
        aPassword,
        aApi,
        aExtras
      )
    else:
      myGlobalModel.addEntry(
        aSub,
        aDomain,
        aIp,
        aProvider,
        aUsername,
        aPassword,
        aApi,
        aExtras
      )

    myGlobalModel.setEdited(True)

    self.destroy()
##############################################################################

## Main method ###############################################################
if __name__ == '__main__':
  import argparse

  # Create the parser.
  aParser = argparse.ArgumentParser(description="Update DDNS entries.")

  # Add the arguments.
  aParser.add_argument("-d", "--daemon", action="store_true")
  aParser.add_argument("-v", "--verbose", action="store_true")
  aParser.add_argument("-q", "--quiet", action="store_true")

  # Parse the arguments.
  aArgs = aParser.parse_args()

  # Check for daemon.
  if aArgs.daemon:
    print("ii Daemonize it.")
  else:
    root = tk.Tk()
    root.withdraw()

    myGlobalModel = Model()

    app = MainWindow(root)

    # main loop.
    root.mainloop()
##############################################################################
