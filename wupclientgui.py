#!/usr/bin/python
# modified from https://github.com/CreeperMario/pytoolkit

# First let's import all the libraries that we need.

import os.path
import sys  
import os
import select as sel
import socket as sock
import sys as sys
if sys.version_info[0] < 3: # Python 2.7 and earlier
    import Tkinter as tk
    import tkFileDialog as tkfd
    from Tkinter import *
else: # Python 3 and later
    import tkinter as tk
    from tkinter import filedialog as tkfd

import wupclient

global w
w = None

global pc
pc = 0

global dir
dir = 0
global dirw
dirw = 0
global opendir
opendir = None
global count
count = None
global size
size = None
global path_src_in
path_src_in = None
global name_src_in
name_src_in = None


# This class controls the GUI and program behaviour.
class Application(tk.Frame):
    def __init__(self, master=None):
        s=None
        # Create the GUI window
        self.master = master 
        self.connected = False
        
        # create a popup menu
        self.menu = Menu(root, tearoff=0)
        self.menu.add_command(label="Open/Close Mode PC.", command=self.open_pc)
        self.menu.add_command(label="--------------WIIU--------------")
        self.menu.add_command(label="Download Folder.", command=self.dl_folder)
        self.menu.add_command(label="Create Folder.", command=self.createfolder)
        self.menu.add_command(label="---------------SD---------------")
        self.menu.add_command(label="Install Title.", command=self.dirinstall)
        self.menu.add_command(label="-------------OTHERS-------------")
        self.menu.add_command(label="Copy.", command=self.copyfile)
        self.menu.add_command(label="Paste.", command=self.pastefile)
        self.menu.add_command(label="------------Warning!------------")
        self.menu.add_command(label="Delete File.", command=self.deletefile)
        self.menu.add_command(label="Delete Folder.", command=self.deletefolder)
        self.menu.add_command(label="CHMod File 777.", command=self.chmod)
        self.menu.add_command(label="CHMod 644 Folder.", command=self.chmodR)

        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)
        
        self.l = Label(master, text="Current Directory: None (hit connect above)")
        self.l.pack()
        
        self.l2 = Label(master, text="Double click an entry above to go into the folder.\nRight click an entry above to download its contents.\n\nCredits to Smea, FIX94, CreeperMario,\nMaschell, rw-r-r_0644, and vgmoose.")
        self.l2.pack(side=tk.BOTTOM)

        
        self.update_list([])
            
        # Add the frames that hold the buttons
        self.btnframe = tk.Frame(self)
        self.btnframe.pack()
        
        self.btnframe2 = tk.Frame(self)
        self.btnframe2.pack()
        
        self.btnclear = tk.Button(self.btnframe, text="Connect", command=self.connect)
        self.btnclear.pack(side=tk.LEFT)
        
#
#        # Add the buttons
#        self.btnclear = tk.Button(self.btnframe, text="Download Directory", command=self.cd)
#        self.btnclear.pack(side=tk.LEFT)

        self.bnrefresh = tk.Button(self.btnframe, text="Refresh", command=self.refresh)
        self.bnrefresh.pack(side=tk.LEFT)
        self.bnrefresh['state'] = 'disabled'

#        self.btnclear = tk.Button(self.btnframe, text="Enter Directory", command=self.cd)
#        self.btnclear.pack(side=tk.LEFT)

        self.btnusb = tk.Button(self.btnframe2, text="Mount usb", command=self.usb)
        self.btnusb.pack(side=tk.LEFT)
        self.btnusb['state'] = 'disabled'

        self.btnmount = tk.Button(self.btnframe2, text="Mount odd_tickets", command=self.mount)
        self.btnmount.pack(side=tk.RIGHT)
        self.btnmount['state'] = 'disabled'

        self.btnumount = tk.Button(self.btnframe2, text="Unmount odd_tickets", command=self.umount)
        self.btnumount.pack(side=tk.RIGHT)
        self.btnumount['state'] = 'disabled'
        
        # create a wupclient instance, mount sd
