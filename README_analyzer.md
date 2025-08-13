# Tax Notice Analyzer & Response Drafter

A comprehensive AI-powered tool for analyzing tax notices and drafting professional responses using Google's Gemini AI.

## Features

### 📄 Input Methods

- **PDF Upload**: Upload tax notice PDF files with automatic text extraction
- **Text Input**: Copy and paste notice content directly

### 📊 Intelligent Analysis

- **Notice Classification**: Identifies type of notice (Assessment, Demand, Show Cause, etc.)
- **Key Details Extraction**: Extracts notice number, dates, taxpayer details, amounts
- **Financial Impact**: Analyzes tax amounts, penalties, and total liability
- **Issue Identification**: Highlights main concerns and discrepancies
- **Action Items**: Lists required actions and deadlines
- **Urgency Assessment**: Rates urgency level based on consequences

### ✍️ Response Drafting

- **Multiple Response Types**:
  - Full Compliance
  - Request Extension
  - Dispute Assessment
  - Partial Agreement
  - Request Hearing
- **Professional Format**: Generates properly structured response letters
- **Legal References**: Includes appropriate legal sections and provisions
- **Editable Drafts**: Review and customize generated responses
- **Download Feature**: Export responses as text files

### 📅 Timeline Management

- **Date Extraction**: Identifies all important dates from notices
- **Deadline Tracking**: Calculates days remaining for responses
- **Reminder System**: Provides actionable reminders and next steps

## Installation & Setup

1. **Install Dependencies**:

   ```bash
   pip install -r requirements_analyzer.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run the Application**:
   ```bash
   streamlit run tax_notice_analyzer.py
   ```

## Usage Guide

### Step 1: Input Notice

- Choose either "Upload PDF" or "Paste Text"
- For PDF upload: Select your tax notice PDF file
- For text input: Copy and paste the notice content
- Review extracted/pasted text for accuracy

### Step 2: Configure Response

- Select appropriate response type from sidebar:
  - **Compliance**: Accept and comply with notice
  - **Request Extension**: Ask for more time to respond
  - **Dispute Assessment**: Challenge the assessment
  - **Partial Agreement**: Agree with some points only
  - **Request Hearing**: Ask for personal hearing

### Step 3: Analyze Notice

- Click "Analyze Notice" to get comprehensive analysis
- Review extracted details, financial implications, and required actions
- Understand urgency level and main issues

### Step 4: Draft Response

- Click "Draft Response" to generate professional response letter
- Review and edit the generated draft as needed
- Download the final response as a text file

### Step 5: Manage Timeline

- Click "Extract Timeline" to see all important dates
- Set calendar reminders for deadlines
- Follow the provided action checklist

## Features Overview

### Smart Analysis Engine

The AI analyzes notices for:

- **Legal Sections**: Identifies which tax laws are being invoked
- **Financial Details**: Extracts amounts, penalties, interest
- **Deadlines**: Finds all critical dates and response deadlines
- **Required Actions**: Lists what taxpayer needs to do
- **Risk Assessment**: Evaluates consequences of non-compliance

### Professional Response Generation

Generates responses that include:

- **Proper Legal Format**: Following standard legal correspondence format
- **Acknowledgment**: Professional acknowledgment of notice receipt
- **Point-by-Point Response**: Addresses each issue raised
- **Supporting Documentation**: Lists required documents
- **Professional Conclusion**: Respectful and legally appropriate closing

### User-Friendly Interface

- **Clean Design**: Modern, professional Streamlit interface
- **Color-Coded Sections**: Different colors for analysis, responses, warnings
- **Progress Indicators**: Clear feedback during processing
- **Editable Content**: All generated content can be reviewed and modified
- **Download Options**: Export responses for official submission

## Technical Details

### AI Model

- **Google Gemini 1.5-Flash**: For natural language processing and generation
- **Temperature 0.3**: Balanced between creativity and consistency
- **Structured Prompts**: Carefully crafted prompts for accurate analysis

### PDF Processing

- **PyPDF2**: Reliable PDF text extraction
- **Error Handling**: Graceful handling of corrupted or image-based PDFs
- **Text Cleanup**: Automatic cleaning of extracted text

### Data Security

- **Local Processing**: All analysis happens locally
- **No Data Storage**: No notice content is stored permanently
- **API Security**: Secure handling of API keys through environment variables

## Troubleshooting

### Common Issues

1. **API Key Error**:

   - Ensure `.env` file is in the same directory as the script
   - Verify your Gemini API key is valid and active
   - Check if API key has sufficient quota

2. **PDF Extraction Issues**:

   - Try converting PDF to text format if extraction fails
   - Ensure PDF is not password protected
   - For image-based PDFs, consider using OCR tools first

3. **Poor Analysis Quality**:
   - Ensure notice text is complete and readable
   - Remove any irrelevant content before analysis
   - Check if notice is in English (tool works best with English content)

## Best Practices

### For Best Results

1. **Clean Input**: Ensure notice text is complete and clearly readable
2. **Review Analysis**: Always review AI analysis for accuracy
3. **Customize Response**: Edit generated responses to match your specific situation
4. **Professional Review**: Have responses reviewed by tax professionals
5. **Timely Submission**: Submit responses well before deadlines

### Legal Disclaimer

This tool provides AI-generated analysis and draft responses for reference only. Always consult with qualified tax professionals before submitting official responses to tax authorities.

## Support

For issues or questions:

1. Check this README for common solutions
2. Verify all dependencies are properly installed
3. Ensure environment variables are correctly set
4. Review Streamlit logs for detailed error messages
