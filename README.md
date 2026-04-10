# STAR SHIP System

SMS-based teacher data collection system using FastAPI and HTTSPMS.

## Prerequisites

- Python 3.14+
- HTTPSMS account (https://httpsms.com)
- ngrok
- sqlite3

## Installation

```bash
# Clone the repository
git clone https://github.com/star-ship-project/starship-system.git
cd starship-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
starship-system/
├── main.py                 # FastAPI entry point
├── backend/
│   ├── data/
│   │   └── database.py   # Database manager
│   └── services/
│       ├── sms_service.py       # SMS handling
│       ├── survey_service.py  # Survey logic
│       └── ai_service.py   # AI (deprecated)
├── frontend/
│   ├── login_page.html
│   ├── login.js
│   └── dashboard/
├── database/
│   ├── schema.sql
│   └── seed.sql
└── star.db
```

## Configuration

1. Create a `.env` file in the project root:

```env
HTTPSMS_API_KEY=your_httpsms_api_key
FROM_NUMBER=+639123456789
```

2. Make a python environment, then do:
```bash
pip install -r "requirements.txt"
```

### Running the Server

```bash
./venv/bin/uvicorn main:app --reload
```

The server runs at `http://localhost:8000`

## Webhook Setup

1. start ngrok on port 8000:
   ```bash
   ngrok http 8000
   ```

2. Go to HTTPSMS Dashboard → Settings →  Add Webhook

3. Create a new webhook with the ngrok URL but append "/webhook": `https://your-domain.com/webhook`

4. ONLY enable the "message.phone.received" event in the webhoook.

5. The phone number in the webhook should be the phone number of the sender.

## HTTPSMS Setup

1. On an android phone download the HTTPSMS app.

2. Input your API key from the HTTPSMS website and also input the same phone number used in FROM_NUMBER.

3. Phone should now be active.

## SMS Survey Flow

From a different phone number send a message to the number you put in FROM_NUMBER to initiate the bot.

The system collects teacher data via SMS in 10 steps:

| Step | Question |
|------|----------|
| 1 | DepEd ID |
| 2 | School ID (or N/A) |
| 3 | Full Name [Last],[First],[Middle],[Suffix] |
| 4 | Age (e.g., 30 or "thirty") |
| 5 | Sex (Lalake/ Babae) |
| 6 | Years of teaching (e.g., "10 years" or "10 taon") |
| 7 | Position |
| 8 | Specialization |
| 9 | Internet access? (yes/no) |
| 10 | Number of devices |

## Database Setup (Optional)

The server will automatically create the database schema on startup. To populate it with sample data:

```bash
sqlite3 star.db < database/seed.sql
```


## Frontend

The server runs at `http://localhost:8000`. The frontend is served through FastAPI:

- Login page: `http://localhost:8000/`
- Dashboard: `http://localhost:8000/frontend/dashboard/index.html`

**Login Credentials:**
- Username: `admin1`
- Password: `12345`

## API Endpoints

- `GET /api/schools` - List all schools
- `GET /api/teachers-bio` - List teacher bios
- `GET /api/teachers-professional` - List professional data
- `GET /api/qualifications` - List qualifications
- `GET /api/star-events` - List STAR events
