# 📊 Career Market Engine

![Daily Sync](https://github.com/boraneak/career-market-engine/actions/workflows/daily_scrape.yml/badge.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://career-market-engine.streamlit.app/)

An **AI-powered job market tracker** that automatically scrapes tech roles daily using Docker + GitHub Actions, parses them with Groq AI, and visualizes opportunities in an interactive Streamlit dashboard.

---

## 🎯 What is Career Market Engine?

Career Market Engine is a fully automated pipeline that:
- **Fetches** the latest tech job listings daily from trusted sources
- **Parses** job data using advanced AI (Groq's Llama model)
- **Stores** structured job records in SQLite for quick searches
- **Displays** a live dashboard with powerful filtering and search capabilities

Perfect for job seekers tracking market trends, career analysts, and tech talent scouts.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/boraneak/career-market-engine.git
   cd career-market-engine
   ```

2. **Create environment file**
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the pipeline**
   ```bash
   python runner.py
   ```

5. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

Visit `http://localhost:8501` in your browser.

---

## 🏗️ Architecture

```
SimplifyJobs Repository (Source)
         ↓
   [Ingester] - Fetches README from SimplifyJobs
         ↓
   [Parser] - AI extracts jobs using Groq API
         ↓
   [Warehouse] - Stores in SQLite database
         ↓
   [Streamlit App] - Interactive dashboard
```

### Pipeline Components

| Module | Purpose |
|--------|---------|
| `ingester.py` | Fetches job markdown from SimplifyJobs GitHub |
| `parser.py` | Parses markdown using Groq AI into structured JSON |
| `warehouse.py` | Stores job records in SQLite with deduplication |
| `app.py` | Streamlit dashboard with search & filter |
| `runner.py` | Orchestrates the full pipeline |
| `config.py` | Centralized configuration |

---

## 🤖 Why Groq?

- **Speed**: Sub-second LLM responses
- **Cost-effective**: Generous free tier
- **Reliable**: Consistent JSON parsing
- **Low latency**: Perfect for automated pipelines

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Your Groq API key
PROJECT_NAME = "Career Market Engine"     # App title
DB_PATH = "career_market.db"              # SQLite database location
GITHUB_URL = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md"
```

---

## 📦 Docker Deployment

Build and run in Docker:

```bash
docker build -t career-market-engine .
docker run -e GROQ_API_KEY=your_key -p 8501:8501 career-market-engine
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE global_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT UNIQUE,           -- Slugified company-title
    title TEXT,                    -- Job title
    company TEXT,                  -- Company name
    location TEXT,                 -- Location (Remote/City)
    link TEXT,                     -- Application URL
    skills TEXT                    -- Extracted skills (comma-separated)
);
```

---

## 🎛️ Dashboard Features

- **Real-time Search**: Find jobs by company or title
- **Location Filtering**: Multi-select by remote, city, or region
- **Market Metrics**: Total roles analyzed & companies represented
- **Direct Apply**: One-click links to applications
- **Last Updated**: Data freshness timestamp

---

## ⚡ Automation with GitHub Actions

The pipeline runs **daily** via GitHub Actions (see `.github/workflows/`):
- Fetches latest jobs
- Runs the full pipeline
- Updates the database
- Keeps dashboard fresh

---

## 🙏 Acknowledgments & Credits

**Special thanks to [SimplifyJobs](https://github.com/SimplifyJobs/New-Grad-Positions)** for maintaining the comprehensive job board that powers this project.

This engine relies on:
- **SimplifyJobs Community** - For curating and updating tech job listings daily
- **Groq API** - For fast, reliable AI parsing
- **Streamlit** - For the interactive dashboard framework
- **Python Community** - Open source tools & libraries

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GROQ_API_KEY not found` | Create `.env` file with your key |
| `Warehouse not found` | Run `python runner.py` first |
| Rate limit errors | Check Groq API limits; wait 60 seconds |
| Database locked | Ensure no other processes are accessing `career_market.db` |

---

## 💡 Use Cases

- **Job Seekers**: Track hiring trends in tech
- **Career Coaches**: Show market demand to clients
- **Talent Scouts**: Monitor competitor hiring
- **Data Analysts**: Analyze job market trends
- **Researchers**: Study tech industry hiring patterns

---

## 🚀 Future Enhancements

- [ ] Salary range extraction
- [ ] Skills demand analytics
- [ ] Company profile scraping
- [ ] Notification system for matching roles
- [ ] Export to CSV/PDF
- [ ] Email digest feature
- [ ] Multi-language support

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---
