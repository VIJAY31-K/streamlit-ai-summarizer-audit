# AI-Powered Audit Report Summarizer

Transform lengthy audit documents into actionable insights using AI technology.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

- **Document Processing**: Upload PDF/TXT audit reports
- **AI Summarization**: Google Gemini 2.5-Flash powered analysis
- **Financial Extraction**: Automatic detection of monetary values, percentages, ratios
- **Risk Assessment**: High/Medium/Low risk categorization
- **Compliance Checking**: Generate checklists and action items
- **Multiple Exports**: TXT, JSON, Markdown, Executive formats

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/ai-audit-summarizer.git
cd ai-audit-summarizer

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GEMINI_API_KEY=your_api_key_here" >> .env

# Launch application
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Usage

1. Upload PDF or TXT audit report
2. Select summary style and analysis type
3. Enable desired features (financial analysis, risk assessment, compliance)
4. Generate summary
5. Download in preferred format

## Project Structure

```
ai-audit-summarizer/
├── app.py              # Streamlit interface
├── summarizer.py       # AI processing logic
├── requirements.txt    # Dependencies
├── .env               # API keys (create this)
└── check_env.py       # Environment validation
```

## Performance

- Small docs (< 10 pages): 15-30 seconds
- Medium docs (10-50 pages): 30-90 seconds
- Large docs (50+ pages): 90-180 seconds

## Security

- API keys in environment variables
- Temporary file cleanup
- No document storage
- Input validation

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - see [LICENSE](LICENSE) file.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "GEMINI key not found" | Check `.env` file exists with valid API key |
| Slow processing | Check internet connection, try smaller documents |
| PDF extraction fails | Ensure PDF has selectable text |

## Support

- [Issues](https://github.com/yourusername/ai-audit-summarizer/issues)
- [Discussions](https://github.com/yourusername/ai-audit-summarizer/discussions)

---

**Note**: Requires Google Gemini API key from [Google AI Studio](https://makersuite.google.com/).

**Disclaimer**: AI-generated analysis should be reviewed by qualified professionals.
