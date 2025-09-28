# app.py - Enhanced Audit-Focused Version
import streamlit as st
from summarizer import (
    extract_text_from_pdf, 
    extract_text_from_txt, 
    chunk_text, 
    summarize_chunk_gemini, 
    aggregate_summaries,
    extract_financial_metrics,
    analyze_audit_findings,
    generate_compliance_checklist,
    categorize_risk_levels,
    generate_audit_executive_summary,
    format_audit_report_comprehensive,
    format_audit_json_report,
    format_audit_markdown_report,
    # Legacy functions for backward compatibility
    format_summary_as_text,
    format_summary_as_json,
    format_summary_as_markdown
)
import tempfile
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI-Powered Audit Report Summarizer", 
    layout="wide",
    page_icon="🔍"
)

# Enhanced title with audit focus
st.title("🔍 AI-Powered Audit Report Summarizer")
st.markdown("*Specialized for Financial Audits, Compliance Reviews & Risk Assessment*")

# Add custom CSS for animated help button (keeping the existing CSS)
st.markdown("""
<style>
.help-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.help-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    color: white;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.help-button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.help-button:active {
    transform: translateY(-1px) scale(1.02);
}

.help-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.help-button:hover::before {
    left: 100%;
}

.help-panel {
    position: fixed;
    top: 90px;
    right: 20px;
    width: 350px;
    max-height: 80vh;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    z-index: 999;
    transform: translateX(380px) scale(0.8);
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    overflow-y: auto;
}

.help-panel.show {
    transform: translateX(0) scale(1);
    opacity: 1;
}

.help-panel h3 {
    color: #333;
    margin: 0 0 20px 0;
    font-size: 22px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.help-section {
    margin-bottom: 20px;
}

.help-section h4 {
    color: #444;
    margin: 0 0 10px 0;
    font-size: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
}

.help-section h4::before {
    content: '';
    width: 4px;
    height: 14px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    margin-right: 8px;
    border-radius: 2px;
}

.help-steps {
    list-style: none;
    padding: 0;
    margin: 0;
}

.help-steps li {
    background: rgba(102, 126, 234, 0.1);
    margin: 6px 0;
    padding: 10px 14px;
    border-radius: 10px;
    border-left: 3px solid #667eea;
    font-size: 13px;
    color: #333;
    transition: all 0.2s ease;
}

.help-steps li:hover {
    background: rgba(102, 126, 234, 0.15);
    transform: translateX(3px);
}

.help-bullets {
    list-style: none;
    padding: 0;
    margin: 0;
}

.help-bullets li {
    background: rgba(118, 75, 162, 0.1);
    margin: 5px 0;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: #444;
    position: relative;
    padding-left: 28px;
}

.help-bullets li::before {
    content: '•';
    position: absolute;
    left: 12px;
    color: #764ba2;
    font-weight: bold;
    font-size: 14px;
}

.close-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    font-size: 18px;
    color: #999;
    cursor: pointer;
    transition: color 0.2s ease;
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.close-btn:hover {
    color: #666;
    background: rgba(0,0,0,0.1);
}

.audit-feature {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
    border: 1px solid #c8e6c9;
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
}

.audit-feature h5 {
    color: #2e7d32;
    margin: 0 0 8px 0;
    font-size: 14px;
    font-weight: 600;
}

.audit-feature p {
    color: #1b5e20;
    margin: 0;
    font-size: 12px;
    line-height: 1.4;
}
</style>

<div class="help-container">
    <button class="help-button" onclick="toggleHelp()">?</button>
    <div class="help-panel" id="helpPanel">
        <button class="close-btn" onclick="toggleHelp()">×</button>
        <h3>🔍 Audit Summarizer Guide</h3>
        
        <div class="help-section">
            <h4>Quick Start:</h4>
            <ol class="help-steps">
                <li>Upload your audit report (PDF/TXT)</li>
                <li>Choose analysis type & style</li>
                <li>Enable audit-specific features</li>
                <li>Generate comprehensive summary</li>
                <li>Download professional report</li>
            </ol>
        </div>
        
        <div class="help-section">
            <h4>Audit Features:</h4>
            <div class="audit-feature">
                <h5>🎯 Financial Analysis</h5>
                <p>Extracts key figures, ratios, and percentages automatically</p>
            </div>
            <div class="audit-feature">
                <h5>⚠️ Risk Assessment</h5>
                <p>Categorizes findings by risk level (High/Medium/Low)</p>
            </div>
            <div class="audit-feature">
                <h5>✅ Compliance Check</h5>
                <p>Generates compliance checklists and action items</p>
            </div>
            <div class="audit-feature">
                <h5>📋 Audit Findings</h5>
                <p>Identifies key findings, recommendations, and management responses</p>
            </div>
        </div>
        
        <div class="help-section">
            <h4>Summary Styles:</h4>
            <ul class="help-bullets">
                <li><strong>Executive:</strong> Board-ready summary</li>
                <li><strong>Detailed:</strong> Comprehensive analysis</li>
                <li><strong>Audit-Focused:</strong> Professional audit format</li>
                <li><strong>Compliance:</strong> Regulatory focus</li>
            </ul>
        </div>
        
        <div class="help-section">
            <h4>Export Formats:</h4>
            <ul class="help-bullets">
                <li><strong>Comprehensive:</strong> Full audit analysis</li>
                <li><strong>JSON:</strong> Structured data with metadata</li>
                <li><strong>Executive:</strong> Management presentation</li>
            </ul>
        </div>
    </div>
</div>

<script>
let helpVisible = false;

function toggleHelp() {
    const panel = document.getElementById('helpPanel');
    helpVisible = !helpVisible;
    
    if (helpVisible) {
        panel.classList.add('show');
    } else {
        panel.classList.remove('show');
    }
}

document.addEventListener('click', function(event) {
    const helpContainer = document.querySelector('.help-container');
    const helpPanel = document.getElementById('helpPanel');
    
    if (!helpContainer.contains(event.target) && helpVisible) {
        helpPanel.classList.remove('show');
        helpVisible = false;
    }
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && helpVisible) {
        document.getElementById('helpPanel').classList.remove('show');
        helpVisible = false;
    }
});
</script>
""", unsafe_allow_html=True)

