import streamlit as st
import PyPDF2
import io
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
import re

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Tax Notice Analyzer & Response Drafter",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

class TaxNoticeAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.llm = None
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=self.api_key,
                temperature=0.3
            )
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from PDF: {e}")
            return None
    
    def analyze_notice(self, notice_text):
        """Analyze the tax notice and extract key information"""
        if not self.llm:
            return None, "API key not configured"
        
        analysis_prompt = PromptTemplate(
            input_variables=["notice_text"],
            template="""
You are a tax expert. Analyze the following tax notice and provide a comprehensive summary.

Tax Notice Content:
{notice_text}

Please provide the analysis in the following format:

**NOTICE TYPE:** [Type of notice - Assessment, Demand, Show Cause, etc.]

**KEY DETAILS:**
- Notice Number: [Extract notice number if available]
- Date of Notice: [Extract date]
- Due Date: [Extract due date for response]
- Taxpayer Details: [Name, PAN if mentioned]
- Assessment Year: [Extract assessment year]
- Tax Type: [Income Tax, GST, etc.]
- Section/Provision: [Legal section under which notice is issued]
- Issuing Authority: [Department/Officer name]

**FINANCIAL IMPLICATIONS:**
- Amount Demanded: [Any tax amount mentioned]
- Interest/Penalty: [Any additional charges]
- Total Liability: [Total amount if calculable]

**MAIN ISSUES:**
- [List the primary concerns/issues raised in the notice]
- [Any discrepancies mentioned]
- [Specific queries or demands]

**REQUIRED ACTIONS:**
- [What the taxpayer needs to do]
- [Documents to be submitted]
- [Deadlines to be met]

**URGENCY LEVEL:** [High/Medium/Low based on consequences mentioned]

**SUMMARY:**
[Provide a clear, concise summary of what this notice is about and what it means for the taxpayer]
            """
        )
        
        try:
            prompt = analysis_prompt.format(notice_text=notice_text)
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content, None
        except Exception as e:
            return None, str(e)
    
    def draft_response(self, notice_text, response_type="compliance"):
        """Draft a response to the tax notice"""
        if not self.llm:
            return None, "API key not configured"
        
        response_prompt = PromptTemplate(
            input_variables=["notice_text", "response_type"],
            template="""
You are a tax consultant helping to draft a response to a tax notice. 

Tax Notice Content:
{notice_text}

Response Type: {response_type}

Please draft a professional response letter. The response should be:
1. Formal and respectful in tone
2. Address all points raised in the notice
3. Include proper legal references where applicable
4. Request extensions if needed
5. Provide a structured response

Format the response as follows:

**TO:** [Issuing Authority]
**FROM:** [Taxpayer Name]
**DATE:** [Current Date]
**SUBJECT:** Response to Notice [Notice Number] dated [Notice Date]

**Sir/Madam,**

[Draft the main response content here]

**1. ACKNOWLEDGMENT:**
[Acknowledge receipt of the notice]

**2. RESPONSE TO SPECIFIC POINTS:**
[Address each point raised in the notice]

**3. SUPPORTING DOCUMENTS:**
[List documents being submitted or to be submitted]

**4. REQUEST FOR CONSIDERATION:**
[Any specific requests - extensions, hearings, etc.]

**5. CONCLUSION:**
[Respectful conclusion requesting favorable consideration]

**Yours faithfully,**
**[Taxpayer Name]**
**[Date]**

**ENCLOSURES:**
- [List of documents attached]

---
**IMPORTANT NOTES FOR TAXPAYER:**
- [Any additional advice or reminders]
- [Critical deadlines to remember]
- [Recommended next steps]
            """
        )
        
        try:
            prompt = response_prompt.format(notice_text=notice_text, response_type=response_type)
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content, None
        except Exception as e:
            return None, str(e)
    
    def extract_key_dates(self, notice_text):
        """Extract important dates from the notice"""
        if not self.llm:
            return None, "API key not configured"
        
        dates_prompt = f"""
        From the following tax notice, extract all important dates and create a timeline:
        
        {notice_text}
        
        Please format as:
        - Notice Date: [date]
        - Due Date: [date]
        - Assessment Year: [year]
        - Any other important dates mentioned
        
        Also calculate days remaining until due date if possible.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=dates_prompt)])
            return response.content, None
        except Exception as e:
            return None, str(e)

def main():
    # Initialize analyzer
    analyzer = TaxNoticeAnalyzer()
    
    # Header
    st.markdown('<h1 class="main-header">📋 Tax Notice Analyzer & Response Drafter</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🛠️ Configuration")
    
    # API Key status
    if analyzer.api_key:
        st.sidebar.success("✅ Gemini API Key configured")
    else:
        st.sidebar.error("❌ Gemini API Key not found")
        st.sidebar.warning("Please set GEMINI_API_KEY in your environment variables")
    
    # Input options
    st.sidebar.subheader("📄 Input Options")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Upload PDF", "Paste Text"]
    )
    
    # Response type selection
    st.sidebar.subheader("📝 Response Type")
    response_type = st.sidebar.selectbox(
        "Select response approach:",
        [
            "compliance",
            "request_extension", 
            "dispute_assessment",
            "partial_agreement",
            "request_hearing"
        ]
    )
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Input Notice", "📊 Analysis", "✍️ Response Draft", "📅 Timeline"])
    
    with tab1:
        st.header("Tax Notice Input")
        
        notice_text = ""
        
        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader(
                "Upload Tax Notice PDF",
                type=['pdf'],
                help="Upload the PDF file of your tax notice"
            )
            
            if uploaded_file is not None:
                with st.spinner("Extracting text from PDF..."):
                    notice_text = analyzer.extract_text_from_pdf(uploaded_file)
                
                if notice_text:
                    st.success("✅ Text extracted successfully!")
                    
                    # Show extracted text
                    st.subheader("Extracted Text:")
                    st.text_area(
                        "Review and edit if needed:",
                        value=notice_text,
                        height=400,
                        key="extracted_text"
                    )
                    notice_text = st.session_state.extracted_text
                else:
                    st.error("Failed to extract text from PDF")
        
        else:  # Paste Text
            notice_text = st.text_area(
                "Paste the tax notice content here:",
                height=400,
                placeholder="Copy and paste the complete text of your tax notice here..."
            )
        
        # Store notice text in session state
        if notice_text:
            st.session_state.notice_text = notice_text
            st.success(f"✅ Notice loaded ({len(notice_text)} characters)")
    
    with tab2:
        st.header("📊 Notice Analysis")
        
        if 'notice_text' in st.session_state and analyzer.api_key:
            if st.button("🔍 Analyze Notice", type="primary"):
                with st.spinner("Analyzing tax notice..."):
                    analysis, error = analyzer.analyze_notice(st.session_state.notice_text)
                
                if error:
                    st.error(f"Error: {error}")
                elif analysis:
                    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                    st.markdown("### 📋 Detailed Analysis")
                    st.markdown(analysis)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Store analysis in session state
                    st.session_state.analysis = analysis
        
        elif 'notice_text' not in st.session_state:
            st.info("👆 Please input a tax notice in the 'Input Notice' tab first")
        elif not analyzer.api_key:
            st.error("❌ Gemini API key not configured. Please set GEMINI_API_KEY in your environment.")
    
    with tab3:
        st.header("✍️ Response Draft")
        
        if 'notice_text' in st.session_state and analyzer.api_key:
            
            # Response type info
            response_info = {
                "compliance": "Full compliance - agreeing with the notice",
                "request_extension": "Requesting time extension to respond",
                "dispute_assessment": "Disputing the assessment/demand",
                "partial_agreement": "Partially agreeing with some points",
                "request_hearing": "Requesting a personal hearing"
            }
            
            st.info(f"📝 Selected Response Type: **{response_type}** - {response_info[response_type]}")
            
            if st.button("✍️ Draft Response", type="primary"):
                with st.spinner("Drafting response letter..."):
                    response, error = analyzer.draft_response(st.session_state.notice_text, response_type)
                
                if error:
                    st.error(f"Error: {error}")
                elif response:
                    st.markdown("### 📝 Draft Response Letter")
                    
                    # Editable response
                    edited_response = st.text_area(
                        "Review and edit the draft response:",
                        value=response,
                        height=600,
                        key="draft_response"
                    )
                    
                    # Download button
                    if st.button("📥 Download Response as Text File"):
                        st.download_button(
                            label="📄 Download Response",
                            data=edited_response,
                            file_name=f"tax_notice_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
        
        elif 'notice_text' not in st.session_state:
            st.info("👆 Please input a tax notice in the 'Input Notice' tab first")
        elif not analyzer.api_key:
            st.error("❌ Gemini API key not configured. Please set GEMINI_API_KEY in your environment.")
    
    with tab4:
        st.header("📅 Important Dates & Timeline")
        
        if 'notice_text' in st.session_state and analyzer.api_key:
            if st.button("📅 Extract Timeline", type="primary"):
                with st.spinner("Extracting important dates..."):
                    timeline, error = analyzer.extract_key_dates(st.session_state.notice_text)
                
                if error:
                    st.error(f"Error: {error}")
                elif timeline:
                    st.markdown('<div class="info-box">', unsafe_allow_html=True)
                    st.markdown("### 📅 Important Dates & Deadlines")
                    st.markdown(timeline)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add calendar reminder
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    st.markdown("### ⚠️ Reminder")
                    st.markdown("**Don't forget to:**")
                    st.markdown("- Set calendar reminders for all due dates")
                    st.markdown("- Prepare and submit response before deadline")
                    st.markdown("- Keep copies of all submissions")
                    st.markdown("- Follow up on acknowledgments")
                    st.markdown('</div>', unsafe_allow_html=True)
        
        elif 'notice_text' not in st.session_state:
            st.info("👆 Please input a tax notice in the 'Input Notice' tab first")
        elif not analyzer.api_key:
            st.error("❌ Gemini API key not configured. Please set GEMINI_API_KEY in your environment.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Disclaimer:** This tool provides AI-generated analysis and draft responses for reference only. "
        "Please consult with a qualified tax professional before submitting any official responses."
    )

if __name__ == "__main__":
    main()