#        self.w = wupclient.wupclient()
#        w.mount_sd()

        # Set the currently loaded program to "Unknown Program"
        self.loadedProgram = "Disconnected"
        root.title("%s - Wup Client GUI" % self.loadedProgram)
                
        
    def popup2(self, event):
        self.menu.post(event.x_root, event.y_root)

    # This function handles the loop for the socket, reading input and putting
    # the input into the text box.
    def update_list(self, files):
        global pc
        try:
            self.listbox.destroy()
        except:
            pass
        
        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        if pc == 0:
            self.listbox.bind('<Double-1>', lambda x: self.cd())
        if pc == 1:
            self.listbox.bind('<Double-1>', lambda x: self.cdpc())
        self.listbox.bind("<Button-2>", self.popup2)
        self.listbox.bind("<Button-3>", self.popup2)
        self.data = ['..']
        self.listbox.insert(END, '..')
        count = 0
        for item in files:
            if "name" not in item:
                item = {"name":item, "is_file": True}
            if not item['is_file']:
                item['name'] += '/'
 
            if pc == 0:
                self.get_size(item['name'])
                self.listbox.insert(END, item['name']+"     "+str(w.size_wiiu))
            if pc == 1:
                self.listbox.insert(END, item['name']+"     "+str(w.size_pc[count]))

            self.data.append(item['name'])
            count += 1
    class popupWindow(object):
        def __init__(self, master, title):
            top=self.top=Toplevel(master)
            self.l=Label(top,text=title)
            self.l.pack()
            self.e=Entry(top)
            self.e.pack()
            self.b=Button(top,text='Accept',command=self.cleanup)
            self.b.pack()
        def cleanup(self, ev=None):
            self.value=self.e.get()
            self.top.destroy()
            
    def connect(self):
        global w
        self.popup = self.popupWindow(self.master, "Enter the IP of your Wii U, after running the wupserver fw.img")
        self.popup.top.bind("<Return>", self.popup.cleanup)
#       self.popup.top.bind("<Enter>", self.popup.cleanup)
        self.master.wait_window(self.popup.top)
        
        self.connected = True
        root.title("%s - Wup Client GUI" % self.popup.value)
        self.l.configure(text="WIIU Connected! Current directory: /vol")
        
        # get value of pop up
        ip = self.popup.value
        # connect with wupserver, mount sd
        w = wupclient.wupclient(ip)
        self.mount_sd()
        
        # do an ls
        self.update_list(w.ls(return_data=True))
        
        self.bnrefresh['state'] = 'normal'
        self.btnusb['state'] = 'normal'
        self.btnmount['state'] = 'normal'
        self.btnumount['state'] = 'normal'   
     
    def popup_file(self):
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = w.pwd()
        if not target.endswith("/"):
            target += "/"
        
        self.popup = self.popupWindow(self.master, "Enter the name file for copie PC to WIIU")
        self.popup.top.bind("<Return>", self.popup.cleanup)
        self.master.wait_window(self.popup.top)
        file = self.popup.value
        
        w.updirfile(target+file)
        

    def copyfile(self):
        global path_src_in
        global name_src_in
        global pc
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = None
        if pc == 0:
            target = w.cwd
        if pc == 1:
            target = w.pcdir
        if not target.endswith("/"):
            target += "/"

        try:
            path_src_in = target+items[0]
            name_src_in = items[0]
        except:
            print "You must select a file from the list below" 

    def pastefile(self):

        global path_src_in
        global name_src_in
        global pc
        
        target = None
        if pc == 0:
            target = w.cwd
        if pc == 1:
            target = w.pcdir
        if not target.endswith("/"):
            target += "/"

        
        #wiiu to wiiu
        if pc == 0 and path_src_in[0] == "/":
            self.cp_pc(path_src_in, target+name_src_in)
            self.update_list(w.ls(return_data=True))
        #pc to wiiu 
        if pc == 0 and path_src_in[0] != "/": 
            self.up_pc(path_src_in, target+name_src_in)
            self.update_list(w.ls(return_data=True))
        #wiiu to pc
        if pc == 1 and path_src_in[0] == "/":
            self.dl_pc(path_src_in, target+name_src_in)
            self.update_list(self.lspc(return_data=True))
  
    def createfolder(self):
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = w.pwd()
        if not target.endswith("/"):
            target += "/"
        
        self.popup = self.popupWindow(self.master, "Enter the name folder create")
        self.popup.top.bind("<Return>", self.popup.cleanup)
        self.master.wait_window(self.popup.top)
        file = self.popup.value
        print(target+file)
        self.create(target+file) 
        self.update_list(w.ls(return_data=True))
     
    def dl_folder(self):
      
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = w.pwd()
        if not target.endswith("/"):
            target += "/"
            
        try:
            w.dldir(target+items[0])
        except:
            print "You must select a directory from the list below"

    def cdpcdir(self, path):
        if path[1] != ":" and w.pcdir[1] == ":":
            return self.cdpcdir(w.pcdir + "/" + path)
        wpath = os.path.normpath(path).replace("\\\\", "/").replace("\\", "/")
        w.pcdir = wpath or w.pcdir
        return 0
    

    def dirinstall(self):
        if not self.connected:
            return
        
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = w.pwd()
        if not target.endswith("/"):
            target += "/"
           
        name = target[20:len(target)]
        try:
            self.install_title(name, items[0])
        except:
            print "You must select a Title Folder from the list below"
            
        
    def refresh(self, path=None):
        if not self.connected:
            return
        
        # do an ls
        self.update_list(w.ls(return_data=True))
        
        if path:
            self.l.configure (text="WIIU Connected! pwd: " + w.pwd())
    
    def cd(self):
        if not self.connected:
            return
        
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        
        try:
            w.cd(items[0])
            self.refresh(items[0])
        except:
            print "You must select a directory from the list below"
