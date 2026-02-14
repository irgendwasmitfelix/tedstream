#!/bin/bash
# Monitor script for YouTube stream

echo "=== YouTube Stream Status ==="
echo ""
echo "Stream processes:"
ps aux | grep -E "(stream\.sh|ffmpeg)" | grep -v grep | awk '{print $2, $11, $12, $13}' | head -5
echo ""
echo "Latest stream log (last 15 lines):"
tail -15 stream.log 2>/dev/null || echo "No log file yet"
echo ""
echo "Current content being streamed:"
echo "---"
cat /tmp/youtube_stream/stream_text.txt 2>/dev/null || echo "Content not generated yet"
echo "---"
echo ""
echo "To stop the stream: kill \$(pgrep -f 'stream.sh' | head -1)"
echo "To view live logs: tail -f stream.log"
