#!/bin/bash

# Usage: ./monitor_resources.sh <output_log> [duration_seconds]

LOG_FILE="$1"
DURATION="${2:-3600}" # Default 1 hour
INTERVAL="${MONITOR_INTERVAL:-5}"

if [ -z "$LOG_FILE" ]; then
    echo "Usage: $0 <output_log> [duration_seconds]"
    exit 1
fi

echo "Starting Resource Monitor for $DURATION seconds..."
echo "Log: $LOG_FILE"
echo "Timestamp, PID, %CPU, %MEM, VRAM_MiB" > "$LOG_FILE"

END_TIME=$(( $(date +%s) + DURATION ))

while [ $(date +%s) -lt $END_TIME ]; do
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    
    # Find python daemons (jarvis_daemon.py)
    PIDS=$(pgrep -f "jarvis_daemon.py")
    
    if [ -z "$PIDS" ]; then
        echo "$TIMESTAMP, NONE, 0, 0, 0" >> "$LOG_FILE"
    else
        for PID in $PIDS; do
            # Get CPU/MEM via ps
            STATS=$(ps -p $PID -o %cpu,%mem --no-headers | sed 's/^[ 	]*//;s/[ 	]*$//;s/[ 	]	/, /')
            
            # Get VRAM via nvtop/nvidia-smi if available
            # Note: nvtop is interactive. nvidia-smi is better for scripts.
            if command -v nvidia-smi &> /dev/null; then
                VRAM=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits | grep "$PID" | awk '{print $2}')
                VRAM=${VRAM:-0}
            else
                VRAM="N/A"
            fi
            
            echo "$TIMESTAMP, $PID, $STATS, $VRAM" >> "$LOG_FILE"
        done
    fi
    
    sleep $INTERVAL
done

echo "Monitoring complete."
