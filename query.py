import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

import pymysql.cursors

connection = pymysql.connect(
    host='milogert.com',
    user='milo',
    passwd='locatetimefarduck',
    db='personal',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def calculate(*args):
  try:
    value = float(feet.get())
    meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
  except ValueError:
    pass

def setupTable(*args):
  try:
    with connection.cursor() as cursor:
      # Read a single record
      sql = "SELECT * FROM `ddns__credentials`"
      cursor.execute(sql)
      result = cursor.fetchall()
      return result
  except ValueError:
    # TODO
    pass

# def select_cmd(selected):
#   print('Selected items:', selected)


## Display the ui. ###########################################################
# root = Tk()
# root.title("Feet to Meters")

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# mainframe.columnconfigure(0, weight=1)
# mainframe.rowconfigure(0, weight=1)

# feet = StringVar()
# meters = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))

# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
# root.bind('<Return>', calculate)

headers = ('subdomain', 'ip', 'provider', 'response')

entries = setupTable()

class MultiColumnListbox(object):
  """use a ttk.TreeView as a multicolumn ListBox"""

  def __init__(self):
    self.tree = None
    self._setup_widgets()
    self._build_tree()

  def _setup_widgets(self):
    # Set up the container.
    self.container = ttk.Frame()
    self.container.pack(fill='both', expand=True)

    # create a treeview with dual scrollbars
    self.tree = ttk.Treeview(columns=headers, show="headings")
    vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
    hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
    self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    self.tree.bind('<1>', self.select_cmd)
    self.tree.grid(column=0, row=0, rowspan=9, sticky='nsew', in_=self.container)
    vsb.grid(column=1, row=0, rowspan=9, sticky='ns', in_=self.container)
    hsb.grid(column=0, row=10, sticky='ew', in_=self.container)

    self.aBtnAdd = ttk.Button()
    self.aBtnAdd.configure(text="Add", command=self.addDialog)
    self.aBtnAdd.grid(column=2, row=0, padx=10, pady=10, in_=self.container)

    self.aBtnEdit = ttk.Button()
    self.aBtnEdit.configure(text="Edit")
    self.aBtnEdit.grid(column=2, row=1, padx=10, pady=10, in_=self.container)

    self.aBtnDelete = ttk.Button()
    self.aBtnDelete.configure(text="Delete")
    self.aBtnDelete.grid(column=2, row=2, padx=10, pady=10, in_=self.container)

    self.aBtnUpdate = ttk.Button()
    self.aBtnUpdate.configure(text="Update")
    self.aBtnUpdate.grid(column=2, row=11, padx=10, pady=10, in_=self.container)

    self.container.grid_columnconfigure(0, weight=1)
    self.container.grid_rowconfigure(0, weight=1)

  def _build_tree(self):
    for col in headers:
      self.tree.heading(
          col,
          text=col.title(),
          command=lambda c=col: sortby(self.tree, c, 0)
      )
      # adjust the column's width to the header string
      self.tree.column(col, width=tkFont.Font().measure(col.title()))

    for item in entries:
      ins = normalizeData(item)
      self.tree.insert('', 'end', values=ins)
      # adjust column's width if necessary to fit each value
      for ix, val in enumerate(ins):
        col_w = tkFont.Font().measure(val)
        if self.tree.column(headers[ix], width=None) < col_w:
          self.tree.column(headers[ix], width=col_w)

  def select_cmd(self, event):
    print(self.tree.focus())
    print(self.tree.selection())


def sortby(tree, col, descending):
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
  tree.heading(col, command=lambda col=col: sortby(tree, col, \
      int(not descending)))


def normalizeData(data):
  ret = []
  for item in headers:
    ret.append(data[item])
  return ret




if __name__ == '__main__':
  root = tk.Tk()
  root.title("Multicolumn Treeview/Listbox")
  listbox = MultiColumnListbox()
  root.mainloop()

  # Close the database connection once the program is done running.
  connection.close()
