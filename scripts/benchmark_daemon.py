import socket
import time
import os
import sys

SOCKET_PATH = f"/run/user/{os.getuid()}/jarvis.sock"
AUDIO_FILE = os.path.abspath("tests/benchmark_test.wav")

def benchmark_daemon():
    if not os.path.exists(SOCKET_PATH):
        print(f"Error: Socket {SOCKET_PATH} not found. Is jarvis.service running?")
        return

    print(f"Benchmarking Daemon at {SOCKET_PATH}...")
    print(f"Audio File: {AUDIO_FILE}")

    # Warmup
    print("Warming up...", end="")
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(SOCKET_PATH)
            client.sendall(AUDIO_FILE.encode('utf-8'))
            _ = client.recv(4096)
        print(" Done.")
    except Exception as e:
        print(f"\nWarmup failed: {e}")
        return

    # Benchmark
    latencies = []
    for i in range(5):
        start = time.time()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(SOCKET_PATH)
            client.sendall(AUDIO_FILE.encode('utf-8'))
            response = client.recv(4096).decode('utf-8')
        end = time.time()
        lat = (end - start) * 1000
        latencies.append(lat)
        print(f"Run {i+1}: {lat:.2f} ms | Text: '{response.strip()}'")
        time.sleep(0.5)

    avg = sum(latencies) / len(latencies)
    print(f"\nAverage Daemon Latency: {avg:.2f} ms")

if __name__ == "__main__":
    benchmark_daemon()
