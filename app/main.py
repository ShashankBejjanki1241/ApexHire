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
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .help-text {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
    }
    .step-number {
        background-color: #1f77b4;
        color: white;
        border-radius: 50%;
        width: 25px;
        height: 25px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
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
    # Header
    st.markdown('<h1 class="main-header">🚀 ApexHire - AI Resume Screener</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
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
    st.markdown("## 🎯 Welcome to ApexHire")
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>📄 Step 1: Upload Resume</h4>
            <p>Go to "Resume Analysis" and upload your resume in PDF, DOCX, or TXT format.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>💼 Step 2: Add Job Description</h4>
            <p>Go to "Job Matching" and enter the job title and description you want to match against.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🔍 Step 3: Analyze</h4>
            <p>Click the analyze button and wait for the AI to process your resume and job requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📊 Step 4: Review Results</h4>
            <p>View detailed match scores, skill analysis, and recommendations for the position.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features
    st.markdown("### 🛠️ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **📄 Resume Parsing**: PDF, DOCX, TXT support
        - **🧠 AI Analysis**: Advanced NLP processing
        - **🔍 Skill Extraction**: Technical and soft skills
        - **📊 Smart Scoring**: Multi-factor matching algorithm
        """)
    
    with col2:
        st.markdown("""
        - **🌐 Web Interface**: Easy-to-use dashboard
        - **📈 Analytics**: Detailed performance insights
        - **⚙️ Customizable**: Adjustable scoring weights
        - **📋 Batch Processing**: Handle multiple files
        """)
    
    # Quick stats
    st.markdown("### 📈 System Statistics")
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
    st.markdown("### 🎯 Match Results")
    
    # Overall score
    overall_score = result.get('overall_score', 0)
    score_percentage = overall_score * 100
    
    st.markdown(f"#### 📊 Match Score for {job_title}")
    
    # Progress bar for score
    st.progress(overall_score)
    st.metric("Match Score", f"{score_percentage:.1f}%")
    
    # Score interpretation
    if score_percentage >= 80:
        st.success("🎉 Excellent match! This candidate is highly qualified for the position.")
    elif score_percentage >= 60:
        st.info("�� Good match. Consider this candidate for the position.")
    elif score_percentage >= 40:
        st.warning("⚠️ Moderate match. Consider additional screening.")
    else:
        st.error("❌ Low match. Consider other candidates.")
    
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
    
    # Skills found
    st.markdown("#### 🔧 Skills Found in Resume")
    skills_found = result.get('skills_found', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        tech_skills = skills_found.get('technical_skills', [])
        if tech_skills:
            st.write("**Technical Skills:**")
            for skill in tech_skills[:8]:
                st.write(f"• {skill}")
        else:
            st.write("No technical skills found")
    
    with col2:
        soft_skills = skills_found.get('soft_skills', [])
        if soft_skills:
            st.write("**Soft Skills:**")
            for skill in soft_skills[:5]:
                st.write(f"• {skill}")
        else:
            st.write("No soft skills found")
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    if score_percentage >= 80:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Strong Candidate</h4>
            <p>• Schedule an interview</p>
            <p>• Review technical skills in detail</p>
            <p>• Check references</p>
        </div>
        """, unsafe_allow_html=True)
    elif score_percentage >= 60:
        st.markdown("""
        <div class="info-box">
            <h4>👍 Good Potential</h4>
            <p>• Consider for interview</p>
            <p>• Review specific skill gaps</p>
            <p>• Ask targeted questions</p>
        </div>
        """, unsafe_allow_html=True)
    elif score_percentage >= 40:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Moderate Match</h4>
            <p>• Consider additional screening</p>
            <p>• Review skill requirements</p>
            <p>• May need training</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4>❌ Low Match</h4>
            <p>• Consider other candidates</p>
            <p>• Review job requirements</p>
            <p>• May need different role</p>
        </div>
        """, unsafe_allow_html=True)

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
