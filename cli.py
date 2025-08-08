#!/usr/bin/env python3
"""
Command Line Interface for ApexHire AI Resume Screener
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from main_pipeline import ResumeScreener

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="ApexHire - AI Resume Screener",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --resume data/resumes/my_resume.pdf --job data/jobs/ios_developer.txt
  python cli.py --batch --resumes data/resumes/ --jobs data/jobs/
  python cli.py --web
        """
    )
    
    parser.add_argument(
        '--resume', '-r',
        type=str,
        help='Path to resume file'
    )
    
    parser.add_argument(
        '--job', '-j',
        type=str,
        help='Path to job description file'
    )
    
    parser.add_argument(
        '--resumes', '-R',
        type=str,
        help='Directory containing resume files'
    )
    
    parser.add_argument(
        '--jobs', '-J',
        type=str,
        help='Directory containing job description files'
    )
    
    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Process multiple files in batch mode'
    )
    
    parser.add_argument(
        '--web', '-w',
        action='store_true',
        help='Launch web interface'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output/results.json',
        help='Output file path'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Initialize the screener
    screener = ResumeScreener()
    
    if args.web:
        print("🌐 Launching web interface...")
        os.system("streamlit run app/main.py")
        return
    
    if args.batch:
        if not args.resumes or not args.jobs:
            print("❌ Batch mode requires --resumes and --jobs directories")
            sys.exit(1)
        
        print(f"📁 Processing resumes from: {args.resumes}")
        print(f"📁 Processing jobs from: {args.jobs}")
        
        results = screener.run_batch_analysis(
            resumes_dir=args.resumes,
            jobs_dir=args.jobs,
            output_file=args.output
        )
        
        print(f"✅ Batch analysis completed. Results saved to: {args.output}")
        
    elif args.resume and args.job:
        print(f"📄 Analyzing resume: {args.resume}")
        print(f"💼 Against job: {args.job}")
        
        result = screener.analyze_single_resume(
            resume_path=args.resume,
            job_path=args.job,
            output_file=args.output
        )
        
        if args.verbose:
            print("\n🎯 ATS Resume Match & Score Report")
            print("=" * 60)
            
            # ATS Score
            ats_analysis = result.get('ats_analysis', {})
            overall_score = ats_analysis.get('overall_score', result.get('overall_score', 0))
            print(f"✅ ATS Match Score: {overall_score:.0f}/100")
            
            # Detailed Matches
            detailed_matches = ats_analysis.get('detailed_matches', [])
            if detailed_matches:
                print("\n📌 Matching Breakdown")
                print("Job Requirement\t\tMatched in Resume?\tDetails\t\tConfidence")
                for match in detailed_matches:
                    requirement = match.get('requirement', '')
                    matched = match.get('matched', '')
                    details = match.get('details', '')
                    confidence = match.get('confidence', 0)
                    explanation = match.get('explanation', '')
                    
                    print(f"{requirement:<25}\t{matched:<20}\t{details:<20}\t{confidence:.1%}")
                    if explanation:
                        print(f"   💡 {explanation}")
                    print()
            
            # Highlights
            highlights = ats_analysis.get('highlights', [])
            if highlights:
                print("\n⭐ Highlights in Resume")
                for highlight in highlights:
                    print(f"✅ {highlight}")
            
            # Gaps
            gaps = ats_analysis.get('gaps', [])
            if gaps:
                print("\n📉 Areas to Improve for 100% Match")
                print("Gap Area\t\t\tRecommendation")
                for gap in gaps:
                    print(f"{gap}")
            
            # Recommendations
            recommendations = ats_analysis.get('recommendations', [])
            if recommendations:
                print("\n💡 Recommendations")
                for i, rec in enumerate(recommendations, 1):
                    print(f"{i}. {rec}")
            
            # Skills Summary
            skills_found = result.get('skills_found', {})
            if skills_found:
                tech_skills = skills_found.get('technical_skills', [])
                soft_skills = skills_found.get('soft_skills', [])
                print(f"\n🔧 Technical Skills Found: {len(tech_skills)}")
                print(f"🤝 Soft Skills Found: {len(soft_skills)}")
            
            # Experience Summary
            experience = result.get('experience', [])
            education = result.get('education', [])
            dates = result.get('dates', [])
            
            print(f"\n📊 Resume Analysis Summary:")
            print(f"   📅 Dates Found: {len(dates)}")
            print(f"   💼 Experience Entries: {len(experience)}")
            print(f"   🎓 Education Entries: {len(education)}")
            
            # Contact info
            contact_info = result.get('contact_info', {})
            if contact_info:
                print(f"   📧 Contact: {contact_info.get('email', 'Not found')}")
            
            # Metrics
            metrics = result.get('metrics', {})
            if metrics:
                print(f"   📝 Total Words: {metrics.get('total_words', 0)}")
                print(f"   📏 Total Characters: {metrics.get('total_characters', 0)}")
                print(f"   📋 Sections Found: {metrics.get('sections_count', 0)}")
        
        print(f"✅ Analysis completed. Results saved to: {args.output}")
        
    else:
        print("❌ Please provide either --resume and --job, or --batch with --resumes and --jobs")
        print("Use --help for more information")
        sys.exit(1)

if __name__ == "__main__":
    main()