#--------------WARNING FONCTION-------------------
    def deletefile(self):
        if not self.connected:
            return
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        self.popup = self.popupWindow(self.master, "Enter 'DELETE' for delete file")
        self.popup.top.bind("<Return>", self.popup.cleanup)
        self.master.wait_window(self.popup.top)
        file = self.popup.value
        global pc
        try:
            if pc == 0 and file == "DELETE":
                w.rm(items[0])
                self.refresh(w.cwd)
            if pc == 0 and file != "DELETE":
                print("rm aborted")
            else:
                print "No Mode PC"
        except:
            print "You must select a directory from the list below"

    def deletefolder(self):
        if not self.connected:
            return
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        self.popup = self.popupWindow(self.master, "Enter 'DELETE' for delete folder (if empty), or 'ALL' to delete recursively")
        self.popup.top.bind("<Return>", self.popup.cleanup)
        self.master.wait_window(self.popup.top)
        file = self.popup.value
        global pc
        try:
            if pc == 0 and file == "DELETE":
                w.rmdir(items[0])
                self.refresh(w.cwd)
            elif pc == 0 and file == "ALL":
                w.rmdir_recursive(items[0])
                self.refresh(w.cwd)
            elif pc == 0 and file != "DELETE" and file != "ALL":
                print("rmdir aborted")
            else:
                print "No Mode PC"
        except:
            print "You must select a directory from the list below"

    def chmod(self):
        if not self.connected:
            return
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        
        global pc
        try:
            if pc == 0:
                w.chmod(items[0], 0x777)
                self.refresh(w.cwd)
            else:
                print "No Mode PC"
        except:
            print "You must select a directory from the list below"

    def chmodR(self):
        if not self.connected:
            return
        items = self.listbox.curselection()
        items = [self.data[int(item)] for item in items]
        target = w.cwd
        if not target.endswith("/"):
            target += "/"
        global pc
        try:
            if pc == 0:
                w.chmodR(target+items[0], 0x644)
                self.refresh(w.cwd)
            else:
                print "No Mode PC"
        except:
            print "You must select a directory from the list below"

