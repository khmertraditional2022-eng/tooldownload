import urllib.request
import json
import os
import sys
import subprocess
from PyQt5.QtWidgets import QMessageBox, QProgressDialog, QApplication
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices

APP_VERSION = "1.0.4"
UPDATE_URL = "https://raw.githubusercontent.com/khmertraditional2022-eng/tooldownload/main/version.json"

def check_for_updates(parent_window):
    """
    Checks if a newer version is available.
    If so, prompts the user to download it automatically.
    """
    try:
        req = urllib.request.Request(UPDATE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        latest_version = data.get("version", APP_VERSION)
        download_url = data.get("download_url", "")
        release_notes = data.get("release_notes", "កំណែថ្មីមានការកែប្រែចំណុចមួយចំនួន។")
        
        if latest_version > APP_VERSION:
            msg = QMessageBox(parent_window)
            msg.setWindowTitle("Update Available (កំណែថ្មី)")
            msg.setText(f"កម្មវិធីកំណែថ្មី {latest_version} ត្រូវបានបញ្ចេញហើយ!\n(Version បច្ចុប្បន្ន: {APP_VERSION})\n\nព័ត៌មានបន្ថែម៖\n{release_notes}\n\nតើអ្នកចង់អាប់ដេតដោយស្វ័យប្រវត្តិឥឡូវនេះទេ?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            
            msg.button(QMessageBox.Yes).setText("អាប់ដេត (Update)")
            msg.button(QMessageBox.No).setText("ពេលក្រោយ (Later)")
            
            retval = msg.exec_()
            if retval == QMessageBox.Yes and download_url:
                is_frozen = getattr(sys, 'frozen', False)
                if not is_frozen:
                    # If running from source code, just open browser
                    QDesktopServices.openUrl(QUrl(download_url))
                    return True
                
                # Auto download and replace logic for .exe
                exe_path = sys.executable
                exe_dir = os.path.dirname(exe_path)
                exe_name = os.path.basename(exe_path)
                new_exe_path = os.path.join(exe_dir, f"new_{exe_name}")
                
                # Create Progress Dialog
                progress = QProgressDialog("កំពុងទាញយកកំណែថ្មី... សូមរង់ចាំ!", "បោះបង់", 0, 100, parent_window)
                progress.setWindowTitle("Downloading Update")
                progress.setWindowModality(Qt.WindowModal)
                progress.setAutoClose(True)
                
                def report_hook(count, block_size, total_size):
                    if total_size > 0:
                        percent = int(count * block_size * 100 / total_size)
                        progress.setValue(percent)
                        QApplication.processEvents()
                        if progress.wasCanceled():
                            raise Exception("Cancelled")
                
                try:
                    urllib.request.urlretrieve(download_url, new_exe_path, reporthook=report_hook)
                except Exception as e:
                    if str(e) == "Cancelled":
                        return False
                    QMessageBox.critical(parent_window, "បរាជ័យ", f"មិនអាចទាញយកកំណែថ្មីបានទេ: {e}")
                    return False
                    
                # Create bat script to replace file
                bat_path = os.path.join(exe_dir, "update.bat")
                with open(bat_path, "w") as f:
                    f.write("@echo off\n")
                    f.write("timeout /t 2 /nobreak > NUL\n")  # Wait for app to close
                    f.write(f'move /y "{new_exe_path}" "{exe_path}"\n')
                    f.write(f'start "" "{exe_path}"\n')
                    f.write('del "%~f0"\n') # Delete this bat file
                
                # Run the bat script detached
                subprocess.Popen(bat_path, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)
                
                # Close the application
                QApplication.quit()
                sys.exit(0)
                
    except Exception as e:
        # Fail silently if offline or URL doesn't exist yet
        pass
        
    return False
