"""
Streamlit Web Application for AI Resume Screener
"""

import streamlit as st
import os
import sys
import pandas as pd
import json
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main_pipeline import ResumeScreenerPipeline


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="ApexHire - AI Resume Screener",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.markdown('<h1 style="text-align: center; color: #1f77b4;">🚀 ApexHire - AI Resume Screener</h1>', unsafe_allow_html=True)
    st.markdown("### Built by Shashank B")
    
    # Sidebar
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Home", "📄 Upload & Screen", "📊 Results", "ℹ️ About"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "📄 Upload & Screen":
        show_upload_page()
    elif page == "📊 Results":
        show_results_page()
    elif page == "ℹ️ About":
        show_about_page()


def show_home_page():
    """Display the home page"""
    st.markdown("## Welcome to ApexHire")
    
    st.markdown("""
    **ApexHire** is an intelligent AI-powered resume screening system that automatically analyzes, 
    scores, and ranks resumes based on job descriptions. It mimics what a human recruiter does—but 
    faster and more consistently.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Key Features")
        st.markdown("""
        - 📝 **Resume Parsing**: Reads PDF and DOCX formats
        - 🧹 **Text Preprocessing**: Cleans and tokenizes text
        - 🧠 **Skill Extraction**: Identifies technical and soft skills
        - 🎯 **Relevance Scoring**: Matches resumes to job descriptions
        - 📊 **Ranking & Output**: Ranks candidates and exports results
        - 🧾 **Semantic Matching**: Uses AI embeddings for better matching
        """)
    
    with col2:
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - **Python 3.10+**: Core language
        - **spaCy**: NLP processing
        - **sentence-transformers**: Semantic similarity
        - **scikit-learn**: Machine learning
        - **Streamlit**: Web interface
        - **PDF/DOCX parsing**: Document processing
        """)
    
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    1. **Upload Resumes**: Add PDF/DOCX resume files to `data/resumes/`
    2. **Add Job Description**: Create a job description file in `data/job_descriptions/`
    3. **Run Screening**: Use the "Upload & Screen" page to process resumes
    4. **View Results**: Check the "Results" page for rankings and analysis
    """)


def show_upload_page():
    """Display the upload and screening page"""
    st.markdown("## 📄 Upload & Screen Resumes")
    
    # File upload section
    st.markdown("### 📁 Upload Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Resume Files")
        uploaded_resumes = st.file_uploader(
            "Upload resume files (PDF/DOCX)",
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            help="Upload multiple resume files to screen"
        )
        
        if uploaded_resumes:
            st.success(f"Uploaded {len(uploaded_resumes)} resume files")
    
    with col2:
        st.markdown("#### Job Description")
        uploaded_job = st.file_uploader(
            "Upload job description (TXT/DOCX)",
            type=['txt', 'docx'],
            help="Upload a job description file"
        )
        
        if uploaded_job:
            st.success("Job description uploaded successfully!")
    
    # Manual job description input
    st.markdown("### 📝 Or Enter Job Description Manually")
    job_description_text = st.text_area(
        "Job Description",
        height=200,
        placeholder="Enter the job description here...",
        help="Paste the job description text directly"
    )
    
    # Run screening
    st.markdown("### 🚀 Run Screening")
    
    if st.button("🎯 Start Resume Screening", type="primary"):
        if not uploaded_resumes and not os.path.exists("data/resumes"):
            st.error("❌ No resumes available. Please upload resume files first.")
            return
        
        if not uploaded_job and not job_description_text and not os.path.exists("data/job_descriptions"):
            st.error("❌ No job description available. Please upload or enter a job description.")
            return
        
        # Show progress
        with st.spinner("🔄 Processing resumes..."):
            try:
                # Initialize pipeline
                pipeline = ResumeScreenerPipeline()
                
                # Get job description
                if uploaded_job:
                    job_desc = uploaded_job.read().decode('utf-8')
                elif job_description_text:
                    job_desc = job_description_text
                else:
                    # Load from file
                    job_files = [f for f in os.listdir("data/job_descriptions") if f.endswith(('.txt', '.docx'))]
                    if job_files:
                        with open(f"data/job_descriptions/{job_files[0]}", 'r') as f:
                            job_desc = f.read()
                    else:
                        st.error("No job description found")
                        return
                
                # Get resume directory
                resume_dir = "data/resumes"
                
                # Run screening
                results = pipeline.screen_resumes(
                    resume_directory=resume_dir,
                    job_description=job_desc
                )
                
                if results:
                    st.success(f"✅ Screening completed! Processed {len(results)} resumes.")
                    
                    # Display results
                    st.markdown("### 📊 Results")
                    for i, result in enumerate(results[:5], 1):
                        st.markdown(f"**#{i}**: {result['filename']} (Score: {result['score']:.3f})")
                    
                else:
                    st.error("❌ Screening failed. Check the logs for details.")
                    
            except Exception as e:
                st.error(f"❌ Error during screening: {str(e)}")


def show_results_page():
    """Display the results page"""
    st.markdown("## 📊 Screening Results")
    
    # Check for results files
    results_files = []
    if os.path.exists("output"):
        results_files = [f for f in os.listdir("output") if f.endswith(('.csv', '.json'))]
    
    if not results_files:
        st.warning("📭 No results found. Run a screening first to see results here.")
        return
    
    # Load summary report
    summary_file = "output/summary_report.json"
    if os.path.exists(summary_file):
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        st.markdown("### 📈 Latest Results")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Resumes", summary.get('summary', {}).get('total_resumes', 0))
        
        with col2:
            st.metric("Average Score", f"{summary.get('summary', {}).get('average_score', 0):.3f}")
        
        with col3:
            st.metric("Highest Score", f"{summary.get('summary', {}).get('highest_score', 0):.3f}")
        
        with col4:
            st.metric("Lowest Score", f"{summary.get('summary', {}).get('lowest_score', 0):.3f}")
        
        # Top candidates
        st.markdown("### 🏆 Top Candidates")
        top_candidates = summary.get('top_candidates', [])
        
        for candidate in top_candidates:
            st.markdown(f"**#{candidate['rank']}**: {candidate['filename']} (Score: {candidate['score']:.3f})")


def show_about_page():
    """Display the about page"""
    st.markdown("## ℹ️ About ApexHire")
    
    st.markdown("""
    ### 🎯 Project Overview
    
    **ApexHire** is an AI-powered resume screening system that automatically analyzes, scores, 
    and ranks resumes based on job descriptions. It uses advanced Natural Language Processing (NLP) 
    techniques to mimic what a human recruiter does—but faster and more consistently.
    
    ### 🚀 Key Features
    
    - **📝 Resume Parsing**: Reads resumes in PDF and DOCX formats
    - **🧹 Text Preprocessing**: Cleans text, removes noise, and tokenizes
    - **🧠 Skill & Info Extraction**: Extracts skills, education, experience, and entities
    - **🎯 Relevance Scoring**: Matches resume content with job description
    - **📊 Ranking & Output**: Ranks candidates and exports result in CSV
    - **🧾 Semantic Matching**: Uses embeddings to compare meaning, not just keywords
    - **🖥️ Web UI**: Upload resumes and job descriptions via Streamlit
    
    ### 🛠️ Tech Stack
    
    - **Python 3.10+**: Core programming language
    - **spaCy**: Tokenization, lemmatization, NER
    - **sentence-transformers**: Semantic similarity via BERT embeddings
    - **scikit-learn**: TF-IDF vectorization and cosine similarity
    - **pdfplumber & python-docx**: Resume parsing
    - **Streamlit**: Web interface
    - **pandas & numpy**: Data processing
    
    ### 🧑‍💻 Author
    
    **Shashank B**
    
    This project demonstrates advanced NLP skills, Python development, and practical AI application 
    for real-world recruitment problems.
    
    ### 📄 License
    
    MIT License – Feel free to use and modify this project with credit to the author.
    """)


if __name__ == "__main__":
    main()
