import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from main_pipeline import ResumeScreener
import config.settings as settings

# Page configuration
st.set_page_config(
    page_title="ApexHire - AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Professional color palette */
    :root {
        --primary-blue: #1e40af;
        --primary-dark: #1e3a8a;
        --secondary-blue: #3b82f6;
        --accent-green: #059669;
        --accent-orange: #ea580c;
        --accent-red: #dc2626;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        --white: #ffffff;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, var(--gray-50) 0%, var(--white) 100%);
        padding: 2rem;
    }
    
    /* Professional header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--gray-900);
        text-align: center;
        margin-bottom: 3rem;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Professional cards */
    .metric-card {
        background: var(--white);
        border: 1px solid var(--gray-200);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        transition: all 0.2s ease;
        border-left: 4px solid var(--primary-blue);
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-1px);
    }
    
    /* Status boxes */
    .success-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--accent-green);
    }
    
    .info-box {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 1px solid #bfdbfe;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--primary-blue);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fde68a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--accent-orange);
    }
    
    .error-box {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1px solid #fecaca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--accent-red);
    }
    
    /* Professional typography */
    .help-text {
        font-size: 0.875rem;
        color: var(--gray-600);
        font-style: italic;
        padding: 0.75rem;
        background: var(--gray-50);
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }
    
    /* Step indicators */
    .step-number {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: var(--white);
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 12px;
        font-size: 0.875rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* Skill tags */
    .skill-tag {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: var(--white);
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.125rem;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .skill-tag.technical {
        background: linear-gradient(135deg, var(--accent-green), #10b981);
    }
    
    .skill-tag.soft {
        background: linear-gradient(135deg, var(--accent-orange), #f97316);
    }
    
    /* Score visualization */
    .score-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: conic-gradient(var(--accent-green) 0deg, var(--accent-green) calc(var(--score) * 360deg), var(--gray-200) calc(var(--score) * 360deg), var(--gray-200) 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem auto;
        box-shadow: var(--shadow-md);
        position: relative;
    }
    
    .score-circle::before {
        content: '';
        position: absolute;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: var(--white);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .score-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--gray-900);
        position: relative;
        z-index: 1;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: var(--white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-blue));
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--gray-900), var(--gray-800));
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed var(--gray-300);
        border-radius: 12px;
        background: var(--gray-50);
        padding: 2rem;
        transition: all 0.2s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-blue);
        background: var(--gray-100);
    }
    
    /* Data tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-green), var(--primary-blue));
        border-radius: 4px;
    }
    
    /* Metrics display */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
        text-align: center;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--gray-600);
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.025em;
        font-weight: 500;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--gray-900);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--gray-200);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: var(--gray-900);
        border-radius: 8px;
        border: 1px solid var(--gray-700);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: var(--shadow-sm);
    }
    
    /* Tabs */
    .stTabs > div > div > div {
        background: var(--white);
        border-radius: 8px 8px 0 0;
        border: 1px solid var(--gray-200);
        border-bottom: none;
    }
    
    .stTabs > div > div > div[data-baseweb="tab"] {
        background: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-bottom: none;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs > div > div > div[data-baseweb="tab"][aria-selected="true"] {
        background: var(--white);
        border-bottom: 2px solid var(--primary-blue);
    }
</style>
""", unsafe_allow_html=True)

def show_help_tooltip():
    """Show help tooltip for current section"""
    st.markdown("""
    <div class="info-box">
        <h4>💡 Need Help?</h4>
        <p>Check out our comprehensive <a href="docs/USER_GUIDE.md" target="_blank">User Guide</a> for detailed instructions!</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Professional header
    st.markdown('<h1 class="main-header">ApexHire AI Resume Screener</h1>', unsafe_allow_html=True)
    
    # Professional sidebar
    st.sidebar.markdown("""
    <div style="padding: 1rem; background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 12px; margin-bottom: 2rem;">
        <h3 style="color: white; margin: 0; font-weight: 600;">Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Select a page:",
        ["🏠 Home", "📄 Resume Analysis", "💼 Job Matching", "📊 Results", "⚙️ Settings", "❓ Help"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📄 Resume Analysis":
        show_resume_analysis()
    elif page == "💼 Job Matching":
        show_job_matching()
    elif page == "📊 Results":
        show_results()
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "❓ Help":
        show_help_page()

def show_home_page():
    """Display the professional home page"""
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); padding: 3rem; border-radius: 16px; margin-bottom: 3rem;">
        <h2 style="color: white; margin: 0 0 1rem 0; font-weight: 700;">AI-Powered Resume Screening</h2>
        <p style="color: white; font-size: 1.1rem; margin: 0; opacity: 0.9;">
            Advanced NLP technology for intelligent resume analysis and job matching. 
            Extract skills, analyze experience, and find the perfect candidate match.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown('<h3 class="section-header">Quick Start Guide</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="step-number">1</div>
                <h4 style="margin: 0; color: #1e40af;">Upload Resume</h4>
            </div>
            <p style="color: #6b7280; margin: 0;">Upload your resume file (PDF, DOCX, TXT) for comprehensive analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="step-number">3</div>
                <h4 style="margin: 0; color: #1e40af;">View Results</h4>
            </div>
            <p style="color: #6b7280; margin: 0;">Review detailed analysis, skills extraction, and match scores</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="step-number">2</div>
                <h4 style="margin: 0; color: #1e40af;">Add Job Description</h4>
            </div>
            <p style="color: #6b7280; margin: 0;">Enter or upload job requirements for intelligent matching</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div class="step-number">4</div>
                <h4 style="margin: 0; color: #1e40af;">Get Insights</h4>
            </div>
            <p style="color: #6b7280; margin: 0;">Analyze experience, education, and skill compatibility</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown('<h3 class="section-header">Key Features</h3>', unsafe_allow_html=True)
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">📄 Smart Resume Parsing</h4>
            <p style="color: #6b7280; margin: 0;">Advanced text extraction from PDF, DOCX, and TXT files with NLP processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">🧠 AI-Powered Analysis</h4>
            <p style="color: #6b7280; margin: 0;">Machine learning algorithms for skills extraction and semantic matching</p>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">📊 Comprehensive Insights</h4>
            <p style="color: #6b7280; margin: 0;">Detailed analysis of experience, education, skills, and contact information</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">🎯 Intelligent Matching</h4>
            <p style="color: #6b7280; margin: 0;">Advanced algorithms to rank candidates by relevance and compatibility</p>
        </div>
        """, unsafe_allow_html=True)
    
    # System statistics
    st.markdown('<h3 class="section-header">System Statistics</h3>', unsafe_allow_html=True)
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value">3</div>
            <div class="metric-label">Supported Formats</div>
            <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">PDF, DOCX, TXT</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value">&lt;30s</div>
            <div class="metric-label">Processing Speed</div>
            <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">per resume</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value">95%+</div>
            <div class="metric-label">Accuracy</div>
            <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">skill extraction</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col4:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div class="metric-value">1</div>
            <div class="metric-label">Languages</div>
            <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">English</div>
        </div>
        """, unsafe_allow_html=True)

def show_resume_analysis():
    st.markdown("## 📄 Resume Analysis")
    
    # Instructions
    st.markdown("""
    <div class="info-box">
        <h4>📋 Instructions</h4>
        <p><strong>Step 1:</strong> Upload your resume file (PDF, DOCX, or TXT)</p>
        <p><strong>Step 2:</strong> Click "Analyze Resume" to process the file</p>
        <p><strong>Step 3:</strong> Review the extracted skills and information</p>
        <p class="help-text">💡 Tip: Use clear, well-formatted resumes for best results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format (max 10MB)"
    )
    
    if uploaded_file is not None:
        # File info
        file_size = len(uploaded_file.getvalue()) / 1024 / 1024  # MB
        st.info(f"📁 File: {uploaded_file.name} ({file_size:.1f} MB)")
        
        # Save uploaded file
        file_path = Path(settings.RESUMES_DIR) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File uploaded successfully!")
        
        # Analyze button
        if st.button("🔍 Analyze Resume", type="primary", help="Click to start AI analysis"):
            with st.spinner("🤖 AI is analyzing your resume..."):
                try:
                    screener = ResumeScreener()
                    result = screener.analyze_resume(str(file_path))
                    
                    if result:
                        display_resume_analysis(result)
                    else:
                        st.error("❌ Failed to analyze resume. Please check file format and content.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.markdown("""
                    <div class="warning-box">
                        <h4>🔧 Troubleshooting</h4>
                        <p>• Ensure file is not corrupted</p>
                        <p>• Check file contains readable text</p>
                        <p>• Try with a different file format</p>
                        <p>• Maximum file size is 10MB</p>
                    </div>
                    """, unsafe_allow_html=True)

def display_resume_analysis(result):
    st.markdown("### 📊 Analysis Results")
    
    # Basic info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Basic Information")
        st.metric("Text Length", f"{result.get('text_length', 0):,} characters")
        st.metric("Words Count", f"{result.get('word_count', 0):,} words")
        st.metric("Processing Time", f"{result.get('processing_time', 0):.2f} seconds")
    
    with col2:
        st.markdown("#### 🎯 Skills Found")
        skills = result.get('skills', {})
        if skills:
            tech_skills = skills.get('technical_skills', [])
            soft_skills = skills.get('soft_skills', [])
            
            st.write("**🔧 Technical Skills:**")
            if tech_skills:
                for skill in tech_skills[:10]:  # Show first 10
                    st.write(f"• {skill}")
            else:
                st.write("No technical skills detected")
            
            st.write("**🤝 Soft Skills:**")
            if soft_skills:
                for skill in soft_skills[:5]:  # Show first 5
                    st.write(f"• {skill}")
            else:
                st.write("No soft skills detected")
    
    # Text preview
    with st.expander("📄 Text Preview"):
        raw_text = result.get('raw_text', '')
        if raw_text:
            st.text(raw_text[:500] + "..." if len(raw_text) > 500 else raw_text)
        else:
            st.write("No text preview available")

def show_job_matching():
    st.markdown("## 💼 Job Matching")
    
    # Instructions
    st.markdown("""
    <div class="info-box">
        <h4>📋 Instructions</h4>
        <p><strong>Step 1:</strong> Enter the job title and description</p>
        <p><strong>Step 2:</strong> Select a resume to match against the job</p>
        <p><strong>Step 3:</strong> Click "Match Resume to Job" to analyze</p>
        <p><strong>Step 4:</strong> Review the match score and recommendations</p>
        <p class="help-text">💡 Tip: Be specific in job descriptions for better matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Job description input
    job_title = st.text_input("Job Title", placeholder="e.g., Senior iOS Developer", help="Enter the position title")
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the complete job description here...\n\nExample:\nWe are looking for a Senior iOS Developer with:\n- 5+ years iOS development experience\n- Proficiency in Swift and Objective-C\n- Experience with UIKit and Core Data\n- Knowledge of RESTful APIs\n- Familiarity with Git and Agile methodologies",
        height=200,
        help="Include requirements, responsibilities, and qualifications"
    )
    
    # Resume selection
    resume_files = list(settings.RESUMES_DIR.glob("*"))
    if resume_files:
        selected_resume = st.selectbox(
            "Select a resume to match:",
            [f.name for f in resume_files if f.is_file()],
            help="Choose a previously uploaded resume"
        )
        
        if st.button("🎯 Match Resume to Job", type="primary", help="Start the matching analysis"):
            if job_description and selected_resume:
                with st.spinner("🤖 AI is matching resume to job..."):
                    try:
                        screener = ResumeScreener()
                        match_result = screener.match_resume_to_job(
                            resume_path=str(settings.RESUMES_DIR / selected_resume),
                            job_description=job_description
                        )
                        
                        if match_result:
                            display_job_match(match_result, job_title)
                        else:
                            st.error("❌ Failed to match resume to job. Please check inputs and try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please provide both job description and select a resume")
    else:
        st.info("ℹ️ No resume files found. Please upload resumes first in the Resume Analysis section.")

