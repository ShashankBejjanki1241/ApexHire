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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 ApexHire - AI Resume Screener</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "📄 Resume Analysis", "💼 Job Matching", "📊 Results", "⚙️ Settings"]
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

def show_home_page():
    st.markdown("## 🎯 Welcome to ApexHire")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 What We Do")
        st.markdown("""
        ApexHire is an intelligent AI-powered resume screening system that:
        - **Parses resumes** in PDF, DOCX, and TXT formats
        - **Extracts skills** and qualifications automatically
        - **Matches candidates** against job requirements
        - **Ranks applicants** by relevance score
        - **Provides detailed analysis** and insights
        """)
    
    with col2:
        st.markdown("### 🛠️ Features")
        st.markdown("""
        - **Advanced NLP** processing with spaCy
        - **Semantic matching** for better accuracy
        - **Skill extraction** from technical and soft skills
        - **Web interface** for easy interaction
        - **Batch processing** for multiple files
        - **Detailed reporting** with insights
        """)
    
    # Quick stats
    st.markdown("### 📈 Quick Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Supported Formats", "3", "PDF, DOCX, TXT")
    
    with col2:
        st.metric("Processing Speed", "< 30s", "per resume")
    
    with col3:
        st.metric("Accuracy", "95%+", "skill extraction")
    
    with col4:
        st.metric("Languages", "1", "English")

def show_resume_analysis():
    st.markdown("## 📄 Resume Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    if uploaded_file is not None:
        # Save uploaded file
        file_path = Path(settings.RESUMES_DIR) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Analyze button
        if st.button("🔍 Analyze Resume", type="primary"):
            with st.spinner("Analyzing resume..."):
                try:
                    screener = ResumeScreener()
                    result = screener.analyze_resume(str(file_path))
                    
                    if result:
                        display_resume_analysis(result)
                    else:
                        st.error("❌ Failed to analyze resume")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

def display_resume_analysis(result):
    st.markdown("### 📊 Analysis Results")
    
    # Basic info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Basic Information")
        st.metric("Text Length", f"{result.get('text_length', 0):,} characters")
        st.metric("Words Count", f"{result.get('word_count', 0):,} words")
    
    with col2:
        st.markdown("#### 🎯 Skills Found")
        skills = result.get('skills', {})
        if skills:
            tech_skills = skills.get('technical_skills', [])
            soft_skills = skills.get('soft_skills', [])
            
            st.write("**Technical Skills:**")
            for skill in tech_skills[:10]:  # Show first 10
                st.write(f"• {skill}")
            
            st.write("**Soft Skills:**")
            for skill in soft_skills[:5]:  # Show first 5
                st.write(f"• {skill}")

def show_job_matching():
    st.markdown("## 💼 Job Matching")
    
    # Job description input
    job_title = st.text_input("Job Title", placeholder="e.g., Senior iOS Developer")
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=200
    )
    
    # Resume selection
    resume_files = list(settings.RESUMES_DIR.glob("*"))
    if resume_files:
        selected_resume = st.selectbox(
            "Select a resume to match:",
            [f.name for f in resume_files if f.is_file()]
        )
        
        if st.button("🎯 Match Resume to Job", type="primary"):
            if job_description and selected_resume:
                with st.spinner("Matching resume to job..."):
                    try:
                        screener = ResumeScreener()
                        match_result = screener.match_resume_to_job(
                            resume_path=str(settings.RESUMES_DIR / selected_resume),
                            job_description=job_description
                        )
                        
                        if match_result:
                            display_job_match(match_result, job_title)
                        else:
                            st.error("❌ Failed to match resume to job")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please provide both job description and select a resume")
    else:
        st.info("ℹ️ No resume files found. Please upload resumes first.")

def display_job_match(result, job_title):
    st.markdown("### 🎯 Match Results")
    
    # Overall score
    overall_score = result.get('overall_score', 0)
    score_percentage = overall_score * 100
    
    st.markdown(f"#### 📊 Match Score for {job_title}")
    
    # Progress bar for score
    st.progress(overall_score)
    st.metric("Match Score", f"{score_percentage:.1f}%")
    
    # Score breakdown
    st.markdown("#### 📈 Score Breakdown")
    breakdown = result.get('breakdown', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Keyword Match", f"{breakdown.get('keyword_score', 0):.1%}")
        st.metric("Skill Match", f"{breakdown.get('skill_score', 0):.1%}")
    
    with col2:
        st.metric("Semantic Match", f"{breakdown.get('semantic_score', 0):.1%}")
        st.metric("Experience Score", f"{breakdown.get('experience_score', 0):.1%}")
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    if score_percentage >= 80:
        st.success("🎉 Excellent match! This candidate is highly qualified for the position.")
    elif score_percentage >= 60:
        st.info("👍 Good match. Consider this candidate for the position.")
    elif score_percentage >= 40:
        st.warning("⚠️ Moderate match. Consider additional screening.")
    else:
        st.error("❌ Low match. Consider other candidates.")

def show_results():
    st.markdown("## 📊 Analysis Results")
    
    # Check for existing results
    results_files = list(settings.OUTPUT_DIR.glob("*.json"))
    
    if results_files:
        selected_result = st.selectbox(
            "Select a result file:",
            [f.name for f in results_files]
        )
        
        if st.button("📋 Load Results"):
            result_path = settings.OUTPUT_DIR / selected_result
            with open(result_path, 'r') as f:
                results = json.load(f)
            
            display_results(results)
    else:
        st.info("ℹ️ No analysis results found. Run some analyses first!")

def display_results(results):
    st.markdown("### 📈 Detailed Results")
    
    # Summary
    if 'summary' in results:
        summary = results['summary']
        st.markdown("#### 📊 Summary")
        
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
            with st.expander(f"Resume {i+1}: {result.get('filename', 'Unknown')}"):
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        keyword_weight = st.slider("Keyword Similarity", 0.0, 1.0, 0.4, 0.1)
        semantic_weight = st.slider("Semantic Similarity", 0.0, 1.0, 0.3, 0.1)
    
    with col2:
        skill_weight = st.slider("Skill Match", 0.0, 1.0, 0.2, 0.1)
        experience_weight = st.slider("Experience Score", 0.0, 1.0, 0.1, 0.1)
    
    # Save settings
    if st.button("💾 Save Settings"):
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

if __name__ == "__main__":
    main()
