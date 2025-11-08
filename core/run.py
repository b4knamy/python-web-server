from watchfiles import run_process
import subprocess


def run_server():
    subprocess.run(["python", "core/server.py"])


if __name__ == "__main__":
    print("👀 Watching for file changes... (Ctrl+C to stop)")
    run_process(
        ".",        
        target=run_server, 
        recursive=True     
    )