def display_job_match(result, job_title):
    """Display job matching results with ATS analysis"""
    st.markdown("### 🎯 ATS Job Match Analysis")
    
    # Overall score
    overall_score = result.get('overall_score', 0)
    st.markdown(f"#### ✅ ATS Match Score: {overall_score:.0f}/100")
    
    # ATS Analysis
    ats_analysis = result.get('ats_analysis', {})
    if ats_analysis:
        # Detailed matches
        detailed_matches = ats_analysis.get('detailed_matches', [])
        if detailed_matches:
            st.markdown("#### 📌 Matching Breakdown")
            
            # Create a table for matches
            match_data = []
            for match in detailed_matches:
                requirement = match.get('requirement', '')
                matched = match.get('matched', '')
                details = match.get('details', '')
                match_data.append([requirement, matched, details])
            
            if match_data:
                df = pd.DataFrame(match_data, columns=['Job Requirement', 'Matched?', 'Details'])
                st.dataframe(df, use_container_width=True)
        
        # Highlights
        highlights = ats_analysis.get('highlights', [])
        if highlights:
            st.markdown("#### ⭐ Highlights in Resume")
            for highlight in highlights:
                st.markdown(f"✅ {highlight}")
        
        # Gaps
        gaps = ats_analysis.get('gaps', [])
        if gaps:
            st.markdown("#### 📉 Areas to Improve")
            for gap in gaps:
                st.markdown(f"⚠️ {gap}")
        
        # Recommendations
        recommendations = ats_analysis.get('recommendations', [])
        if recommendations:
            st.markdown("#### 💡 Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
    
    # Skills breakdown
    skills_found = result.get('skills_found', {})
    if skills_found:
        technical_skills = skills_found.get('technical_skills', [])
        soft_skills = skills_found.get('soft_skills', [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔧 Technical Skills")
            st.metric("Total Skills", len(technical_skills))
            if technical_skills:
                # Show skills in a more compact way
                skills_text = ", ".join(technical_skills[:15])  # Show first 15
                if len(technical_skills) > 15:
                    skills_text += f" ... and {len(technical_skills) - 15} more"
                st.markdown(f"**Skills:** {skills_text}")
        
        with col2:
            st.markdown("#### 🤝 Soft Skills")
            st.metric("Total Skills", len(soft_skills))
            if soft_skills:
                st.markdown(f"**Skills:** {', '.join(soft_skills)}")
    
    # Resume metrics
    metrics = result.get('metrics', {})
    if metrics:
        st.markdown("#### 📊 Resume Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total Words", metrics.get('total_words', 0))
        with col2:
            st.metric("📏 Characters", metrics.get('total_characters', 0))
        with col3:
            st.metric("📋 Sections", metrics.get('sections_count', 0))
    
    # Processing time
    processing_time = result.get('processing_time', 0)
    st.markdown(f"**Processing Time:** {processing_time:.2f}s")

def show_results():
    st.markdown("## 📊 Results")
    
    # Check for existing results
    results_files = list(settings.OUTPUT_DIR.glob("*.json"))
    
    if results_files:
        selected_result = st.selectbox(
            "Select a result file:",
            [f.name for f in results_files],
            help="Choose a previous analysis result"
        )
        
        if st.button("📋 Load Results", help="Load and display the selected results"):
            result_path = settings.OUTPUT_DIR / selected_result
            with open(result_path, 'r') as f:
                results = json.load(f)
            
            display_results(results)
    else:
        st.info("ℹ️ No analysis results found. Run some analyses first!")

def display_results(results):
    st.markdown("### 📈 Detailed Results")
    
    # Handle single result or batch results
    if isinstance(results, dict) and 'resume_filename' in results:
        # Single result
        display_single_result(results)
    elif isinstance(results, dict) and 'results' in results:
        # Batch results
        display_batch_results(results)
    else:
        # Single result (new format)
        display_single_result(results)

def display_single_result(result):
    """Display a single resume analysis result"""
    st.markdown("#### 🎯 ATS Resume Analysis")
    
    # Overall score
    overall_score = result.get('overall_score', 0)
    st.markdown(f"### ✅ ATS Match Score: {overall_score:.0f}/100")
    
    # ATS Analysis
    ats_analysis = result.get('ats_analysis', {})
    if ats_analysis:
        # Detailed matches
        detailed_matches = ats_analysis.get('detailed_matches', [])
        if detailed_matches:
            st.markdown("#### 📌 Matching Breakdown")
            
            # Create a table for matches
            match_data = []
            for match in detailed_matches:
                requirement = match.get('requirement', '')
                matched = match.get('matched', '')
                details = match.get('details', '')
                match_data.append([requirement, matched, details])
            
            if match_data:
                df = pd.DataFrame(match_data, columns=['Job Requirement', 'Matched?', 'Details'])
                st.dataframe(df, use_container_width=True)
        
        # Highlights
        highlights = ats_analysis.get('highlights', [])
        if highlights:
            st.markdown("#### ⭐ Highlights in Resume")
            for highlight in highlights:
                st.markdown(f"✅ {highlight}")
        
        # Gaps
        gaps = ats_analysis.get('gaps', [])
        if gaps:
            st.markdown("#### 📉 Areas to Improve")
            for gap in gaps:
                st.markdown(f"⚠️ {gap}")
        
        # Recommendations
        recommendations = ats_analysis.get('recommendations', [])
        if recommendations:
            st.markdown("#### 💡 Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
    
    # Skills summary
    skills_found = result.get('skills_found', {})
    if skills_found:
        col1, col2 = st.columns(2)
        with col1:
            tech_skills = skills_found.get('technical_skills', [])
            st.metric("🔧 Technical Skills", len(tech_skills))
        with col2:
            soft_skills = skills_found.get('soft_skills', [])
            st.metric("🤝 Soft Skills", len(soft_skills))
    
    # Resume metrics
    metrics = result.get('metrics', {})
    if metrics:
        st.markdown("#### 📊 Resume Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total Words", metrics.get('total_words', 0))
        with col2:
            st.metric("📏 Characters", metrics.get('total_characters', 0))
        with col3:
            st.metric("📋 Sections", metrics.get('sections_count', 0))
    
    # Experience summary
    experience = result.get('experience', [])
    education = result.get('education', [])
    dates = result.get('dates', [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Dates Found", len(dates))
    with col2:
        st.metric("💼 Experience Entries", len(experience))
    with col3:
        st.metric("🎓 Education Entries", len(education))

def display_batch_results(results):
    """Display batch analysis results"""
    st.markdown("#### 📊 Batch Analysis Summary")
    
    # Summary
    if 'summary' in results:
        summary = results['summary']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Resumes", summary.get('total_resumes', 0))
        
        with col2:
            st.metric("Average Score", f"{summary.get('average_score', 0):.1%}")
        
        with col3:
            st.metric("Processing Time", f"{summary.get('processing_time', 0):.2f}s")
    
    # Detailed results
    if 'results' in results:
        st.markdown("#### 📋 Detailed Analysis")
        
        for i, result in enumerate(results['results']):
            with st.expander(f"Resume {i+1}: {result.get('resume_filename', 'Unknown')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Score:** {result.get('score', 0):.1%}")
                    st.write(f"**Skills:** {', '.join(result.get('skills', []))}")
                
                with col2:
                    st.write(f"**Text Length:** {result.get('text_length', 0):,} chars")
                    st.write(f"**Processing Time:** {result.get('processing_time', 0):.2f}s")

def show_settings():
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 🔧 Configuration")
    
    # Scoring weights
    st.markdown("#### 📊 Scoring Weights")
    st.markdown("Adjust how the AI calculates match scores:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keyword_weight = st.slider("Keyword Similarity", 0.0, 1.0, 0.4, 0.1, help="Weight for exact word matches")
        semantic_weight = st.slider("Semantic Similarity", 0.0, 1.0, 0.3, 0.1, help="Weight for meaning-based similarity")
    
    with col2:
        skill_weight = st.slider("Skill Match", 0.0, 1.0, 0.2, 0.1, help="Weight for skill alignment")
        experience_weight = st.slider("Experience Score", 0.0, 1.0, 0.1, 0.1, help="Weight for experience matching")
    
    # Save settings
    if st.button("💾 Save Settings", help="Apply the new scoring weights"):
        settings.SCORING_WEIGHTS.update({
            'keyword_similarity': keyword_weight,
            'semantic_similarity': semantic_weight,
            'skill_match': skill_weight,
            'experience_score': experience_weight
        })
        st.success("✅ Settings saved successfully!")
    
    # System info
    st.markdown("#### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Project Root:** {settings.PROJECT_ROOT}")
        st.write(f"**Data Directory:** {settings.DATA_DIR}")
    
    with col2:
        st.write(f"**Output Directory:** {settings.OUTPUT_DIR}")
        st.write(f"**Supported Formats:** {', '.join(settings.SUPPORTED_FORMATS)}")

def show_help_page():
    st.markdown("## ❓ Help & Support")
    
    st.markdown("### 📚 User Guide")
    st.markdown("""
    <div class="info-box">
        <h4>📖 Complete User Guide</h4>
        <p>For detailed instructions, troubleshooting, and advanced features, check out our comprehensive <a href="docs/USER_GUIDE.md" target="_blank">User Guide</a>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 Troubleshooting")
    
    # Common issues
    with st.expander("❌ File Upload Issues"):
        st.markdown("""
        **Problem**: File upload fails
        **Solutions**:
        - Check file format (PDF, DOCX, TXT only)
        - Ensure file size < 10MB
        - Try converting to different format
        - Check file is not corrupted
        """)
    
    with st.expander("❌ Analysis Fails"):
        st.markdown("""
        **Problem**: Resume analysis fails
        **Solutions**:
        - Check file contains readable text
        - Try with a different resume file
        - Ensure file is not password protected
        - Check file format compatibility
        """)
    
    with st.expander("❌ Low Match Scores"):
        st.markdown("""
        **Problem**: Consistently low match scores
        **Solutions**:
        - Improve job description clarity
        - Add more specific requirements
        - Check resume format and content
        - Adjust scoring weights in Settings
        """)
    
    st.markdown("### 📞 Support")
    st.markdown("""
    <div class="info-box">
        <h4>🆘 Need More Help?</h4>
        <p>• <strong>Documentation</strong>: Check the User Guide</p>
        <p>• <strong>GitHub Issues</strong>: Report bugs and feature requests</p>
        <p>• <strong>Author</strong>: Shashank B - [@ShashankBejjanki1241](https://github.com/ShashankBejjanki1241)</p>
        <p>• <strong>Project</strong>: [ApexHire](https://github.com/ShashankBejjanki1241/ApexHire)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
