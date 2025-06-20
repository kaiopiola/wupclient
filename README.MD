# WupClient GUI Mod

## What's New / Improvements

- **Recursive Delete**: Now it's possible to delete folders and all their contents (including subfolders and files) recursively directly through the interface. Simply select the folder and, when confirming deletion, type `ALL` for complete removal, even for non-empty folders.
- Other usability and compatibility improvements.

## About

This project is a Python graphical interface (GUI) for `wupclient`, allowing you to explore, transfer, install and manage Wii U files remotely over the network. Based on classic homebrew community scripts, with improvements for modern use.

## Requirements

- **Wii U** with wupserver (fw.img) running
- **Python 2.7** (doesn't work with Python 3)
  - Download at: https://www.python.org/downloads/release/python-2718/
- Windows (recommended)

## Python 2.7 Installation

1. Download the Python 2.7 installer: [Python 2.7.18 Windows x86-64 MSI installer](https://www.python.org/ftp/python/2.7.18/python-2.7.18.amd64.msi)
2. Install normally, making sure to check the option to install Tcl/Tk (Tkinter).
3. (Optional) Add `C:\Python27` to Windows PATH.

## How to Run WupClient GUI

1. **Open Command Prompt or PowerShell in the project folder.**
2. Run:
   ```
   C:\Python27\python.exe wupclientgui.py
   ```
   or, if Python 2.7 is in your PATH:
   ```
   python wupclientgui.py
   ```
3. In the interface, click "Connect" and enter your Wii U's IP address (with wupserver running).

## Interface Functions

- **Connect**: connects to the Wii U using the provided IP address.
- **Refresh**: updates the current directory listing.
- **Mount usb / Mount odd_tickets / Unmount odd_tickets**: mounts/unmounts Wii U volumes.
- **Download Folder**: downloads a folder from the Wii U to your PC.
- **Create Folder**: creates a new folder on the Wii U.
- **Install Title**: installs a title from a selected folder.
- **Copy / Paste**: copies and pastes files between the Wii U and PC.
- **Delete File**: deletes a selected file.
- **Delete Folder**: deletes a selected folder. If you type `ALL` when confirming, it deletes recursively (including non-empty folders).
  - **Recursive Delete**: By typing `ALL` during confirmation, the deletion will be performed recursively, removing all files and subfolders.

## Notes

- The app only works with Python 2.7 due to dependencies on the older Tkinter and syntax.
- To delete non-empty folders, type `ALL` when confirming.
  - With the recursive delete option, all folder contents will be permanently removed.
- The Wii U and PC must be on the same network.
- The script was NOT originally written by me, I am just including necessary improvements in this repo!

## Credits
- Smea, FIX94, CreeperMario, Maschell, rw-r-r_0644, vgmoose, KaioPiola and the Wii U homebrew community.

---

If you find bugs or want to contribute, please open an issue or send a pull request!
