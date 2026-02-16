# Fuction for popups
def popup_fuc(tittle, msg_text, parent=None):
    import tkinter as tk
    if parent is None:
        msg = tk.Tk()
        msg.withdraw()
    else:
        msg = parent
    
    #   Top level window
    top = tk.Toplevel(msg)
    top.title(tittle)
    top.geometry('400x250')
    top.resizable(False, False)
    top.configure(bg='#2b2b2b')
    top.attributes('-topmost', True)
    #   Create window
    top.update_idletasks()
    x = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
    y = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
    top.geometry(f'+{x}+{y}')
    #   Label
    label = tk.Label(top, text=msg_text, bg='#2b2b2b', fg='white', wraplength=380, font=('Arial', 11))
    label.pack(expand=True, pady=(20, 10))
    #   Button
    if parent is None:
        def close_first_popup():
            msg.destroy()
        btn_command = close_first_popup
        top.protocol("WM_DELETE_WINDOW", close_first_popup)
    else:
        btn_command = top.destroy
    button = tk.Button(top, text='OK', command=btn_command, bg='#555555', fg='white', width=10)
    button.pack(pady=(0, 20))
    
    if parent is None:
        msg.after(100, lambda: None)
        top.protocol("WM_DELETE_WINDOW", msg.destroy)
        msg.mainloop()

list = ['customtkinter'] # List of libraries to import and install if not found
import subprocess, time, socket, threading
#   Try to import libraries, if not found, install them and try again
try:
    import customtkinter as ctk
    
    #   Popup message
    popup_fuc('Import OK', 'All libraries imported successfully!')
except Exception as e:
    popup_fuc(f'Error importing the libraries', f'error: {e}')
    time.sleep(1)
    for l in list:
        try:
            subprocess.run(['python', '-m', 'pip', 'install', l])
        except Exception as e:
            popup_fuc(f'Error installing {l}', f'error: {e}')

#   Defs => APP
def get_data(data_title, data_text):
    dialog = ctk.CTkInputDialog(text=data_text, title=data_title)
    data = dialog.get_input()
    if data:
        popup_fuc('Data Received', f'You entered: {data}', parent=app)
    else:
        popup_fuc('No Data', 'No data was entered.', parent=app)
    return data

def check_wifi_nets():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)
        output = result.stdout
        popup_fuc('Available Wi-Fi Networks', output, parent=app)
    except Exception as e:
        popup_fuc('Error Checking Wi-Fi Networks', f'error: {e}', parent=app)

def set_server_python():
    try:
        ip = get_data('Server IP', 'Enter the IP address to bind the server to (e.g., 127.0.0.1): ')
        if not ip:
            popup_fuc('No IP Address', 'No IP address was entered. Server setup cancelled.', parent=app)
            return
        rute = get_data('Server Route', 'Enter the directory path to serve (e.g., C:\\Users\\YourName\\Documents): ')
        if not rute:
            popup_fuc('No Directory Path', 'No directory path was entered. Server setup cancelled.', parent=app)
            return
        def start_server():
            subprocess.run(['python', '-m', 'http.server', '8000', '--bind', ip, '-d', rute])
            popup_fuc('Server Started', f'Python server is running on {ip}:8000', parent=app)
            popup_fuc('Server Path', f'Python server is running on {rute}', parent=app)
        threading.Thread(target=start_server).start()
    except Exception as e:
        popup_fuc('Error Starting Server', f'error: {e}', parent=app)

#   Main window
app = ctk.CTk()
app.title('Nettools - v1.0')
app.geometry('800x600')
app.resizable(False, False)
app.configure(bg='#2b2b2b')

wifi_btn = ctk.CTkButton(app, text='Check Wi-Fi Networks',
                         command=check_wifi_nets,
                         fg_color='#555555',
                         text_color='white',
                         width=200)
wifi_btn.pack(pady=20)

set_server = ctk.CTkButton(app, text='Set up a server',
                         command=set_server_python,
                         fg_color='#555555',
                         text_color='white',
                         width=200)
set_server.pack(pady=20)

ctk.CTkLabel(app, text='Developed by Kurkodevs', text_color='white', font=('Arial', 16)).pack(pady=10, side='bottom')    
app.protocol("WM_DELETE_WINDOW", app.destroy) # Handle window close event
app.mainloop() # Start the main loop