"""
Analytics components for ApexHire dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import json
from pathlib import Path
import config.settings as settings

def create_skill_distribution_chart(skills_data: Dict[str, List[str]]) -> go.Figure:
    """Create a skill distribution chart"""
    
    # Count skills
    skill_counts = {}
    for skill_type, skills in skills_data.items():
        for skill in skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    if not skill_counts:
        return go.Figure()
    
    # Create chart
    fig = go.Figure(data=[
        go.Bar(
            x=list(skill_counts.keys()),
            y=list(skill_counts.values()),
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="Skill Distribution",
        xaxis_title="Skills",
        yaxis_title="Frequency",
        height=400
    )
    
    return fig

def create_score_comparison_chart(results: List[Dict[str, Any]]) -> go.Figure:
    """Create a score comparison chart"""
    
    if not results:
        return go.Figure()
    
    # Extract scores
    scores = []
    labels = []
    
    for result in results:
        for match in result.get('job_matches', []):
            scores.append(match.get('overall_score', 0))
            labels.append(f"{result.get('resume_filename', 'Unknown')} vs {match.get('job_name', 'Unknown')}")
    
    if not scores:
        return go.Figure()
    
    # Create chart
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=scores,
            marker_color='lightgreen'
        )
    ])
    
    fig.update_layout(
        title="Score Comparison",
        xaxis_title="Resume vs Job",
        yaxis_title="Match Score",
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

def create_processing_time_chart(results: List[Dict[str, Any]]) -> go.Figure:
    """Create a processing time chart"""
    
    if not results:
        return go.Figure()
    
    # Extract processing times
    times = []
    labels = []
    
    for result in results:
        analysis = result.get('resume_analysis', {})
        times.append(analysis.get('processing_time', 0))
        labels.append(result.get('resume_filename', 'Unknown'))
    
    if not times:
        return go.Figure()
    
    # Create chart
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=times,
            marker_color='lightcoral'
        )
    ])
    
    fig.update_layout(
        title="Processing Time Analysis",
        xaxis_title="Resume File",
        yaxis_title="Processing Time (seconds)",
        height=400
    )
    
    return fig

def display_analytics_dashboard(results_file: str):
    """Display comprehensive analytics dashboard"""
    
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        st.markdown("## 📊 Analytics Dashboard")
        
        # Summary metrics
        summary = results.get('summary', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Resumes", summary.get('total_resumes', 0))
        
        with col2:
            st.metric("Total Jobs", summary.get('total_jobs', 0))
        
        with col3:
            st.metric("Total Matches", summary.get('total_matches', 0))
        
        with col4:
            st.metric("Avg Score", f"{summary.get('average_score', 0):.1%}")
        
        # Charts
        st.markdown("### 📈 Performance Charts")
        
        # Skill distribution
        all_skills = {'technical_skills': [], 'soft_skills': []}
        for result in results.get('results', []):
            analysis = result.get('resume_analysis', {})
            skills = analysis.get('skills', {})
            for skill_type, skills_list in skills.items():
                if skill_type in all_skills:
                    all_skills[skill_type].extend(skills_list)
        
        if any(all_skills.values()):
            fig1 = create_skill_distribution_chart(all_skills)
            st.plotly_chart(fig1, use_container_width=True)
        
        # Score comparison
        fig2 = create_score_comparison_chart(results.get('results', []))
        if fig2.data:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Processing time
        fig3 = create_processing_time_chart(results.get('results', []))
        if fig3.data:
            st.plotly_chart(fig3, use_container_width=True)
        
        # Detailed results table
        st.markdown("### 📋 Detailed Results")
        
        if results.get('results'):
            # Prepare data for table
            table_data = []
            for result in results['results']:
                for match in result.get('job_matches', []):
                    table_data.append({
                        'Resume': result.get('resume_filename', 'Unknown'),
                        'Job': match.get('job_name', 'Unknown'),
                        'Score': f"{match.get('overall_score', 0):.1%}",
                        'Processing Time': f"{match.get('processing_time', 0):.2f}s"
                    })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

def create_performance_report(results: Dict[str, Any]) -> str:
    """Create a performance report"""
    
    summary = results.get('summary', {})
    
    report = f"""
# ApexHire Performance Report

## Summary
- **Total Resumes Processed**: {summary.get('total_resumes', 0)}
- **Total Jobs Analyzed**: {summary.get('total_jobs', 0)}
- **Total Matches**: {summary.get('total_matches', 0)}
- **Average Score**: {summary.get('average_score', 0):.1%}
- **Processing Time**: {summary.get('processing_time', 0):.2f} seconds

## Performance Metrics
- **Average Processing Time per Resume**: {summary.get('processing_time', 0) / max(summary.get('total_resumes', 1), 1):.2f} seconds
- **Matches per Resume**: {summary.get('total_matches', 0) / max(summary.get('total_resumes', 1), 1):.1f}
- **Success Rate**: {(summary.get('total_matches', 0) / max(summary.get('total_resumes', 1) * summary.get('total_jobs', 1), 1)) * 100:.1f}%

## Recommendations
"""
    
    avg_score = summary.get('average_score', 0)
    if avg_score >= 0.7:
        report += "- System is performing excellently\n"
    elif avg_score >= 0.5:
        report += "- System is performing well\n"
    else:
        report += "- Consider adjusting scoring weights\n"
    
    return report
