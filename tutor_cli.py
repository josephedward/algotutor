#!/usr/bin/env python3
"""
Algorithm Tutor CLI

A simple command-line interface for the algorithm tutor study system.
"""

import argparse
import sys
from study_system import StudySystemManager


def main():
    parser = argparse.ArgumentParser(description='Algorithm Tutor Study System CLI')
    parser.add_argument('--student', '-s', required=True, help='Student ID')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start session command
    start_parser = subparsers.add_parser('start', help='Start a study session')
    
    # End session command
    end_parser = subparsers.add_parser('end', help='End a study session')
    end_parser.add_argument('--session', required=True, help='Session ID')
    end_parser.add_argument('--topics', nargs='+', required=True, help='Topics covered')
    end_parser.add_argument('--attempted', type=int, required=True, help='Problems attempted')
    end_parser.add_argument('--completed', type=int, required=True, help='Problems completed')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show student statistics')
    
    # Recommendations command
    recommend_parser = subparsers.add_parser('recommend', help='Get topic recommendations')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize study system
    study_system = StudySystemManager()
    
    if args.command == 'start':
        session_id = study_system.start_study_session(args.student)
        print(f"Started study session: {session_id}")
        print(f"Use this session ID to end the session when you're done studying.")
        
    elif args.command == 'end':
        study_system.end_study_session(
            args.student,
            args.session,
            args.topics,
            args.attempted,
            args.completed
        )
        print(f"Ended study session {args.session}")
        print(f"Topics covered: {', '.join(args.topics)}")
        print(f"Problems: {args.completed}/{args.attempted} completed")
        
        # Show updated stats
        stats = study_system.get_student_statistics(args.student)
        if stats:
            print(f"\nUpdated progress:")
            print(f"  Total problems solved: {stats['total_problems_solved']}")
            print(f"  Topics mastered: {stats['topics_mastered']}")
            if stats['mastered_topics']:
                print(f"  Mastered topics: {', '.join(stats['mastered_topics'])}")
        
    elif args.command == 'stats':
        stats = study_system.get_student_statistics(args.student)
        if not stats:
            print(f"No progress data found for student '{args.student}'")
            return
            
        print(f"Statistics for student '{args.student}':")
        print(f"  Current level: {stats['current_level']}")
        print(f"  Topics mastered: {stats['topics_mastered']}")
        print(f"  Total problems solved: {stats['total_problems_solved']}")
        print(f"  Total study sessions: {stats['total_sessions']}")
        print(f"  Last active: {stats['last_active'] or 'Never'}")
        
        if stats['mastered_topics']:
            print(f"  Mastered topics: {', '.join(stats['mastered_topics'])}")
        
        if stats['recommended_topics']:
            print(f"  Recommended next topics: {', '.join(stats['recommended_topics'])}")
    
    elif args.command == 'recommend':
        recommendations = study_system.get_recommended_topics(args.student)
        if not recommendations:
            print(f"No recommendations available for student '{args.student}'")
            print("This might mean all topics are mastered or no progress has been recorded yet.")
        else:
            print(f"Recommended topics for '{args.student}':")
            for topic in recommendations:
                print(f"  - {topic}")


if __name__ == '__main__':
    main()