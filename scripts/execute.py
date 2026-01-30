import subprocess

def execute_command(command):
    """
    Executes a shell command and captures output.
    Returns (stdout, stderr, returncode).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 execute.py <command>")
        sys.exit(1)
    
    out, err, code = execute_command(sys.argv[1])
    print(f"Code: {code}")
    print(f"Stdout: {out}")
    print(f"Stderr: {err}")

if __name__ == "__main__":
    main()
