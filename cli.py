import argparse
import sys
import json
from pathlib import Path
import asyncio
from .main import AudioSummarizer, create_async_summarizer

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Process audio files to generate summaries and action items."
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the audio file to process"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to save the output JSON file (default: input_file_summary.json)"
    )
    
    parser.add_argument(
        "--create-tasks",
        action="store_true",
        help="Create tasks from extracted action items"
    )
    
    parser.add_argument(
        "--schedule-followup",
        action="store_true",
        help="Schedule a follow-up meeting based on the summary"
    )
    
    parser.add_argument(
        "--async",
        action="store_true",
        help="Run processing asynchronously"
    )
    
    return parser

async def process_async(
    input_file: str,
    create_tasks: bool = False,
    schedule_followup: bool = False
) -> dict:
    """Process audio file asynchronously."""
    async with await create_async_summarizer() as summarizer:
        return await summarizer.process_audio_file_async(
            input_file,
            create_tasks=create_tasks,
            schedule_followup=schedule_followup
        )

def process_sync(
    input_file: str,
    create_tasks: bool = False,
    schedule_followup: bool = False
) -> dict:
    """Process audio file synchronously."""
    summarizer = AudioSummarizer()
    return summarizer.process_audio_file(
        input_file,
        create_tasks=create_tasks,
        schedule_followup=schedule_followup
    )

def save_results(results: dict, output_path: str):
    """Save processing results to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)
    
    output_path = args.output
    if not output_path:
        output_path = str(input_path.with_suffix('')) + "_summary.json"
    
    try:
        if getattr(args, 'async'):
            results = asyncio.run(process_async(
                str(input_path),
                create_tasks=args.create_tasks,
                schedule_followup=args.schedule_followup
            ))
        else:
            results = process_sync(
                str(input_path),
                create_tasks=args.create_tasks,
                schedule_followup=args.schedule_followup
            )
        
        save_results(results, output_path)
        print(f"Processing complete. Results saved to: {output_path}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()