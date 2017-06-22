# WiFi_Password_Viewer
## How it works:
WiFi network information is saved onto .XML files located in: ProgramData\Microsoft\Wlansvc\Profiles\Interfaces\
The passwords found in these XML files are encrypted using Windows DPAPI. This program uses the Windows cryptography functions in order to decrypt the passwords and display them in cleartext. Alternatively, from the 'Preferences' drop down menu, you can choose to decrypt the passwords using the command prompt 'netsh wlan' command.

![](http://i.imgur.com/q5aVCwb.png)
## How to use:
Install Python 3.0 or higher.
Copy all files to your computer. (I've included PsExec.exe here, but you can download it directly from the [Microsoft website](https://technet.microsoft.com/en-us/sysinternals/bb897553.aspx) if you don't trust an .exe file from a random person on the internet.)

Start Command Prompt as administrator.

Run user_interface.py

```
python user_interface.py
```
