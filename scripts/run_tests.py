import subprocess
import sys

def run_tests():
    """Run all tests with coverage report."""
    try:
        subprocess.check_call([
            "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html:coverage_report",
            "tests/"
        ])
        
        print("\nTests completed successfully!")
        print("Coverage report generated in: coverage_report/index.html")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()