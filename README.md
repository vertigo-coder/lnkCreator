
# LNK Creator
Creates Windows LNK shortcuts that run hidden PowerShell commands.
## Features
*   Silent execution with a decoy file.
*   Uses common system icons (MP3, DOCX, XLS, TXT, Folder).
*   Payload is Base64 encoded.
## Install
```bash
pip install pywin32
```
## Usage
**Hidden Payload:**
```bash
python -m lnkCreator -o secret.lnk -i txt
```
**With Decoy:**
```bash
python -m lnkCreator -o Report.lnk -i docx -d decoy.docx
```
**Debug:**
```bash
python -m lnkCreator -o secret.lnk -i txt --debug
```
## Change Payload
Encode your command in PowerShell and replace the `encoded_command` variable in the script.
```powershell
$command = 'your-command-here'
$bytes = [System.Text.Encoding]::UTF16.GetBytes($command)
[Convert]::ToBase64String($bytes)
```
**Disclaimer:** For authorized security testing only.
