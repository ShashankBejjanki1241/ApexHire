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
            print("\n📊 Analysis Results:")
            print("=" * 50)
            print(f"Overall Score: {result.get('overall_score', 0):.2%}")
            print(f"Skills Found: {', '.join(result.get('skills', []))}")
        
        print(f"✅ Analysis completed. Results saved to: {args.output}")
        
    else:
        print("❌ Please provide either --resume and --job, or --batch with --resumes and --jobs")
        print("Use --help for more information")
        sys.exit(1)

if __name__ == "__main__":
    main()
