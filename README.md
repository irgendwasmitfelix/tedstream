# YouTube 24/7 Live Stream - Kraken Bot Logs

This setup streams your Kraken trading bot logs 24/7 to YouTube.

## Stream Details
- **RTMP URL**: rtmp://a.rtmp.youtube.com/live2
- **Stream Key**: d56x-qhfs-q29r-7s53-85k5
- **Resolution**: 1280x720 @ 15fps
- **Bitrate**: 2000kbps
- **Log File**: ~/.openclaw/workspace/kraken_bot/bot.log

## Current Status
✅ Stream is **RUNNING** in the background!

## Files
- `stream.sh` - Main streaming script
- `monitor.sh` - Check stream status
- `install-service.sh` - Install as systemd service (auto-restart + boot startup)
- `youtube-stream.service` - Systemd service configuration
- `stream.log` - Stream output logs

## Usage

### Check Stream Status
```bash
./monitor.sh
```

### View Live Stream Logs
```bash
tail -f stream.log
```

### Manual Control
```bash
# Stop the stream
kill $(pgrep -f 'stream.sh' | head -1)

# Start the stream
./stream.sh &

# Or run in foreground (Ctrl+C to stop)
./stream.sh
```

### Install as System Service (Recommended)
This makes the stream automatically restart if it crashes and start on boot:

```bash
./install-service.sh

# Then control with:
sudo systemctl start youtube-stream   # Start
sudo systemctl stop youtube-stream    # Stop
sudo systemctl restart youtube-stream # Restart
sudo systemctl status youtube-stream  # Check status
```

## What's Being Streamed
The stream displays:
- Current timestamp
- Last 15 lines of bot.log
- Auto-updates every 2 seconds

## Troubleshooting

### Stream not working?
1. Check logs: `tail -50 stream.log`
2. Verify YouTube accepts the stream key
3. Check bot.log exists: `ls -la ~/.openclaw/workspace/kraken_bot/bot.log`
4. Verify ffmpeg is running: `ps aux | grep ffmpeg`

### High CPU usage?
The current settings are optimized for Raspberry Pi with:
- ultrafast preset
- 15fps (lower than standard 30fps)
- 2000kbps bitrate

You can adjust these in `stream.sh` if needed.

### Stream quality
- The stream updates every 2 seconds
- Text is displayed in white on black background
- Font: DejaVu Sans Mono (monospace)

## Notes
- The stream runs as a detached background process
- It will continue even if you close the terminal
- Stream restarts automatically if installed as systemd service
- All output is logged to `stream.log`
