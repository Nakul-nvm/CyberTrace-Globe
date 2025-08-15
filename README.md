# CyberTrace Globe 🌐

A stunning, real-time 3D visualization of simulated global cyberattacks, built with Python, FastAPI, and Globe.gl.

**Live Demo:** [CyberTrace Globe](https://cyber-trace-globe.vercel.app/)

---

https://github.com/user-attachments/assets/639a65d8-99ce-4ce3-908f-3cb521e0a3f9

## ✨ Features

- **Interactive 3D Globe**: A fully interactive and pannable 3D globe rendered with Globe.gl.
- **Real-time Updates**: New attack visualizations are pushed from the server to the client in real-time using WebSockets.
- **Authentic Simulation**: The simulation uses a cached list of real, recently reported malicious IP locations from the AbuseIPDB API.
- **Dynamic Visualization**: Attack arcs are color-coded and originate from and target the glowing coordinates of real malicious IPs.
- **High-Performance Backend**: Built with FastAPI, a modern, high-performance Python web framework.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, Server-Sent Events (SSE)
- **Frontend**: HTML5, CSS3, JavaScript, Globe.gl (Three.js)
- **Data Source**: AbuseIPDB API (for initial data caching)
- **Deployment**: Vercel

## 🚀 Getting Started

To run this project locally, follow these steps:

### Prerequisites

- Python 3.8+
- Git
- An API Key from [AbuseIPDB](https://www.abuseipdb.com/api)

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Nakul-nvm/CyberTrace-Globe.git
    cd CyberTrace-Globe
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    # Create a virtual environment
    python -m venv venv
    # Activate it (Windows)
    .\venv\Scripts\activate
    # Activate it (macOS/Linux)
    source venv/bin/activate

    # Install required packages
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**

    - Create a new file named `.env` in the root of the project.
    - Add your API key to it:
      ```
      ABUSEIPDB_API_KEY='your_actual_api_key_goes_here'
      ```

4.  **Generate the initial data cache:**

    - Run the `update_cache.py` script once to fetch data from the API and create your `cache.json` file.
      ```bash
      python update_cache.py
      ```

5.  **Run the backend server:**

    ```bash
    uvicorn api.index:app --reload
    ```

    Your backend is now running at `http://127.0.0.1:8000`.

6.  **Run the frontend:**
    - Open the `index.html` file with a live server extension (like the one in VS Code).

## 🙏 Acknowledgements

- **Globe.gl** for the amazing 3D globe library.
- **FastAPI** for a fantastic backend framework.
- **AbuseIPDB** for providing the threat intelligence data.
