# Build Session - BookingApp

## Getting Started

### Prerequisites
Make sure you have the following installed on your system:
- Python 3.7 or higher
- Pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://gitlab.mpharma.com/engineering/backend/build-session-bookingapp.git
   cd build-session-bookingapp
   ```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the API
Run the following commands to start the FastAPI server and initialize the SQLite database:

```bash
uvicorn app:app --reload
```
Open your browser and visit http://127.0.0.1:8000/docs to access the documentation. Use the /docs endpoint to interact with the API and create sample data.

### Running the tests
Run the following command to run the tests:
```bash
pytest
```
