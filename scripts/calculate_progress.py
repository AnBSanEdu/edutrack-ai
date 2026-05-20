import argparse
import json

def calculate_progress(completed, total):
    """Calculates the progress percentage."""
    if total == 0:
        return 0.0
    
    if completed < 0:
        completed = 0

    if completed > total:
        return 100.0
    
    progress = (completed / total) * 100
    return progress

def main():
    parser = argparse.ArgumentParser(description='Calculate progress percentage.')
    parser.add_argument('--completed', type=int, required=True, help='Number of completed tasks.')
    parser.add_argument('--total', type=int, required=True, help='Total number of tasks.')
    
    args = parser.parse_args()
    
    progress = calculate_progress(args.completed, args.total)
    
    result = {'progress': progress}
    print(json.dumps(result))

if __name__ == '__main__':
    main()
