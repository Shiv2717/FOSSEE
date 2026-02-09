"""
PyQt5 Desktop Application for Chemical Equipment Visualizer API

This desktop application connects to the Django REST API to upload CSV files
and display equipment statistics.

Requirements:
    pip install PyQt5 requests python-dotenv

Usage:
    python desktop_app.py

Configuration:
    Set API credentials in .env file in the project root:
    DESKTOP_API_URL=http://localhost:8000
    DESKTOP_API_USERNAME=admin
    DESKTOP_API_PASSWORD=your-password
    
Make sure the Django API is running.
"""

import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Import configuration
try:
    from config import API_UPLOAD_URL, DESKTOP_API_URL, DESKTOP_API_USERNAME, DESKTOP_API_PASSWORD
except ImportError:
    # Fallback if config.py is not found
    API_UPLOAD_URL = 'http://localhost:8000/api/upload/'
    DESKTOP_API_URL = 'http://localhost:8000'
    DESKTOP_API_USERNAME = 'admin'
    DESKTOP_API_PASSWORD = 'admin123'

API_BASE_URL = DESKTOP_API_URL


# =============================================================================
# API Worker Thread (for non-blocking API calls)
# =============================================================================
class UploadWorker(QThread):
    """
    Background thread for uploading files to prevent UI freezing.
    """
    # Signals to communicate with main thread
    upload_success = pyqtSignal(dict)  # Emits response data on success
    upload_error = pyqtSignal(str)     # Emits error message on failure
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """
        Execute the file upload in a background thread.
        """
        try:
            # Open and read the CSV file
            with open(self.file_path, 'rb') as f:
                files = {'csv_file': f}
                
                # Make POST request to API with Basic Auth
                response = requests.post(
                    API_UPLOAD_URL,
                    files=files,
                    auth=(DESKTOP_API_USERNAME, DESKTOP_API_PASSWORD),
                    timeout=30
                )
            
            # Check response status
            if response.status_code == 201:
                # Success - emit data
                data = response.json()
                self.upload_success.emit(data)
            else:
                # API returned error
                error_msg = None
                try:
                    payload = response.json()
                    error_msg = payload.get('error') or payload.get('detail')
                except ValueError:
                    payload = None

                if not error_msg:
                    error_msg = response.text.strip() or 'Unknown error'

                self.upload_error.emit(
                    f"API Error ({response.status_code}): {error_msg}"
                )
                
        except requests.exceptions.ConnectionError:
            self.upload_error.emit(
                "Connection Error: Unable to connect to API.\n"
                "Make sure Django server is running on localhost:8000"
            )
        except requests.exceptions.Timeout:
            self.upload_error.emit("Request timeout. Please try again.")
        except Exception as e:
            self.upload_error.emit(f"Error: {str(e)}")


