import os
import math
import pyperclip
import windnd
import ctypes
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from torrent import parserInfoPrint, parserFilePrint

filePath = ''
recentFile = []
lang = 'Eng'
encode = 'utf-8'


class newEntry(Entry):
    def __init__(self, master, textvariable, placeholder="PLACEHOLDER", color="grey", *args, **kwargs):
        super().__init__(master, textvariable=textvariable, *args, **kwargs)
        self.textvariable = textvariable
        self.placeholder = StringVar()
        self.placeholdertext = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]
        self.texttempvar = StringVar()
        self.texttempvar = self.textvariable
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind('<<Focus In>>', self.foc_in)

        self.put_placeholder()

    def put_placeholder(self):
        self['textvariable'] = self.placeholder
        self.placeholder.set(self.placeholdertext)
        self["fg"] = self.placeholder_color

    def foc_in(self, *args):
        self['textvariable'] = self.texttempvar
        if self["fg"] == self.placeholder_color:
            self["fg"] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self['textvariable'] = self.placeholder
            self["fg"] = self.placeholder_color

    def get(self):
        return self.texttempvar.get()


class Gui:
    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.root()
        self.mainframe()
        self.menu_1()
        self.entry()
        self.entry_0()
        self.entry_1()
        self.button()
        # self.button_0()
        # self.button_1()
        self.entry_2()
        self.entry_3Temp()
        self.entry_3()
        self.entry_4()
        self.Grid()
        self.dragFiles()
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=0, pady=0)
        # self.root.resizable(False, False)
        self.mainframe.mainloop()

    def root(self):
        self.root = Tk()
        self.root.title('BitInfo')
        self.root.geometry("1600x1080")
        self.root.configure(bg="#e1e1e1")
        self.root.wm_iconbitmap("assets\search.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # self.root.tk.call('tk', 'scaling', self.ScaleFactor / 75)

    def mainframe(self):
        self.mainframe = Frame(self.root, background='#f0f0f0', pady=1, padx=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=0)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.columnconfigure(3, weight=0)
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=0)
        self.mainframe.rowconfigure(2, weight=1)
        self.mainframe.rowconfigure(3, weight=0)

    def menu_1(self):
        self.root.option_add('*tearOff', FALSE)
        menubar = Menu(self.root)
        self.root['menu'] = menubar
        menu_file = Menu(menubar)
        menu_option = Menu(menubar)
        # menu_file.add_separator()
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_option, label='Option')
        self.openimage = PhotoImage(file='assets\open.png')
        menu_file.add_command(label='Open...', command=self.open, image=self.openimage, compound='left')
        self.menu_recent = Menu(menu_file)
        self.recentimage = PhotoImage(file=r'assets\recent.png')
        menu_file.add_cascade(menu=self.menu_recent, label='Open Recent', image=self.recentimage, compound='left')
        menu_language = Menu(menu_option)
        self.languageimage = PhotoImage(file='assets\language.png')
        menu_option.add_cascade(menu=menu_language, label='Language', image=self.languageimage, compound='left')
        menu_language.add_command(label='Eng', command=lambda: self.LangSet(lan='Eng'))
        menu_language.add_command(label='Chi', command=lambda: self.LangSet(lan='Chi'))
        menu_Encoding = Menu(menu_option)
        self.encodeimage = PhotoImage(file='assets\encode.png')
        menu_option.add_cascade(menu=menu_Encoding, label='Encoding', image=self.encodeimage, compound='left')
        menu_Encoding.add_command(label='UTF-8', command=lambda: self.LangSet(enc='utf-8'))
        menu_Encoding.add_command(label='GB18030', command=lambda: self.LangSet(enc='GB18030'))
        self.popup_1 = Menu(self.root, tearoff=0)

    def entry(self):
        self.entryVar = StringVar()
        self.entry = newEntry(self.mainframe, textvariable=self.entryVar, placeholder='Enter path')
        self.entry.bind("<Return>", self.Browse)
        self.entry.focus()

    def entry_0(self):
        self.entry0Var = StringVar()
        self.entry_0 = newEntry(self.mainframe, textvariable=self.entry0Var, placeholder='Search files', bd=1,
                                bg="#FFFFFF", highlightthickness=0)
        self.entry_0.bind("<Return>", self.SearchFile)
        self.entry0Var.trace('w', self.SearchFile)

    def entry_1(self):
        self.entry1Var = StringVar()
        self.entry_1 = newEntry(self.mainframe, textvariable=self.entry1Var, placeholder='Search files in .torrent',
                                bd=1, bg="#FFFFFF", highlightthickness=0)
        self.entry_1.bind("<Return>", self.SearchName)
        self.entry1Var.trace('w', self.SearchName)

    def button(self):
        self.button = Button(self.mainframe, text='Browse', bg="#FFFFFF", width=8, height=1, activebackground="#FFFFFF",
                             borderwidth=1,
                             highlightthickness=0,
                             command=self.Browse)

    def button_0(self):
        pass
        # self.button_0 = Button(self.mainframe, text='Search', bg="#FFFFFF", width=8, height=1,
        #                        activebackground="#FFFFFF",
        #                        borderwidth=1,
        #                        highlightthickness=0,
        #                        command=self.SearchFile)

    def button_1(self):
        pass
        # self.button_1 = Button(self.mainframe, text='Search', bg="#FFFFFF", width=8, height=1,
        #                        activebackground="#FFFFFF",
        #                        borderwidth=1,
        #                        highlightthickness=0,
        #                        command=self.SearchName)

    def entry_2(self):
        self.fileList = []
        self.fileListVar = StringVar()
        self.entry_2 = Listbox(self.mainframe, listvariable=self.fileListVar, bd=1, bg="#FFFFFF", highlightthickness=0)
        self.scroll_2 = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.entry_2.yview)
        self.entry_2.configure(yscrollcommand=self.scroll_2.set)
        self.entry_2.bind('<Enter>', lambda e: self.entry_2.bind('<<ListboxSelect>>', self.info))
        self.entry_2.bind('<Leave>', lambda e: self.entry_2.unbind('<<ListboxSelect>>'))
        self.entry_2.bind('<Button-3>', self.popupMenu)

    def entry_3(self):
        self.entry_3 = ttk.Treeview(self.mainframe, show='tree', columns=('Size'),padding=(0,0,30,0))
        self.scroll_3 = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.entry_3.yview)
        self.entry_3.configure(yscrollcommand=self.scroll_3.set)
        self.entry_3.column('#0', width=1)
        self.entry_3.column('#1', anchor='e', width=120, stretch=0)
        style = ttk.Style(self.entry_3)
        # style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", foreground="black",
                        lightcolor="#FFFFFF", darkcolor="#FFFFFF", rowheight=32
                        # bordercolor="#FFFFFF",
                        )
        self.entry_3.bind('<Button-3>', self.popupMenu)

    def entry_3Temp(self):
        # self.fileListTemp = []
        # self.fileListTempVar = StringVar()
        # self.entry_3Temp = Listbox(self.mainframe, listvariable=self.fileListTempVar, bd=1, bg="#FFFFFF",
        #                            highlightthickness=0)
        self.entry_3Temp = ttk.Treeview(self.mainframe, show='tree', columns=('Size'),padding=(0,0,30,0))
        self.scroll_3Temp = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.entry_3Temp.yview)
        self.entry_3Temp.configure(yscrollcommand=self.scroll_3Temp.set)
        self.entry_3Temp.column('#0', width=1)
        self.entry_3Temp.column('#1', anchor='e', width=120, stretch=0)
        self.entry_3Temp.bind('<Button-3>', self.popupMenu)
        # style = ttk.Style(self.entry_3)

    def entry_4(self):
        self.notebook_4 = ttk.Notebook(self.mainframe)
        self.infoVar = StringVar()
        self.entry_4 = Listbox(self.notebook_4, bd=1, height=8, bg="#FFFFFF", listvariable=self.infoVar,
                               highlightthickness=0)
        self.notebook_4.add(self.entry_4, text='Info')
        self.entry_4.bind('<Button-3>', self.popupMenu)
        self.commentVar = StringVar()
        self.entry_5 = Listbox(self.notebook_4, bd=1, height=7, bg="#FFFFFF", listvariable=self.commentVar,
                               highlightthickness=0)
        self.notebook_4.add(self.entry_5, text='Comment')
        self.entry_5.bind('<Button-3>', self.popupMenu)

    def Grid(self):
        self.mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
        self.entry.grid(column=0, row=0, columnspan=3, sticky=(E, W))
        self.entry_0.grid(column=0, row=1, columnspan=2, sticky=(E, W))
        self.entry_1.grid(column=2, row=1, columnspan=2, sticky=(E, W))
        self.button.grid(column=3, row=0)
        # self.button_0.grid(column=1, row=1)
        # self.button_1.grid(column=3, row=1)
        self.entry_2.grid(column=0, row=2, columnspan=2, rowspan=2, sticky=(N, S, E, W))
        self.scroll_2.grid(column=0,row=2,rowspan=2,sticky=(N,E,S))
        self.entry_3Temp.grid(column=2, row=2, columnspan=2, sticky=(N, S, W, E))
        self.scroll_3Temp.grid(column=3, row=2, sticky=(N, E, S))
        self.entry_3.grid(column=2, row=2, columnspan=2, sticky=(N, S, W, E))
        self.scroll_3.grid(column=3, row=2, sticky=(N, E, S))
        self.notebook_4.grid(column=2, row=3, columnspan=2, sticky=(N, S, E, W))

    def LangSet(self, *, lan=None, enc=None):
        global lang, encode
        if lan == 'Eng':
            lang = lan
            encode = 'utf-8'
        elif lan == 'Chi':
            lang = lan
            encode = 'GB18030'
        else:
            encode = enc

    def SearchFile(self, *event):
        fileTemp = []
        self.entry_2.select_clear(0, END)
        keyword = self.entry_0.get()
        for item in self.fileList:
            if keyword.lower() in item.lower():
                fileTemp.append(item)
        self.fileListVar.set(fileTemp)

    def SearchName(self, *event):
        for item in self.fileListTemp:
            self.entry_3Temp.reattach(item, '', 0)
        keyword = self.entry_1.get()
        if keyword == '':
            self.entry_3.tkraise()
            self.scroll_3.tkraise()
        else:
            self.entry_3Temp.tkraise()
            self.scroll_3Temp.tkraise()
        for item in self.fileListTemp:
            if keyword.lower() not in item.lower():
                self.entry_3Temp.detach(item)
        # self.fileListTempVar.set(fileListTempforTemp)

    def Browse(self, *event):
        global filePath
        self.fileList = []
        filePath = self.entry.get()
        try:
            f = os.listdir(filePath)
        except FileNotFoundError as fe:
            print('未找到指定路径')
        else:
            for item in f:
                if item[-8:] == '.torrent':
                    self.fileList.append(item[0:-8])
            self.fileListVar.set(self.fileList)

    def convertSize(self, sizeBytes):
        if sizeBytes == '':
            return ""
        elif sizeBytes == 0:
            return "0B"
        sizeName = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(sizeBytes, 1024)))
        p = math.pow(1024, i)
        s = round(sizeBytes / p, 1)
        return "%s %s" % (s, sizeName[i])

    def info(self, *event):
        global filePath
        self.fileListTemp = []
        self.entry_3.delete(*self.entry_3.get_children())
        self.entry_3Temp.delete(*self.entry_3Temp.get_children())
        self.entry_4.delete(0, END)
        self.entry_5.delete(0, END)
        info = parserInfoPrint(filePath + '\\' + self.entry_2.get(self.entry_2.curselection()[0]) + '.torrent', lang)
        file = parserFilePrint(filePath + '\\' + self.entry_2.get(self.entry_2.curselection()[0]) + '.torrent')
        # Files
        length = 0
        for item in file:
            length += item['length']
            n = 1
            if item['path'][0] not in self.entry_3.get_children(''):
                oid = self.entry_3.insert('', 0, item['path'][0], text=item['path'][0], open=False)
                if len(item['path']) == 1:
                    self.entry_3.set(oid, 'Size', self.convertSize(item['length']))
                    self.entry_3Temp.insert('', 0, item['path'][0], text=item['path'][0])
                    self.entry_3Temp.set(oid, 'Size', self.convertSize(item['length']))
            elif item['path'][0] in self.entry_3.get_children(''):
                oid = item['path'][0]
            for itemPath in item['path'][1:]:
                n += 1
                if oid + '/' + itemPath not in self.entry_3.get_children(oid):
                    oid = self.entry_3.insert(oid, 0, oid + '/' + itemPath, text=itemPath, open=False)
                    if n == len(item['path']):
                        self.entry_3.set(oid, 'Size', self.convertSize(item['length']))
                        self.entry_3Temp.insert('', 0, oid, text=itemPath, open=True)
                        self.entry_3Temp.set(oid, 'Size', self.convertSize(item['length']))
                if oid + '/' + itemPath in self.entry_3.get_children(oid):
                    oid = oid + '/' + itemPath
        # Info
        Temp = info[int(len(info) / 2 + 1):-1]
        if info[0] != '':
            if lang=='Chi':
                Temp.insert(0, '大小:' + self.convertSize(int(info[0])))
            else:
                Temp.insert(0, 'Size:' + self.convertSize(int(info[0])))
        else:
            Temp.insert(0, info[int(len(info) / 2)] + self.convertSize(length))
        self.infoVar.set(Temp)
        # Comment
        self.commentVar.set(info[8])
        # self.fileListTempVar.set(self.fileListTemp)
        self.fileListTemp = self.entry_3Temp.get_children()
        self.SearchName()

    def open(self, dirname=''):
        if dirname == '':
            dirname = filedialog.askdirectory()
        self.entry.event_generate('<<Focus In>>')
        self.entryVar.set(dirname)
        self.Browse()
        if dirname not in recentFile:
            self.menu_recent.add_command(label=dirname, command=lambda: self.open(dirname=dirname))
            recentFile.append(dirname)

    def popupMenu(self, event):
        self.popup_1.delete(0, 'end')
        if '.!listbox' in str(event.widget):
            event.widget.selection_clear(0, END)
            event.widget.selection_set(self.entry_2.nearest(event.y))
            event.widget.activate(self.entry_2.nearest(event.y))
            self.popup_1.add_command(label="Copy", command=lambda: pyperclip.copy(event.widget.selection_get()))
        elif '.!treeview' in str(event.widget):
            event.widget.selection_set(self.entry_3.identify_row(event.y))
            item = event.widget.selection()[0]
            self.popup_1.add_command(label="Copy",
                                     command=lambda: pyperclip.copy(event.widget.item(item, option='text')))
        self.popup_1.post(event.x_root, event.y_root)

    def dragFiles(self):
        windnd.hook_dropfiles(self.root, func=lambda files: self.open(os.path.dirname(files[0]).decode(encode)))


if __name__ == '__main__':
    Gui()
