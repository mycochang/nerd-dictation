import time
import os
import sys
import subprocess

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.transcribe import transcribe_audio

def benchmark_latency(audio_file, model_size="tiny.en"):
    print(f"Benchmarking model: {model_size} on CPU...")
    
    start_time = time.time()
    result = transcribe_audio(audio_file, model_size=model_size, device="cpu", compute_type="int8")
    duration = time.time() - start_time
    
    print(f"Result: '{result}'")
    print(f"Latency: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    # Create a 2-second dummy wav file if it doesn't exist
    test_wav = "tests/benchmark_test.wav"
    if not os.path.exists(test_wav):
        print("Creating dummy audio for benchmark...")
        # Speak something into it if we wanted real text, but for latency silence is fine
        subprocess.run(["sox", "-n", "-r", "16000", "-c", "1", test_wav, "trim", "0.0", "2.0"])

    bench_tiny = benchmark_latency(test_wav, "tiny.en")
    bench_base = benchmark_latency(test_wav, "base.en")
    
    print("\nSummary:")
    print(f"Tiny model: {bench_tiny:.4f}s")
    print(f"Base model: {bench_base:.4f}s")
