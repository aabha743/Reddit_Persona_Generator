# Reddit User Persona Generator 🎯

A powerful tool that generates detailed user personas from Reddit activity using AI and natural language processing. The tool analyzes a user's Reddit history to create comprehensive personality profiles, complete with behavior patterns, motivations, and frustrations.

## Features ✨

- **Reddit Data Scraping**: Fetches user activity data from Reddit
- **AI-Powered Analysis**: Generates detailed persona sketches using advanced language models
- **Dynamic Avatar Generation**: Creates unique avatars based on user characteristics
- **Multiple Export Options**: Download personas in both PDF and TXT formats
- **Modern UI**: Clean, responsive interface with dark theme support
- **Real-time Progress Tracking**: Visual feedback during persona generation

## Getting Started 🚀

### Prerequisites

- Python 3.8 or higher
- Reddit API credentials
- Groq key (for persona generation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
API_KEY=your_groq_api_key
```

### Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`
3. Enter a Reddit username and click "Generate Persona"
4. Download the generated persona in PDF or TXT format

## Project Structure 📁

```
persona_generator/
├── app.py                 # Main Streamlit application
├── scraper/               # Reddit data scraping modules
├── processor/             # Data cleaning and processing
├── llm_engine/            # AI persona generation
├── export/                # PDF and text export utilities
├── avatar/                # Avatar generation module
├── assets/                # Static assets and fonts
└── data/                  # Data storage
    ├── raw/               # Raw scraped data
    ├── cleaned/           # Processed data
    └── personas/          # Generated personas
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Reddit API
- Groq
- DiceBear Avatars
- Streamlit
- FPDF
