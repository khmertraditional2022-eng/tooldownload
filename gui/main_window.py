import os
import shutil
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QProgressBar, QLabel, QMessageBox, QHeaderView, QAbstractItemView,
                             QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from core.scraper import scrape_episodes
from core.downloader import download_episode

class ScraperThread(QThread):
    finished = pyqtSignal(list, str)
    error = pyqtSignal(str)

    def __init__(self, url, platform):
        super().__init__()
        self.url = url
        self.platform = platform

    def run(self):
        try:
            episodes = scrape_episodes(self.url, self.platform)
            if episodes:
                self.finished.emit(episodes, "")
            else:
                self.error.emit(f"រកមិនឃើញភាគណាមួយទេ! អាចមកពី {self.platform} មិនទាន់គាំទ្រការទាញយកគ្រប់ភាគ ឬ Link ខុស។")
        except Exception as e:
            self.error.emit(str(e))

class DownloadThread(QThread):
    progress = pyqtSignal(int, int, str) # current_ep_index, percent, status
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, episodes, output_dir):
        super().__init__()
        self.episodes = episodes
        self.output_dir = output_dir

    def run(self):
        for i, ep in enumerate(self.episodes):
            try:
                self.progress.emit(i, 0, "កំពុងទាញយក...")
                # Download episode
                download_url = ep.get('stream_url') or ep['url']
                success = download_episode(download_url, ep['title'], self.output_dir, 
                                 progress_callback=lambda p: self.progress.emit(i, p, "កំពុងទាញយក..."))
                if success:
                    self.progress.emit(i, 100, "ជោគជ័យ")
                else:
                    self.progress.emit(i, 0, "បរាជ័យ")
            except Exception as e:
                self.progress.emit(i, 0, f"កំហុស: {str(e)}")
        
        self.finished.emit()