#-----------------------------------
    def open_pc(self):
        #pc = 0 = mode wiiu 
        global pc
        global dir
        if pc == 1:  
            pc = 0
        else:  
            pc = 1
         
        if pc == 1:
            self.cdpc()
        else:
            dir = 0
            self.refresh(w.cwd)
            
   
    def refreshpc(self, path):
        if not self.connected:
            return
        # do an ls
        self.update_list(self.lspc(return_data=True))
        
        if path:
            self.l.configure (text="PC Connected! pwd: " + w.pcdir)
    
    def cdpc(self):
        if not self.connected:
            return
        
        global dir
        if dir == 1:
            items = self.listbox.curselection()
            items = [self.data[int(item)] for item in items]
            
            if items[0].endswith("/") or items[0].endswith(".."):
                self.cdpcdir(items[0])
                self.refreshpc(items[0])
            else:
                print("cdpc error : path does not exist (%s)" % (w.pcdir+"/"+items[0]))
        if dir == 0:
            dir = 1
            self.cdpcdir(w.pcdir)
            self.refreshpc(w.pcdir)
    
    def lspc(self, path = None, return_data = False):
        s = None
        tpath = path if path != None else w.pcdir
        print "=============================================="
        print os.path.normpath(tpath)
        wpath = os.path.normpath(tpath).replace("\\\\", "/").replace("\\", "/").split("/")
        print wpath
        # os.path.getsize(path)
        data = os.listdir(tpath)
        w.size_pc[:] = []
        print "----------------------------------------------"
        
        global size
        counter = 0
        for element in os.listdir(tpath):
            if os.path.isdir(tpath+"/"+data[counter]):
                data[counter] = data[counter]+"/"
                w.size_pc.append(" ")
                print data[counter]+"     "+str(w.size_pc[counter])
            else:
                
                size = os.path.getsize(tpath+"/"+data[counter])
                size = size/1024
                w.size_pc.append("("+str(size)+" Ko"+")")
                print data[counter]+"     "+str(w.size_pc[counter])
            counter += 1
        entries = data
        return entries if return_data else None
   
    def up_pc(self, source_in, source_out):

        fsa_handle = w.get_fsa_handle()
        
        f = open(source_in, "rb")
        ret, file_handle = w.FSA_OpenFile(fsa_handle, source_out, "w")
        if ret != 0x0:
            print("up error : could not open " + source_out)
            return
        progress = 0
        block_size = 0x400
        while True:
            data = f.read(block_size)
            ret = w.FSA_WriteFile(fsa_handle, file_handle, data)
            progress += len(data)
            sys.stdout.write(hex(progress) + "\r"); sys.stdout.flush();
            if len(data) < block_size:
                break
        ret = w.FSA_CloseFile(fsa_handle, file_handle)
   
    def dl_pc(self, source_in, source_out):
        fsa_handle = w.get_fsa_handle()

        ret, file_handle = w.FSA_OpenFile(fsa_handle, source_in, "r")

        if ret != 0x0:
            print("dl error : could not open " + source_in)
            return
        buffer = bytearray()
        block_size = 0x400

        while True:
            ret, data = w.FSA_ReadFile(fsa_handle, file_handle, 0x1, block_size)
            # print(hex(ret), data)
            buffer += data[:ret]
            sys.stdout.write(hex(len(buffer)) + "\r"); sys.stdout.flush();
            if ret < block_size:
                break
        ret = w.FSA_CloseFile(fsa_handle, file_handle)
        
        #Needs to be tested
        open(source_out, "wb").write(buffer) 
        print("download finish : " +  source_in)
   
    def cp_pc(self, filename_in, filename_out):

        fsa_handle = w.get_fsa_handle()
        ret, in_file_handle = w.FSA_OpenFile(fsa_handle, filename_in, "r")
        if ret != 0x0:
            print("cp error : could not open in " + filename_in)
            return
        ret, out_file_handle = w.FSA_OpenFile(fsa_handle, filename_out, "w")
        if ret != 0x0:
            print("cp error : could not open out" + filename_out)
            return
        block_size = 0x10000
        buffer = w.alloc(block_size, 0x40)
        k = 0
        while True:
            ret, _ = w.FSA_ReadFilePtr(fsa_handle, in_file_handle, 0x1, block_size, buffer)
            k += ret
            ret = w.FSA_WriteFilePtr(fsa_handle, out_file_handle, 0x1, ret, buffer)
            sys.stdout.write(hex(k) + "\r"); sys.stdout.flush();
            if ret < block_size:
                break
        w.free(buffer)
        ret = w.FSA_CloseFile(fsa_handle, out_file_handle)
        ret = w.FSA_CloseFile(fsa_handle, in_file_handle)

    def get_size(self, filename):
        
        global size
        fsa_handle = w.get_fsa_handle()
        error = 0
        
        ret, file_handle = w.FSA_OpenFile(fsa_handle, w.cwd+"/"+filename, "r")
        if ret != 0x0:
            error = 1  
        if error == 0:
            (ret, stats) = w.FSA_GetStatFile(fsa_handle, file_handle)
            if ret != 0x0:
                print("stat error : " + hex(ret))
            

        if error == 1:
            w.size_wiiu = " "
            print filename+"     "+w.size_wiiu
        else:
            size = stats[5]
            if size < 1024:
                w.size_wiiu = "("+str(size)+"Bytes"+")"
                print filename+"     "+str(w.size_wiiu)
            else:
                size = size/1024
                w.size_wiiu = "("+str(size)+"Kb"+")"
                print filename+"     "+str(w.size_wiiu)
               

        ret = w.FSA_CloseFile(fsa_handle, file_handle)
  
    def create(self, path):
        w.mkdir(path, 777)


    def usb(self):
        if not self.connected:
            return
        
        self.mount_usb()
    
    def mount(self):
        if not self.connected:
            return
        
        self.mount_odd_tickets()
    
    def umount(self):
        if not self.connected:
            return
        self.unmount_odd_tickets()
        
    def mount_usb(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Mount(handle, "/dev/usb01", "/vol/storage_usb", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    # This function handles the "Clear Backlog" button, simply clearing the box.
    def callclear(self):
        self.backlog.configure(state="normal")
        self.backlog.delete("0.0", tk.END)
        self.backlog.configure(state="disabled")

    # This function handles the "Dunp Backlog to File" button. It opens a dialog
    # and asks the user to select a file to save the contents to.
    def calldump(self):
        content = self.backlog.get("0.0", tk.END)
        f = tkfd.asksaveasfile(mode="w", defaultextension=".log",
            filetypes=[("Log Files", ".log"), ("Text Files", ".txt"), ("All Files", ".*")], initialfile="wiiu.log",
            parent=root, title="Save logs")
        if f is None: # If the user pressed the "Cancel" button in the dialog
            return
        f.write(content)
        f.close()
    
    def install_title(self, path, name):
        mcp_handle = w.open("/dev/mcp", 0)
        print(hex(mcp_handle))
         
        
        ret, data = w.MCP_InstallGetInfo(mcp_handle, "/vol/storage_sdcard/"+path +name)
        if ret != 0:
            print("error open folder")
            ret = w.close(mcp_handle)
            return
        else:
            print("install info : " + hex(ret), [hex(v) for v in data])
            ret = w.MCP_Install(mcp_handle, "/vol/storage_sdcard/"+path +name)
            if ret == 0:
                print("install finish") 
                ret = w.close(mcp_handle)
                return
            else:
                print("error install !")
                ret = w.close(mcp_handle)
                return

        return
    
    def mount_sd(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Mount(handle, "/dev/sdcard01", "/vol/storage_sdcard", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def unmount_sd(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Unmount(handle, "/vol/storage_sdcard", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def mount_odd_content(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Mount(handle, "/dev/odd03", "/vol/storage_odd_content", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def unmount_odd_content(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Unmount(handle, "/vol/storage_odd_content", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def mount_odd_update(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Mount(handle, "/dev/odd02", "/vol/storage_odd_update", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def unmount_odd_update(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Unmount(handle, "/vol/storage_odd_update", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def mount_odd_tickets(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Mount(handle, "/dev/odd01", "/vol/storage_odd_tickets", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def unmount_odd_tickets(self):
        handle = w.open("/dev/fsa", 0)
        print(hex(handle))

        ret = w.FSA_Unmount(handle, "/vol/storage_odd_tickets", 2)
        print(hex(ret))

        ret = w.close(handle)
        print(hex(ret))

    def get_nim_status(self):
        nim_handle = w.open("/dev/nim", 0)
        print(hex(nim_handle))

        inbuffer = buffer(0x80)
        (ret, data) = w.ioctlv(nim_handle, 0x00, [inbuffer], [0x80])

        print(hex(ret), "".join("%02X" % v for v in data[0]))

        ret = w.close(nim_handle)
        print(hex(ret))

    def read_and_print(self, adr, size):
        data = w.read(adr, size)
        data = struct.unpack(">%dI" % (len(data) // 4), data)
        for i in range(0, len(data), 4):
            print(" ".join("%08X"%v for v in data[i:i+4]))

# The class above's code is finished now. Let's actually run it!
root = tk.Tk()
root.title("Starting...")
root.minsize(269, 66) # For macOS GUI style. May be different depending on your Desktop environment.
app = Application(master=root)
app.mainloop()

# We only reach this point once the user has explicitly closed the window by pressing the "X" button.
# Let's close the sockets and finish the program.
app.wiiu.close()
