# Image and Text Comparison Pipeline

## Overview

This project demonstrates a pipeline for comparing images with text to determine their contextual relevance. The pipeline uses Selenium to extract images and text from a webpage and employs the Gemini API for initial comparison. Future improvements will include testing MM LLM models to enhance image generation and analysis.

## Features

- **Web Scraping**: Uses Selenium WebDriver to scrape webpages for images and text.
- **Image Downloading**: Downloads images from the webpage and saves them locally.
- **Text Extraction**: Saves webpage text to a file for analysis.
- **Contextual Comparison**: Utilizes the Gemini API to compare images with text and determine contextual relevance.
- **Future Enhancements**: Plan to test MM LLM models for generating and analyzing images.

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package manager)
- Selenium WebDriver for Chrome
- Gemini API key

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. **Set Up API Key:**