# =============================================================================
# Main Application Window
# =============================================================================
class EquipmentVisualizerApp(QMainWindow):
    """
    Main application window for Chemical Equipment Visualizer.
    """
    
    def __init__(self):
        super().__init__()
        self.upload_worker = None
        self.current_data = None  # Store uploaded data for future chart generation
        self.chart_canvas = None  # Store canvas reference for chart updates
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        """
        # Window settings
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # =================================================================
        # Header Section
        # =================================================================
        header_label = QLabel('Chemical Equipment Visualizer')
        header_label.setFont(QFont('Arial', 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #667eea; padding: 20px;")
        main_layout.addWidget(header_label)
        
        # =================================================================
        # Upload Section
        # =================================================================
        upload_group = QGroupBox("Upload CSV File")
        upload_group.setFont(QFont('Arial', 11, QFont.Bold))
        upload_layout = QHBoxLayout()
        
        # Selected file label
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet("padding: 5px; color: #666;")
        upload_layout.addWidget(self.file_label, stretch=1)
        
        # Browse button
        self.browse_btn = QPushButton('Browse...')
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #764ba2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_file)
        upload_layout.addWidget(self.browse_btn)
        
        # Upload button
        self.upload_btn = QPushButton('Upload & Analyze')
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        upload_layout.addWidget(self.upload_btn)
        
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)
        
        # =================================================================
        # Statistics Section
        # =================================================================
        stats_group = QGroupBox("Equipment Statistics")
        stats_group.setFont(QFont('Arial', 11, QFont.Bold))
        stats_layout = QVBoxLayout()
        
        # Statistics labels with larger font
        self.stats_label = QLabel('Upload a CSV file to see statistics')
        self.stats_label.setFont(QFont('Arial', 12))
        self.stats_label.setStyleSheet("padding: 10px; color: #333;")
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        # =================================================================
        # Details Section (Scrollable Text Area)
        # =================================================================
        details_group = QGroupBox("Upload Details")
        details_group.setFont(QFont('Arial', 11, QFont.Bold))
        details_layout = QVBoxLayout()
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText(
            "Detailed information about uploaded equipment will appear here..."
        )
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        details_layout.addWidget(self.details_text)
        
        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group, stretch=1)
        
        # =================================================================
        # Chart Section (for Matplotlib integration)
        # =================================================================
        self.chart_group = QGroupBox("Data Visualization")
        self.chart_group.setFont(QFont('Arial', 11, QFont.Bold))
        self.chart_layout = QVBoxLayout()
        
        self.chart_placeholder = QLabel('Charts will be displayed here after uploading CSV')
        self.chart_placeholder.setAlignment(Qt.AlignCenter)
        self.chart_placeholder.setStyleSheet("color: #999; padding: 40px; font-style: italic;")
        self.chart_layout.addWidget(self.chart_placeholder)
        
        self.chart_group.setLayout(self.chart_layout)
        main_layout.addWidget(self.chart_group, stretch=1)
        
        # =================================================================
        # Status Bar
        # =================================================================
        self.status_label = QLabel('Ready')
        self.status_label.setStyleSheet("padding: 5px; color: #666;")
        self.statusBar().addWidget(self.status_label)
        
        # API connection indicator
        self.api_status = QLabel(f'API: {API_BASE_URL}')
        self.api_status.setStyleSheet("padding: 5px; color: #28a745;")
        self.statusBar().addPermanentWidget(self.api_status)
    
    def browse_file(self):
        """
        Open file dialog to select CSV file.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.setText(f'Selected: {filename}')
            self.file_label.setStyleSheet("padding: 5px; color: #28a745; font-weight: bold;")
            self.upload_btn.setEnabled(True)
            self.status_label.setText('File selected. Click "Upload & Analyze" to continue.')
    
    def upload_file(self):
        """
        Upload selected file to API.
        """
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, 'Warning', 'Please select a file first.')
            return
        
        # Disable buttons during upload
        self.upload_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.status_label.setText('Uploading file...')
        self.details_text.setText('Processing...')
        
        # Create and start upload worker thread
        self.upload_worker = UploadWorker(self.selected_file)
        self.upload_worker.upload_success.connect(self.on_upload_success)
        self.upload_worker.upload_error.connect(self.on_upload_error)
        self.upload_worker.finished.connect(self.on_upload_finished)
        self.upload_worker.start()
    
    def on_upload_success(self, data):
        """
        Handle successful upload response.
        
        Args:
            data (dict): API response data
        """
        self.current_data = data  # Store for future chart generation
        
        # Extract data from response
        response_data = data.get('data', {})
        equipment_count = response_data.get('equipment_count', 0)
        avg_flowrate = response_data.get('avg_flowrate', 0)
        avg_pressure = response_data.get('avg_pressure', 0)
        avg_temperature = response_data.get('avg_temperature', 0)
        
        # Update statistics label
        stats_text = f"""
        <h3 style="color: #28a745;">✓ Upload Successful!</h3>
        <p style="font-size: 14px;">
        <b>Total Equipment Count:</b> {equipment_count}<br>
        <b>Average Flowrate:</b> {avg_flowrate:.2f}<br>
        <b>Average Pressure:</b> {avg_pressure:.2f}<br>
        <b>Average Temperature:</b> {avg_temperature:.2f}
        </p>
        """
        self.stats_label.setText(stats_text)
        
        # Update details text area
        details = f"""
Upload Details
{'='*60}
Message: {data.get('message', 'N/A')}

Equipment Statistics
{'='*60}
Total Equipment: {equipment_count}
Average Flowrate: {avg_flowrate:.2f}
Average Pressure: {avg_pressure:.2f}
Average Temperature: {avg_temperature:.2f}

Equipment Type Distribution
{'='*60}
"""
        
        # Add type distribution if available
        type_dist = response_data.get('type_distribution', {})
        if type_dist:
            for eq_type, count in type_dist.items():
                details += f"{eq_type}: {count}\n"
        
        self.details_text.setText(details)
        self.status_label.setText('Upload successful!')
        
        # Show success message
        QMessageBox.information(
            self,
            'Success',
            f'CSV file uploaded successfully!\n\nTotal Equipment: {equipment_count}'
        )
        
        # Generate Matplotlib charts
        self.generate_charts(self.current_data)
    
    def on_upload_error(self, error_message):
        """
        Handle upload error.
        
        Args:
            error_message (str): Error message to display
        """
        self.stats_label.setText(f'<span style="color: red;">✗ Upload Failed</span>')
        self.details_text.setText(f'ERROR:\n{error_message}')
        self.status_label.setText('Upload failed')
        
        # Show error dialog
        QMessageBox.critical(self, 'Upload Error', error_message)
    
    def on_upload_finished(self):
        """
        Re-enable buttons after upload completes (success or failure).
        """
        self.upload_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
    
    # =========================================================================
    # Matplotlib Chart Generation Methods
    # =========================================================================
    def generate_charts(self, data):
        """
        Generate Matplotlib charts from uploaded data.
        
        Args:
            data (dict): API response data containing statistics
        """
        try:
            response_data = data.get('data', {})
            type_distribution = response_data.get('type_distribution', {})
            avg_flowrate = response_data.get('avg_flowrate', 0)
            avg_pressure = response_data.get('avg_pressure', 0)
            avg_temperature = response_data.get('avg_temperature', 0)
            
            # Create figure with two subplots
            fig = Figure(figsize=(12, 4), dpi=100)
            
            # Chart 1: Equipment Type Distribution (Pie Chart)
            ax1 = fig.add_subplot(121)
            if type_distribution:
                types = list(type_distribution.keys())
                counts = list(type_distribution.values())
                colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
                ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)])
                ax1.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold')
            else:
                ax1.text(0.5, 0.5, 'No type data', ha='center', va='center')
                ax1.set_title('Equipment Type Distribution', fontsize=12, fontweight='bold')
            
            # Chart 2: Average Measurements (Bar Chart)
            ax2 = fig.add_subplot(122)
            measurements = ['Flowrate', 'Pressure', 'Temperature']
            values = [avg_flowrate, avg_pressure, avg_temperature]
            colors_bar = ['#667eea', '#764ba2', '#f093fb']
            bars = ax2.bar(measurements, values, color=colors_bar)
            ax2.set_title('Average Measurements', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Value')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.2f}',
                        ha='center', va='bottom', fontsize=10)
            
            fig.tight_layout()
            
            # Clear previous chart if exists
            if self.chart_canvas is not None:
                self.chart_layout.removeWidget(self.chart_canvas)
                self.chart_canvas.deleteLater()
            
            # Hide placeholder
            if self.chart_placeholder.isVisible():
                self.chart_placeholder.setVisible(False)
            
            # Create canvas and add to layout
            self.chart_canvas = FigureCanvas(fig)
            self.chart_layout.addWidget(self.chart_canvas)
            
        except Exception as e:
            print(f"Error generating charts: {e}")
            self.chart_placeholder.setText(f'Error generating charts: {str(e)}')
            self.chart_placeholder.setVisible(True)


# =============================================================================
# Main Entry Point
# =============================================================================
def main():
    """
    Application entry point.
    """
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = EquipmentVisualizerApp()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
