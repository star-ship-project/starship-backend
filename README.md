# STAR SHIP System

SMS-based teacher data collection system using FastAPI and HTTSPMS.

## Prerequisites

- Python 3.14+
- HTTPSMS account (https://httpsms.com)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd starship-system

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root:

```env
HTTPSMS_API_KEY=your_httpsms_api_key
GEMINI_API_KEY=your_gemini_api_key # deprecated
FROM_NUMBER=+639123456789
```

2. Make a python environment, then do:
```bash
pip install -r "requirements.txt"
```

### Running the Server

```bash
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`

## Webhook Setup

1. For local development, use ngrok:
   ```bash
   ngrok http 8000
   ```
2. Go to HTTPSMS Dashboard → Webhooks
3. Create a new webhook with the ngrok URL but append "/webhook": `https://your-domain.com/webhook`
4. ONLY enable the "message.phone.received" event in the webhoook.
5. The phone number in the webhook should be the phone number of the sender.

## SMS Survey Flow

Send a message to initiate the bot.

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

## Frontend

Open `frontend/dashboard/index.html` in a browser to view the dashboard.

## API Endpoints

- `GET /api/schools` - List all schools
- `GET /api/teachers-bio` - List teacher bios
- `GET /api/teachers-professional` - List professional data
- `GET /api/qualifications` - List qualifications
- `GET /api/star-events` - List STAR events