from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_platform = "ReelShort"
        self.setWindowTitle("ReelShort & DramaBox Downloader - ទាញយកវីដេអូ")
        
        # Set Window Icon
        import sys
        base_path = getattr(sys, '_MEIPASS', os.getcwd())
        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.resize(800, 600)
        
        self.episodes = []
        
        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Reel_Drama_Downloads")
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        except Exception:
            self.output_dir = os.path.expanduser("~")

        self.apply_styles()
        self.init_ui()

    def apply_styles(self):
        style = """
        * {
            font-family: "Battambang", "Inter", "Segoe UI", sans-serif;
        }
        QMainWindow {
            background-color: #1e1e2e;
        }
        QLabel {
            color: #cdd6f4;
            font-size: 14px;
            font-weight: 500;
        }
        QLineEdit {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 1px solid #89b4fa;
            background-color: #1e1e2e;
        }
        QPushButton {
            background-color: #89b4fa;
            color: #11111b;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #b4befe;
        }
        QPushButton:pressed {
            background-color: #74c7ec;
        }
        QPushButton:disabled {
            background-color: #45475a;
            color: #a6adc8;
        }
        QPushButton[checkable="true"] {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
        }
        QPushButton[checkable="true"]:checked {
            background-color: #89b4fa;
            color: #11111b;
            border: 1px solid #89b4fa;
        }
        QPushButton[checkable="true"]:hover {
            background-color: #45475a;
        }
        QPushButton[checkable="true"]:checked:hover {
            background-color: #b4befe;
        }
        QTableWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
            gridline-color: #313244;
            border: 1px solid #45475a;
            border-radius: 6px;
            outline: none;
        }
        QTableWidget::item {
            padding: 4px;
        }
        QTableWidget::item:alternate {
            background-color: #181825;
        }
        QTableWidget::item:selected {
            background-color: #313244;
            color: #89b4fa;
        }
        QHeaderView::section {
            background-color: #11111b;
            color: #a6adc8;
            padding: 8px;
            border: none;
            border-right: 1px solid #313244;
            border-bottom: 1px solid #313244;
            font-weight: bold;
        }
        QProgressBar {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 6px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #a6e3a1;
            border-radius: 4px;
        }
        """
        self.setStyleSheet(style)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Top Bar (Platform Selector)
        top_bar_layout = QHBoxLayout()
        self.platform_label = QLabel("ជ្រើសរើស Platform:")
        top_bar_layout.addWidget(self.platform_label)
        
        platforms = [
            "ReelShort", "DramaBox"
        ]
        self.platform_buttons = {}
        for p in platforms:
            btn = QPushButton(p)
            btn.setCheckable(True)
            if p == self.current_platform:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, plat=p: self.change_platform(plat))
            top_bar_layout.addWidget(btn)
            self.platform_buttons[p] = btn
            
        top_bar_layout.addStretch()
        layout.addLayout(top_bar_layout)

        # Input Area
        self.input_label = QLabel(f"Link របស់ {self.current_platform}:")
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(f"សូមបញ្ចូល Link {self.current_platform} នៅទីនេះ...")
        self.analyze_btn = QPushButton("វិភាគ (Analyze)")
        self.analyze_btn.clicked.connect(self.start_analyze)
        
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.analyze_btn)
        
        layout.addLayout(input_layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ចំណងជើង (Title)", "ស្ថានភាព (Status)", "ដំណើរការ (Progress)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 220)
        self.table.horizontalHeader().setMinimumHeight(45) # Prevent header text clipping
        self.table.verticalHeader().setDefaultSectionSize(45) # Prevent row text clipping
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        # Bottom Area
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("ត្រៀមខ្លួនរួចរាល់")
        
        self.save_dir_label = QLabel(f"ទីតាំងរក្សាទុក: {self.output_dir}")
        self.save_btn = QPushButton("ប្តូរទីតាំង (Change Folder)")
        self.save_btn.clicked.connect(self.choose_save_dir)
        
        self.cookie_label = QLabel("Cookies: គ្មានទេ (No)")
        if os.path.exists(self.get_cookie_path()):
            self.cookie_label.setText("Cookies: មាន (Yes)")
            
        self.cookie_btn = QPushButton("នាំចូល Cookies (Import)")
        self.cookie_btn.clicked.connect(self.import_cookies)
        
        self.download_btn = QPushButton("ទាញយកទាំងអស់ (Download All)")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.start_download)
        
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.cookie_label)
        bottom_layout.addWidget(self.cookie_btn)
        bottom_layout.addWidget(self.save_dir_label)
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.download_btn)
        
        layout.addLayout(bottom_layout)

    def choose_save_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "ជ្រើសរើសទីតាំងរក្សាទុកវីដេអូ")
        if dir_path:
            self.output_dir = dir_path
            self.save_dir_label.setText(f"ទីតាំងរក្សាទុក: {self.output_dir}")
            
    def get_cookie_path(self):
        app_data = os.path.join(os.path.expanduser("~"), ".downloadreel")
        if not os.path.exists(app_data):
            try:
                os.makedirs(app_data)
            except Exception:
                pass
        return os.path.join(app_data, "cookies.txt")

    def import_cookies(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "ជ្រើសរើសឯកសារ Cookies", "", "Text Files (*.txt)")
        if file_path:
            try:
                dest = self.get_cookie_path()
                shutil.copy2(file_path, dest)
                self.cookie_label.setText("Cookies: មាន (Yes)")
                QMessageBox.information(self, "ជោគជ័យ", "បាននាំចូល Cookies ដោយជោគជ័យ!")
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចនាំចូល Cookies បានទេ: {e}")

    def change_platform(self, platform_name):
        self.current_platform = platform_name
        self.setWindowTitle(f"{platform_name} Downloader - ទាញយកវីដេអូ")
        self.input_label.setText(f"Link របស់ {platform_name}:")
        self.url_input.setPlaceholderText(f"សូមបញ្ចូល Link {platform_name} នៅទីនេះ...")
        
        for p, btn in self.platform_buttons.items():
            btn.setChecked(p == platform_name)

    def start_analyze(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "កំហុស", "សូមបញ្ចូល Link ជាមុនសិន!")
            return
            
        self.analyze_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.status_label.setText("កំពុងវិភាគ...")
        self.table.setRowCount(0)
        self.episodes = []
        
        self.scraper_thread = ScraperThread(url, self.current_platform)
        self.scraper_thread.finished.connect(self.on_analyze_finished)
        self.scraper_thread.error.connect(self.on_analyze_error)
        self.scraper_thread.start()

    def on_analyze_finished(self, episodes, message):
        self.episodes = episodes
        self.analyze_btn.setEnabled(True)
        self.status_label.setText(f"រកឃើញ {len(episodes)} ភាគ")
        
        self.table.setRowCount(len(episodes))
        for i, ep in enumerate(episodes):
            self.table.setItem(i, 0, QTableWidgetItem(ep['title']))
            self.table.setItem(i, 1, QTableWidgetItem("រង់ចាំ..."))
            
            progress = QProgressBar()
            progress.setValue(0)
            self.table.setCellWidget(i, 2, progress)
            
        if self.episodes:
            self.download_btn.setEnabled(True)

    def on_analyze_error(self, error_msg):
        self.analyze_btn.setEnabled(True)
        self.status_label.setText("កំហុសក្នុងការវិភាគ")
        QMessageBox.critical(self, "កំហុស", error_msg)

    def start_download(self):
        if not self.episodes:
            return
            
        self.analyze_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.status_label.setText("កំពុងទាញយក...")
        
        self.download_thread = DownloadThread(self.episodes, self.output_dir)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def update_progress(self, index, percent, status):
        self.table.setItem(index, 1, QTableWidgetItem(status))
        progress_widget = self.table.cellWidget(index, 2)
        if progress_widget:
            progress_widget.setValue(percent)

    def on_download_finished(self):
        self.analyze_btn.setEnabled(True)
        self.download_btn.setEnabled(True)
        self.status_label.setText("ការទាញយកបានបញ្ចប់!")
        QMessageBox.information(self, "ជោគជ័យ", f"ទាញយកចប់សព្វគ្រប់! វីដេអូរួចរាល់នៅក្នុង Folder:\n{self.output_dir}")
