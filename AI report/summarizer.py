import pdfplumber
from typing import List, Dict, Any
import os
from google import genai
from datetime import datetime
import json
import re

# -----------------------------
# Set up Gemini API client
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with your actual Gemini API key
os.environ["GOOGLE_GENAI_API_KEY"] = GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------
# PDF / TXT extraction functions
# -----------------------------

def extract_text_from_pdf(pdf_file) -> str:
    """
    Accepts a file path or file-like object for PDF extraction.
    """
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_txt(txt_file) -> str:
    """
    Accepts a file path or file-like object for TXT extraction.
    """
    if isinstance(txt_file, str):
        with open(txt_file, "r", encoding="utf-8") as file:
            return file.read()
    else:
        txt_file.seek(0)
        return txt_file.read().decode("utf-8")

# -----------------------------
# Text chunking
# -----------------------------
def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

# -----------------------------
# Audit-Specific Analysis Functions
# -----------------------------

def extract_financial_metrics(text: str) -> Dict[str, Any]:
    """Extract key financial metrics from audit text"""
    metrics = {
        "revenue": [],
        "expenses": [],
        "assets": [],
        "liabilities": [],
        "ratios": [],
        "percentages": []
    }
    
    # Common patterns for financial figures
    money_pattern = r'\$[\d,]+\.?\d*'
    percentage_pattern = r'\d+\.?\d*%'
    ratio_pattern = r'\d+\.?\d*:\d+\.?\d*'
    
    # Extract monetary values
    money_matches = re.findall(money_pattern, text)
    metrics["financial_figures"] = money_matches[:10]  # Limit to top 10
    
    # Extract percentages
    percentage_matches = re.findall(percentage_pattern, text)
    metrics["percentages"] = percentage_matches[:10]
    
    # Extract ratios
    ratio_matches = re.findall(ratio_pattern, text)
    metrics["ratios"] = ratio_matches[:5]
    
    return metrics

def analyze_audit_findings(text: str) -> Dict[str, Any]:
    """Analyze audit findings using AI"""
    prompt = f"""
    Analyze this audit text and extract key information in the following categories:
    
    1. AUDIT FINDINGS (significant issues, deficiencies, non-compliance)
    2. RECOMMENDATIONS (suggested improvements, corrective actions)
    3. RISK LEVEL (High/Medium/Low for each finding)
    4. COMPLIANCE STATUS (areas of compliance and non-compliance)
    5. MANAGEMENT RESPONSE (if any)
    
    Format the response as structured text with clear sections.
    
    Text to analyze:
    {text[:3000]}  # Limit text to avoid token limits
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return {"analysis": response.text.strip()}
    except Exception as e:
        return {"analysis": f"Error in AI analysis: {str(e)}"}

def generate_compliance_checklist(text: str) -> Dict[str, Any]:
    """Generate compliance checklist based on audit content"""
    prompt = f"""
    Based on this audit text, create a compliance checklist with the following format:
    
    COMPLIANCE AREAS REVIEWED:
    ✓ [Compliant areas]
    ✗ [Non-compliant areas]
    ? [Areas needing further review]
    
    REGULATORY STANDARDS MENTIONED:
    - List any standards, regulations, or frameworks mentioned
    
    ACTION ITEMS:
    1. Immediate actions required
    2. Short-term improvements
    3. Long-term strategic changes
    
    Text: {text[:2000]}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return {"checklist": response.text.strip()}
    except Exception as e:
        return {"checklist": f"Error generating checklist: {str(e)}"}

