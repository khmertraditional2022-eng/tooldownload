import urllib.request
import json
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

APP_VERSION = "1.0.2"
# Replace this URL with the raw URL to your version.json file on GitHub or Gist.
# Example: "https://raw.githubusercontent.com/YourName/YourRepo/main/version.json"
UPDATE_URL = "https://raw.githubusercontent.com/khmertraditional2022-eng/tooldownload/main/version.json"

def check_for_updates(parent_window):
    """
    Checks if a newer version is available.
    If so, prompts the user to download it.
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
            msg.setText(f"កម្មវិធីកំណែថ្មី {latest_version} ត្រូវបានបញ្ចេញហើយ!\n(Version បច្ចុប្បន្ន: {APP_VERSION})\n\nព័ត៌មានបន្ថែម៖\n{release_notes}\n\nតើអ្នកចង់ទាញយកឥឡូវនេះទេ?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            
            # Change button text to Khmer
            msg.button(QMessageBox.Yes).setText("យល់ព្រម (Yes)")
            msg.button(QMessageBox.No).setText("ពេលក្រោយ (No)")
            
            retval = msg.exec_()
            if retval == QMessageBox.Yes and download_url:
                QDesktopServices.openUrl(QUrl(download_url))
                return True
                
    except Exception as e:
        # Fail silently if offline or URL doesn't exist yet
        pass
        
    return False