# Main interface
uploaded_file = st.file_uploader(
    "📄 Upload your audit report (PDF or TXT)", 
    type=["pdf", "txt"],
    help="Supports financial audit reports, compliance reviews, internal audit reports, and risk assessments"
)

if uploaded_file is not None:
    file_type = uploaded_file.type
    st.success(f"✅ File uploaded: **{uploaded_file.name}**")
    
    # Enhanced options with audit focus
    col1, col2, col3 = st.columns(3)
    
    with col1:
        summary_style = st.selectbox(
            "📊 Summary Style:",
            ["audit-focused", "executive", "detailed", "compliance-focused", "concise", "bullet-points"],
            help="Choose the most appropriate style for your audience"
        )
    
    with col2:
        analysis_type = st.selectbox(
            "🔍 Analysis Type:",
            ["comprehensive-audit", "basic-summary", "financial-focus", "compliance-review"],
            help="Comprehensive audit provides full analysis with financial metrics and risk assessment"
        )
    
    with col3:
        download_format = st.selectbox(
            "📥 Export Format:",
            ["comprehensive", "json", "markdown", "executive-summary"],
            help="Comprehensive format includes all audit-specific analysis"
        )
    
    # Audit-specific options
    st.markdown("### 🎯 Audit-Specific Features")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        enable_financial_analysis = st.checkbox(
            "💰 Financial Metrics", 
            value=True if analysis_type == "comprehensive-audit" else False,
            help="Extract financial figures, ratios, and percentages"
        )
    
    with col2:
        enable_risk_assessment = st.checkbox(
            "⚠️ Risk Categorization", 
            value=True if analysis_type == "comprehensive-audit" else False,
            help="Categorize findings by risk level"
        )
    
    with col3:
        enable_compliance_check = st.checkbox(
            "✅ Compliance Checklist", 
            value=True if analysis_type == "comprehensive-audit" else False,
            help="Generate compliance assessment and action items"
        )
    
    with col4:
        enable_audit_trail = st.checkbox(
            "📋 Audit Trail", 
            value=True if analysis_type == "comprehensive-audit" else False,
            help="Document processing methodology and validation notes"
        )
    
    # Process button with enhanced styling
    process_btn = st.button(
        "🚀 Generate Comprehensive Audit Summary", 
        type="primary",
        help="Process your audit report with AI-powered analysis"
    )

    if process_btn:
        with st.spinner("🔄 Processing audit report and generating comprehensive analysis..."):
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf" if file_type == "application/pdf" else ".txt") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Extract text
            if file_type == "application/pdf":
                text = extract_text_from_pdf(tmp_path)
            elif file_type == "text/plain":
                text = extract_text_from_txt(tmp_path)
            else:
                st.error("❌ Unsupported file type!")
                text = None

            os.unlink(tmp_path)

            if text:
                # Initialize analysis containers
                financial_metrics = {}
                audit_analysis = {}
                compliance_checklist = {}
                risk_categorization = {}
                
                # Display original text in expandable section
                with st.expander("📄 Original Document Text", expanded=False):
                    st.text_area("Extracted text from your audit report:", text, height=300)

                # Progress tracking
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                # Step 1: Financial Analysis (if enabled)
                if enable_financial_analysis:
                    status_text.text("💰 Analyzing financial metrics...")
                    financial_metrics = extract_financial_metrics(text)
                    progress_bar.progress(0.2)

                # Step 2: Text chunking and summarization
                status_text.text("📝 Processing document chunks...")
                chunks = chunk_text(text)
                summaries = []
                
                chunk_progress_start = 0.2 if enable_financial_analysis else 0.0
                chunk_progress_range = 0.4
                
                for i, chunk in enumerate(chunks):
                    chunk_progress = chunk_progress_start + (chunk_progress_range * (i + 1) / len(chunks))
                    status_text.text(f"📝 Processing chunk {i+1} of {len(chunks)}...")
                    
                    # Use audit-focused summarization if analysis type is audit-related
                    audit_focus = analysis_type in ["comprehensive-audit", "financial-focus", "compliance-review"]
                    summary_chunk = summarize_chunk_gemini(chunk, style=summary_style, audit_focus=audit_focus)
                    summaries.append(summary_chunk)
                    progress_bar.progress(min(chunk_progress, 1.0))

                # Step 3: Audit-specific analysis (if enabled)
                if enable_risk_assessment or analysis_type == "comprehensive-audit":
                    status_text.text("⚠️ Performing risk assessment...")
                    audit_analysis = analyze_audit_findings(text)
                    if enable_risk_assessment:
                        risk_categorization = categorize_risk_levels(audit_analysis.get('analysis', ''))
                    progress_bar.progress(0.7)

                if enable_compliance_check or analysis_type == "compliance-review":
                    status_text.text("✅ Generating compliance checklist...")
                    compliance_checklist = generate_compliance_checklist(text)
                    progress_bar.progress(0.8)

                # Step 4: Generate final summary
                status_text.text("📊 Generating final summary...")
                if analysis_type == "comprehensive-audit" or summary_style == "executive":
                    final_summary = generate_audit_executive_summary(text, financial_metrics, audit_analysis)
                else:
                    final_summary = aggregate_summaries(summaries)
                progress_bar.progress(0.9)

                # Clear progress indicators
                status_text.empty()
                progress_bar.progress(1.0)
                st.success("✅ Analysis completed successfully!")
                
                # Display results in organized tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Executive Summary", 
                    "💰 Financial Analysis", 
                    "🎯 Audit Findings", 
                    "✅ Compliance", 
                    "📑 Detailed Chunks"
                ])

                with tab1:
                    st.subheader("📊 Executive Summary")
                    st.text_area("Final Summary:", final_summary, height=400, key="final_summary")
                    
                    # Key metrics display
                    if financial_metrics:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Financial Figures Found", len(financial_metrics.get('financial_figures', [])))
                        with col2:
                            st.metric("Percentages Extracted", len(financial_metrics.get('percentages', [])))
                        with col3:
                            st.metric("Document Sections", len(chunks))

                with tab2:
                    st.subheader("💰 Financial Analysis")
                    if financial_metrics and enable_financial_analysis:
                        if financial_metrics.get('financial_figures'):
                            st.write("**💵 Key Financial Figures:**")
                            for fig in financial_metrics['financial_figures'][:10]:
                                st.write(f"• {fig}")
                        
                        if financial_metrics.get('percentages'):
                            st.write("**📊 Percentages Found:**")
                            for pct in financial_metrics['percentages'][:10]:
                                st.write(f"• {pct}")
                        
                        if financial_metrics.get('ratios'):
                            st.write("**⚖️ Ratios Identified:**")
                            for ratio in financial_metrics['ratios'][:5]:
                                st.write(f"• {ratio}")
                    else:
                        st.info("💡 Enable Financial Metrics analysis to see detailed financial data extraction")

                with tab3:
                    st.subheader("🎯 Audit Findings & Risk Assessment")
                    if audit_analysis and enable_risk_assessment:
                        st.text_area("Audit Analysis:", audit_analysis.get('analysis', 'No analysis performed'), height=300)
                        
                        if risk_categorization:
                            st.subheader("⚠️ Risk Categorization")
                            st.text_area("Risk Assessment:", risk_categorization.get('risk_categorization', ''), height=200)
                    else:
                        st.info("💡 Enable Risk Categorization to see detailed audit findings analysis")

                with tab4:
                    st.subheader("✅ Compliance Assessment")
                    if compliance_checklist and enable_compliance_check:
                        st.text_area("Compliance Checklist:", compliance_checklist.get('checklist', 'No checklist generated'), height=350)
                    else:
                        st.info("💡 Enable Compliance Checklist to see regulatory compliance assessment")

                with tab5:
                    st.subheader("📑 Detailed Section Analysis")
                    if summaries:
                        for i, summary in enumerate(summaries):
                            with st.expander(f"Section {i+1} Summary", expanded=False):
                                st.text_area(f"Analysis of section {i+1}:", summary, height=200, key=f"chunk_{i}")
                    else:
                        st.info("No chunk summaries available")

                # Enhanced Download Section
                st.markdown("---")
                st.subheader("📥 Download Professional Reports")
                
                # Generate download content based on format
                base_filename = uploaded_file.name.rsplit('.', 1)[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if download_format == "comprehensive":
                    download_content = format_audit_report_comprehensive(
                        uploaded_file.name, text, final_summary, financial_metrics, 
                        audit_analysis, compliance_checklist, summaries
                    )
                    download_filename = f"{base_filename}_comprehensive_audit_report_{timestamp}.txt"
                    mime_type = "text/plain"
                    
                elif download_format == "json":
                    download_content = format_audit_json_report(
                        uploaded_file.name, text, final_summary, financial_metrics,
                        audit_analysis, compliance_checklist, summaries
                    )
                    download_filename = f"{base_filename}_audit_analysis_{timestamp}.json"
                    mime_type = "application/json"
                    
                elif download_format == "markdown":
                    download_content = format_audit_markdown_report(
                        uploaded_file.name, text, final_summary, financial_metrics,
                        audit_analysis, compliance_checklist, summaries
                    )
                    download_filename = f"{base_filename}_audit_report_{timestamp}.md"
                    mime_type = "text/markdown"
                    
                elif download_format == "executive-summary":
                    download_content = f"""
EXECUTIVE AUDIT SUMMARY
{uploaded_file.name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{final_summary}

Key Statistics:
- Document Length: {len(text):,} characters
- Summary Length: {len(final_summary):,} characters  
- Compression Ratio: {len(final_summary)/len(text)*100:.1f}%
- Sections Analyzed: {len(summaries)}
"""
                    download_filename = f"{base_filename}_executive_summary_{timestamp}.txt"
                    mime_type = "text/plain"

                # Download buttons with enhanced layout
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.download_button(
                        label=f"📊 Download {download_format.title()}",
                        data=download_content,
                        file_name=download_filename,
                        mime=mime_type,
                        type="primary",
                        help=f"Download complete {download_format} analysis report"
                    )
                
                with col2:
                    # Executive summary only
                    executive_filename = f"{base_filename}_executive_only_{timestamp}.txt"
                    st.download_button(
                        label="👔 Executive Summary",
                        data=final_summary,
                        file_name=executive_filename,
                        mime="text/plain",
                        help="Download only the executive summary"
                    )
                
                with col3:
                    # Financial metrics only (if available)
                    if financial_metrics and enable_financial_analysis:
                        financial_content = f"""
FINANCIAL METRICS REPORT
{uploaded_file.name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Financial Figures: {', '.join(financial_metrics.get('financial_figures', []))}
Percentages: {', '.join(financial_metrics.get('percentages', []))}
Ratios: {', '.join(financial_metrics.get('ratios', []))}
"""
                        financial_filename = f"{base_filename}_financial_metrics_{timestamp}.txt"
                        st.download_button(
                            label="💰 Financial Report",
                            data=financial_content,
                            file_name=financial_filename,
                            mime="text/plain",
                            help="Download financial metrics analysis only"
                        )
                    else:
                        st.info("💡 Enable Financial Analysis")

                with col4:
                    # Compliance report (if available)
                    if compliance_checklist and enable_compliance_check:
                        compliance_content = f"""
COMPLIANCE ASSESSMENT REPORT
{uploaded_file.name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{compliance_checklist.get('checklist', 'No compliance assessment available')}
"""
                        compliance_filename = f"{base_filename}_compliance_report_{timestamp}.txt"
                        st.download_button(
                            label="✅ Compliance Report",
                            data=compliance_content,
                            file_name=compliance_filename,
                            mime="text/plain",
                            help="Download compliance assessment only"
                        )
                    else:
                        st.info("💡 Enable Compliance Check")

                # Advanced options
                with st.expander("🔧 Advanced Export Options", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📋 Generate All Formats"):
                            st.info("Generating preview of all available formats...")
                            
                            # Show format previews
                            format_tabs = st.tabs(["📊 Comprehensive", "💾 JSON", "📝 Markdown"])
                            
                            with format_tabs[0]:
                                comprehensive_preview = format_audit_report_comprehensive(
                                    uploaded_file.name, text[:1000] + "...", final_summary[:500] + "...", 
                                    financial_metrics, audit_analysis, compliance_checklist, summaries[:2]
                                )
                                st.text_area("Comprehensive Report Preview:", comprehensive_preview[:2000] + "...", height=300)
                            
                            with format_tabs[1]:
                                json_preview = format_audit_json_report(
                                    uploaded_file.name, text[:500], final_summary[:300], 
                                    financial_metrics, audit_analysis, compliance_checklist, summaries[:2]
                                )
                                st.code(json_preview[:2000] + "...", language="json")
                            
                            with format_tabs[2]:
                                md_preview = format_audit_markdown_report(
                                    uploaded_file.name, text[:500], final_summary[:300],
                                    financial_metrics, audit_analysis, compliance_checklist, summaries[:2]
                                )
                                st.markdown("**Markdown Preview:**")
                                st.markdown(md_preview[:2000] + "...")
                    
                    with col2:
                        # Audit trail documentation
                        if enable_audit_trail:
                            st.markdown("**🔍 Audit Trail Information:**")
                            st.json({
                                "processing_timestamp": datetime.now().isoformat(),
                                "ai_model": "Gemini-2.5-Flash",
                                "analysis_type": analysis_type,
                                "features_enabled": {
                                    "financial_analysis": enable_financial_analysis,
                                    "risk_assessment": enable_risk_assessment,
                                    "compliance_check": enable_compliance_check,
                                    "audit_trail": enable_audit_trail
                                },
                                "document_stats": {
                                    "original_length": len(text),
                                    "chunks_processed": len(chunks),
                                    "summary_length": len(final_summary)
                                }
                            })

                # Enhanced sidebar statistics
                st.sidebar.markdown("### 📊 Analysis Statistics")
                st.sidebar.metric("📄 Original Length", f"{len(text):,} chars")
                st.sidebar.metric("📝 Summary Length", f"{len(final_summary):,} chars")
                st.sidebar.metric("📊 Compression Ratio", f"{len(final_summary)/len(text)*100:.1f}%")
                st.sidebar.metric("🧩 Sections Processed", len(chunks))
                
                if financial_metrics:
                    st.sidebar.metric("💰 Financial Figures", len(financial_metrics.get('financial_figures', [])))
                
                # Processing summary
                st.sidebar.markdown("### ⚙️ Processing Summary")
                processing_info = {
                    "AI Model": "Gemini-2.5-Flash",
                    "Analysis Type": analysis_type,
                    "Summary Style": summary_style,
                    "Features Used": f"{sum([enable_financial_analysis, enable_risk_assessment, enable_compliance_check, enable_audit_trail])}/4"
                }
                
                for key, value in processing_info.items():
                    st.sidebar.text(f"{key}: {value}")
                
            else:
                st.error("❌ No text could be extracted from the file. Please ensure your document contains readable text.")

# Footer
st.markdown("---")
st.markdown("*🔍 AI-Powered Audit Report Summarizer - Specialized for professional audit analysis and compliance review*")