def categorize_risk_levels(findings_text: str) -> Dict[str, List[str]]:
    """Categorize findings by risk level"""
    prompt = f"""
    Categorize the following audit findings by risk level:
    
    HIGH RISK: Critical issues requiring immediate attention
    MEDIUM RISK: Significant issues requiring timely resolution
    LOW RISK: Minor issues or recommendations for improvement
    
    For each finding, provide a brief description and assign a risk level.
    
    Findings: {findings_text[:2000]}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return {"risk_categorization": response.text.strip()}
    except Exception as e:
        return {"risk_categorization": f"Error in risk categorization: {str(e)}"}

# -----------------------------
# Enhanced Summarization Functions
# -----------------------------

def summarize_chunk_gemini(chunk: str, style: str = "concise", audit_focus: bool = False) -> str:
    """
    Summarize a chunk of text using Gemini AI API with optional audit focus.
    """
    if audit_focus:
        prompt = f"""
        Summarize this audit text in {style} style, focusing on:
        - Key audit findings and observations
        - Financial figures and metrics
        - Compliance issues
        - Risk factors
        - Recommendations
        
        Text: {chunk}
        """
    else:
        prompt = f"Summarize the following text in a {style} style:\n\n{chunk}"
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text.strip()

def generate_audit_executive_summary(text: str, financial_metrics: Dict, findings: Dict) -> str:
    """Generate executive summary specifically for audit reports"""
    prompt = f"""
    Create an executive summary for this audit report including:
    
    1. AUDIT OVERVIEW (scope, period, methodology)
    2. KEY FINDINGS (most critical issues)
    3. FINANCIAL HIGHLIGHTS (key figures and trends)
    4. RISK ASSESSMENT (overall risk rating)
    5. RECOMMENDATIONS SUMMARY (top priority actions)
    6. CONCLUSION (overall audit opinion)
    
    Make it suitable for senior management and board members.
    Limit to 300-400 words.
    
    Audit text: {text[:3000]}
    Financial metrics: {str(financial_metrics)}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating executive summary: {str(e)}"

# -----------------------------
# Aggregate summaries
# -----------------------------
def aggregate_summaries(summaries: List[str]) -> str:
    return "\n\n".join(summaries)

# -----------------------------
# Enhanced Download Formatting Functions
# -----------------------------

def format_audit_report_comprehensive(filename: str, original_text: str, final_summary: str, 
                                    financial_metrics: Dict, audit_analysis: Dict, 
                                    compliance_checklist: Dict, chunk_summaries: List[str] = None) -> str:
    """
    Format comprehensive audit report with all analysis.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""
COMPREHENSIVE AUDIT ANALYSIS REPORT
{'='*60}
Original File: {filename}
Generated: {timestamp}
Analysis Type: AI-Powered Audit Summarization
{'='*60}

EXECUTIVE SUMMARY
{'-'*20}
{final_summary}

FINANCIAL METRICS EXTRACTED
{'-'*30}
Key Financial Figures: {', '.join(financial_metrics.get('financial_figures', [])[:5])}
Percentages Found: {', '.join(financial_metrics.get('percentages', [])[:5])}
Ratios Identified: {', '.join(financial_metrics.get('ratios', []))}

DETAILED AUDIT ANALYSIS
{'-'*25}
{audit_analysis.get('analysis', 'No analysis available')}

COMPLIANCE CHECKLIST
{'-'*20}
{compliance_checklist.get('checklist', 'No checklist generated')}

AUDIT TRAIL DOCUMENTATION
{'-'*30}
Document Processing Timestamp: {timestamp}
AI Model Used: Gemini-2.5-Flash
Analysis Method: Chunk-based processing with audit-specific prompts
Total Chunks Processed: {len(chunk_summaries) if chunk_summaries else 0}
Original Document Size: {len(original_text)} characters
Summary Compression Ratio: {len(final_summary)/len(original_text)*100:.1f}%

"""
    
    if chunk_summaries:
        content += f"\nDETAILED CHUNK ANALYSIS\n{'-'*25}\n"
        for i, chunk_summary in enumerate(chunk_summaries, 1):
            content += f"\nSection {i} Analysis:\n{chunk_summary}\n"
    
    content += f"\n{'='*60}\nReport generated by AI-Powered Audit Summarizer\n{'='*60}"
    
    return content

def format_audit_json_report(filename: str, original_text: str, final_summary: str,
                           financial_metrics: Dict, audit_analysis: Dict,
                           compliance_checklist: Dict, chunk_summaries: List[str] = None) -> str:
    """
    Format audit report as structured JSON.
    """
    timestamp = datetime.now().isoformat()
    
    data = {
        "audit_report_metadata": {
            "original_file": filename,
            "generated_timestamp": timestamp,
            "ai_model": "Gemini-2.5-Flash",
            "processing_method": "audit-focused-analysis",
            "document_stats": {
                "original_length": len(original_text),
                "summary_length": len(final_summary),
                "compression_ratio": f"{len(final_summary)/len(original_text)*100:.1f}%",
                "chunks_processed": len(chunk_summaries) if chunk_summaries else 0
            }
        },
        "executive_summary": final_summary,
        "financial_analysis": financial_metrics,
        "audit_findings": audit_analysis,
        "compliance_assessment": compliance_checklist,
        "detailed_analysis": {
            "chunk_summaries": chunk_summaries or [],
            "processing_notes": "Each chunk analyzed with audit-specific AI prompts"
        },
        "audit_trail": {
            "processing_timestamp": timestamp,
            "validation_status": "AI-generated, requires human review",
            "confidence_level": "Medium - AI analysis should be verified by qualified auditor"
        }
    }
    
    return json.dumps(data, indent=2, ensure_ascii=False)

