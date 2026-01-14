# Ground Stone - Golf Course Audit Report Monitor

## Project Overview

Ground Stone is a Telegram bot and channel system that automatically monitors and notifies subscribers when companies in the golf course operations industry (골프장 운영업) submit their audit reports (감사보고서).

**Benchmark Reference**: @jh_python_bot

## Project Goals

Create an automated notification system that:
- Monitors DART (Data Analysis, Retrieval and Transfer System) - Korea's electronic disclosure system
- Filters companies by industry classification (golf course operations)
- Detects when audit reports are submitted
- Sends automatic push notifications to a Telegram channel
- Provides subscribers with timely access to financial information

## Technical Architecture

### Core Components

1. **DART API Integration**
   - Monitor Korea's Open DART API for new filings
   - Filter by industry code (골프장 운영업)
   - Track audit report submissions (감사보고서)

2. **Telegram Bot**
   - Python Telegram Bot library
   - Channel management for broadcasting
   - User subscription handling (optional)

3. **Scheduling System**
   - Periodic checks for new reports
   - Configurable polling intervals
   - Event-driven notifications

4. **Database**
   - Track processed reports to avoid duplicates
   - Store company information
   - Log notification history

## Key Features

### Phase 1 (MVP)
- [ ] Connect to DART Open API
- [ ] Filter companies by golf course industry classification
- [ ] Detect new audit report submissions
- [ ] Send notifications to Telegram channel
- [ ] Basic error handling and logging

### Phase 2 (Enhanced)
- [ ] Rich message formatting with report details
- [ ] Direct links to reports
- [ ] Company profile information
- [ ] Notification scheduling (business hours only)
- [ ] Admin commands for bot management

### Phase 3 (Advanced)
- [ ] Multi-industry support
- [ ] Custom alert preferences
- [ ] Report summarization using AI
- [ ] Historical data analysis
- [ ] Web dashboard for monitoring

## Technology Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: python-telegram-bot
- **API Client**: requests / httpx
- **Database**: SQLite / PostgreSQL
- **Scheduler**: APScheduler / Celery
- **Environment**: python-dotenv

### External Services
- **DART Open API**: https://opendart.fss.or.kr/
- **Telegram Bot API**: https://core.telegram.org/bots/api

## Project Structure

```
ground-stone/
├── src/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py          # Telegram command handlers
│   │   └── notifications.py     # Notification formatting
│   ├── dart/
│   │   ├── __init__.py
│   │   ├── client.py            # DART API client
│   │   └── filters.py           # Industry filtering logic
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # Database models
│   │   └── operations.py        # CRUD operations
│   └── scheduler/
│       ├── __init__.py
│       └── tasks.py             # Scheduled monitoring tasks
├── tests/
│   ├── test_dart_client.py
│   ├── test_bot.py
│   └── test_scheduler.py
├── config/
│   └── settings.py              # Configuration management
├── data/
│   └── ground-stone.db          # SQLite database
├── .env.example                 # Environment variables template
├── .gitignore
├── requirements.txt
├── README.md
├── CLAUDE.MD
└── main.py                      # Application entry point
```

## Setup Requirements

### Prerequisites
1. DART Open API Key (from https://opendart.fss.or.kr/)
2. Telegram Bot Token (from @BotFather)
3. Telegram Channel (created and bot added as admin)

### Environment Variables
```
DART_API_KEY=your_dart_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_name
DATABASE_URL=sqlite:///data/ground-stone.db
CHECK_INTERVAL_MINUTES=60
LOG_LEVEL=INFO
```

## DART API Integration Details

### Industry Classification
- **Industry Code**: Golf course operations (골프장 운영업)
- **Korean Standard Industry Code (KSIC)**: 91221

### Report Types to Monitor
- 사업보고서 (Business Report)
- 감사보고서 (Audit Report)
- 반기보고서 (Semi-annual Report)
- 분기보고서 (Quarterly Report)

### API Endpoints
- Company List: `/api/corpCode.xml`
- Report List: `/api/list.json`
- Report Document: `/api/document.xml`

## Implementation Approach

### Step 1: DART API Client
```python
class DARTClient:
    def get_companies_by_industry(self, industry_code: str) -> List[Company]
    def get_recent_reports(self, corp_code: str, start_date: str) -> List[Report]
    def check_new_audit_reports(self) -> List[Report]
```

### Step 2: Telegram Bot
```python
class AuditReportBot:
    def send_notification(self, channel_id: str, report: Report)
    def format_report_message(self, report: Report) -> str
    def handle_commands(self)  # /start, /status, /help
```

### Step 3: Scheduler
```python
class ReportMonitor:
    def schedule_periodic_check(self, interval_minutes: int)
    def check_and_notify(self)
    def process_new_reports(self, reports: List[Report])
```

## Message Format Example

```
🏌️ 새로운 감사보고서가 제출되었습니다!

📋 회사명: [회사명]
🏢 종목코드: [종목코드]
📊 보고서: 감사보고서
📅 제출일: 2026-03-15
🔗 링크: [DART 바로가기]

💼 업종: 골프장 운영업
```

## Development Workflow

1. **Setup Development Environment**
   - Clone repository
   - Install dependencies: `pip install -r requirements.txt`
   - Configure `.env` file
   - Initialize database

2. **Development Process**
   - Write tests first (TDD approach)
   - Implement features incrementally
   - Run tests: `pytest`
   - Update documentation

3. **Deployment**
   - Use systemd service or Docker container
   - Set up monitoring and logging
   - Configure automatic restarts
   - Schedule periodic health checks

## Testing Strategy

- **Unit Tests**: Individual components (API client, filters, formatters)
- **Integration Tests**: DART API connection, Telegram API connection
- **End-to-End Tests**: Complete notification flow
- **Mock Testing**: Use mock data for DART responses

## Security Considerations

- Store API keys securely (environment variables)
- Validate all external data
- Rate limiting for API calls
- Secure database access
- Telegram webhook security (if using webhooks)

## Monitoring & Logging

- Log all API requests and responses
- Track notification delivery status
- Monitor error rates and types
- Set up alerts for system failures
- Performance metrics (response times, check durations)

## Scalability Considerations

- Database indexing for quick lookups
- Caching for company information
- Asynchronous API calls
- Queue system for high-volume notifications
- Horizontal scaling with multiple workers

## Legal & Compliance

- Respect DART API rate limits
- Follow Telegram Bot API guidelines
- Ensure proper data usage rights
- Privacy considerations for user data
- Comply with Korean financial data regulations

## Future Enhancements

- Multi-language support (Korean/English)
- PDF report parsing and analysis
- Financial metrics extraction
- Trend analysis and insights
- Integration with other disclosure systems
- Mobile app companion
- Export functionality (CSV, Excel)

## Resources

- [DART Open API Documentation](https://opendart.fss.or.kr/guide/main.do)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Korean Financial Services Commission](https://www.fsc.go.kr/)

## Contributing

When contributing to this project:
1. Follow PEP 8 style guidelines
2. Write comprehensive tests
3. Update documentation
4. Use meaningful commit messages
5. Create detailed pull requests

## Support

For questions or issues:
- Create an issue in the repository
- Review DART API documentation
- Check Telegram Bot API status

---

**Note**: This project is designed for informational purposes. Users should verify all financial information through official sources.
