from watchfiles import run_process
import subprocess


def run_server():
    # Start your custom Python web server
    subprocess.run(["python", "core/server.py"])


if __name__ == "__main__":
    print("👀 Watching for file changes... (Ctrl+C to stop)")
    run_process(
        ".",                # Watch current directory
        target=run_server,  # Function to call when a change happens
        recursive=True      # Also watch subfolders
    )