def format_audit_markdown_report(filename: str, original_text: str, final_summary: str,
                                financial_metrics: Dict, audit_analysis: Dict,
                                compliance_checklist: Dict, chunk_summaries: List[str] = None) -> str:
    """
    Format audit report as professional Markdown.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# 🔍 Comprehensive Audit Analysis Report

## 📋 Report Information
- **Original File:** {filename}
- **Generated:** {timestamp}
- **Analysis Method:** AI-Powered Audit Summarization
- **Processing Model:** Gemini-2.5-Flash

---

## 📊 Executive Summary

{final_summary}

---

## 💰 Financial Metrics Analysis

### Key Financial Figures
{', '.join(financial_metrics.get('financial_figures', ['None identified'])[:8])}

### Percentages & Ratios
- **Percentages:** {', '.join(financial_metrics.get('percentages', ['None'])[:5])}
- **Ratios:** {', '.join(financial_metrics.get('ratios', ['None'])[:3])}

---

## 🎯 Detailed Audit Analysis

{audit_analysis.get('analysis', '*No detailed analysis available*')}

---

## ✅ Compliance Assessment

{compliance_checklist.get('checklist', '*No compliance checklist generated*')}

---

## 📈 Document Statistics

| Metric | Value |
|--------|--------|
| Original Length | {len(original_text):,} characters |
| Summary Length | {len(final_summary):,} characters |
| Compression Ratio | {len(final_summary)/len(original_text)*100:.1f}% |
| Sections Analyzed | {len(chunk_summaries) if chunk_summaries else 0} |

---

## 🔗 Audit Trail

- **Processing Timestamp:** {timestamp}
- **AI Model:** Gemini-2.5-Flash
- **Validation Status:** ⚠️ AI-generated content requires human review
- **Confidence Level:** Medium - Should be verified by qualified auditor

"""

    if chunk_summaries:
        content += f"\n---\n\n## 📑 Detailed Section Analysis\n\n"
        for i, chunk_summary in enumerate(chunk_summaries, 1):
            content += f"### Section {i}\n\n{chunk_summary}\n\n"

    content += f"\n---\n\n*Report generated by AI-Powered Audit Summarizer v2.0*\n"
    
    return content

# Legacy formatting functions (for backward compatibility)
def format_summary_as_text(filename: str, final_summary: str, chunk_summaries: List[str] = None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"AI REPORT SUMMARY\n{'='*50}\nOriginal File: {filename}\nGenerated: {timestamp}\n{'='*50}\n\nFINAL SUMMARY\n{'-'*20}\n{final_summary}\n\n"
    if chunk_summaries:
        content += f"DETAILED CHUNK SUMMARIES\n{'-'*30}\n"
        for i, chunk_summary in enumerate(chunk_summaries, 1):
            content += f"Chunk {i}:\n{chunk_summary}\n\n"
    return content

def format_summary_as_json(filename: str, final_summary: str, chunk_summaries: List[str] = None) -> str:
    timestamp = datetime.now().isoformat()
    data = {
        "metadata": {"original_file": filename, "generated_timestamp": timestamp, "total_chunks": len(chunk_summaries) if chunk_summaries else 0},
        "final_summary": final_summary, "chunk_summaries": chunk_summaries or []
    }
    return json.dumps(data, indent=2, ensure_ascii=False)

def format_summary_as_markdown(filename: str, final_summary: str, chunk_summaries: List[str] = None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"# AI Report Summary\n\n**Original File:** {filename}  \n**Generated:** {timestamp}  \n\n---\n\n## Final Summary\n\n{final_summary}\n\n"
    if chunk_summaries:
        content += f"## Detailed Chunk Summaries\n\n"
        for i, chunk_summary in enumerate(chunk_summaries, 1):
            content += f"### Chunk {i}\n\n{chunk_summary}\n\n"

    return content
