import React, { useState, useRef } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './App.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// API Configuration from environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_USERNAME = process.env.REACT_APP_API_USERNAME || 'admin';
const API_PASSWORD = process.env.REACT_APP_API_PASSWORD || 'admin123';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef(null);

  // Handle file selection
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
      setError(null);
      setSuccess(false);
    } else {
      setError('Please select a valid CSV file');
      setSelectedFile(null);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('csv_file', selectedFile);

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        auth: {
          username: API_USERNAME,
          password: API_PASSWORD,
        },
      });

      if (response.status === 201) {
        const payload = response.data?.data || {};
        const normalized = {
          total_records: payload.equipment_count ?? 0,
          equipment_types: payload.type_distribution || {},
          statistics: {
            avg_flowrate: payload.avg_flowrate ?? 0,
            avg_pressure: payload.avg_pressure ?? 0,
            avg_temperature: payload.avg_temperature ?? 0,
          },
          equipment: [],
        };
        setSummaryData(normalized);
        setSuccess(true);
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          'Failed to upload file. Make sure the Django API is running.'
      );
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Prepare bar chart data
  const getBarChartData = () => {
    if (!summaryData || !summaryData.statistics) {
      return null;
    }

    const stats = summaryData.statistics;
    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average Values',
          data: [
            stats.avg_flowrate || 0,
            stats.avg_pressure || 0,
            stats.avg_temperature || 0,
          ],
          backgroundColor: [
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(75, 192, 75, 0.7)',
          ],
          borderColor: [
            'rgba(54, 162, 235, 1)',
            'rgba(255, 99, 132, 1)',
            'rgba(75, 192, 75, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  // Prepare pie chart data
  const getPieChartData = () => {
    if (!summaryData || !summaryData.equipment_types) {
      return null;
    }

    const types = summaryData.equipment_types;
    const labels = Object.keys(types || {});
    const data = Object.values(types || {});

    const colors = [
      'rgba(255, 99, 132, 0.7)',
      'rgba(54, 162, 235, 0.7)',
      'rgba(255, 206, 86, 0.7)',
      'rgba(75, 192, 75, 0.7)',
      'rgba(153, 102, 255, 0.7)',
      'rgba(255, 159, 64, 0.7)',
      'rgba(199, 199, 199, 0.7)',
      'rgba(83, 102, 255, 0.7)',
    ];

    return {
      labels,
      datasets: [
        {
          data,
          backgroundColor: colors.slice(0, labels.length),
          borderColor: colors.slice(0, labels.length).map((c) =>
            c.replace('0.7', '1')
          ),
          borderWidth: 2,
        },
      ],
    };
  };

  const barChartData = getBarChartData();
  const pieChartData = getPieChartData();

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Chemical Equipment Visualizer</h1>
        <p>Upload CSV files and visualize equipment data</p>
      </header>

      <main className="app-main">
        {/* Upload Section */}
        <section className="upload-section">
          <h2>Upload Equipment CSV</h2>

          <div className="input-group">
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="file-input"
              id="csv-file"
            />
            <label htmlFor="csv-file" className="file-label">
              {selectedFile ? selectedFile.name : 'Choose CSV file...'}
            </label>
          </div>

          <button
            onClick={handleUpload}
            disabled={!selectedFile || loading}
            className="upload-button"
          >
            {loading ? 'Uploading...' : 'Upload & Analyze'}
          </button>

          {error && <div className="error-message">{error}</div>}
          {success && (
            <div className="success-message">
              ✓ File uploaded successfully!
            </div>
          )}
        </section>

        {/* Summary Section */}
        {summaryData && (
          <section className="summary-section">
            <h2>Data Summary</h2>

            <div className="summary-info">
              <div className="info-card">
                <h3>Total Equipment</h3>
                <p className="info-value">{summaryData.total_records}</p>
              </div>

              <div className="info-card">
                <h3>Equipment Types</h3>
                <p className="info-value">
                  {summaryData.equipment_types
                    ? Object.keys(summaryData.equipment_types).length
                    : 0}
                </p>
              </div>

              {summaryData.statistics && (
                <>
                  <div className="info-card">
                    <h3>Avg Flowrate</h3>
                    <p className="info-value">
                      {summaryData.statistics.avg_flowrate?.toFixed(2)}
                    </p>
                  </div>

                  <div className="info-card">
                    <h3>Avg Pressure</h3>
                    <p className="info-value">
                      {summaryData.statistics.avg_pressure?.toFixed(2)}
                    </p>
                  </div>

                  <div className="info-card">
                    <h3>Avg Temperature</h3>
                    <p className="info-value">
                      {summaryData.statistics.avg_temperature?.toFixed(2)}
                    </p>
                  </div>
                </>
              )}
            </div>

            {/* Charts Section */}
            <div className="charts-container">
              {barChartData && (
                <div className="chart-wrapper">
                  <h3>Average Metrics</h3>
                  <Bar data={barChartData} options={chartOptions} />
                </div>
              )}

              {pieChartData && (
                <div className="chart-wrapper">
                  <h3>Equipment Type Distribution</h3>
                  <Pie data={pieChartData} options={chartOptions} />
                </div>
              )}
            </div>

            {/* Equipment List */}
            {summaryData.equipment && summaryData.equipment.length > 0 && (
              <div className="equipment-list">
                <h3>Equipment Details</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Flowrate</th>
                        <th>Pressure</th>
                        <th>Temperature</th>
                      </tr>
                    </thead>
                    <tbody>
                      {summaryData.equipment.map((item, idx) => (
                        <tr key={idx}>
                          <td>{item.name}</td>
                          <td>{item.type}</td>
                          <td>{item.flowrate}</td>
                          <td>{item.pressure}</td>
                          <td>{item.temperature}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>
        )}

        {/* Empty State */}
        {!summaryData && !loading && (
          <div className="empty-state">
            <p>Upload a CSV file to see equipment data and visualizations</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Django API: <code>{API_BASE_URL}</code>
        </p>
        <p>Make sure the Django development server is running on localhost:8000</p>
      </footer>
    </div>
  );
}

export default App;
