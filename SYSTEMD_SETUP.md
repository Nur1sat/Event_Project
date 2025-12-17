# Systemd Service Setup for JIHClubs

## Installation Instructions

### 1. Copy service file to systemd directory

```bash
sudo cp /root/jihclubs/jihclubs.service /etc/systemd/system/
```

### 2. Reload systemd daemon

```bash
sudo systemctl daemon-reload
```

### 3. Enable service to start on boot (optional)

```bash
sudo systemctl enable jihclubs.service
```

### 4. Start the service

```bash
sudo systemctl start jihclubs.service
```

### 5. Check service status

```bash
sudo systemctl status jihclubs.service
```

## Service Management Commands

### Start service
```bash
sudo systemctl start jihclubs
```

### Stop service
```bash
sudo systemctl stop jihclubs
```

### Restart service
```bash
sudo systemctl restart jihclubs
```

### View logs
```bash
sudo journalctl -u jihclubs.service -f
```

### View recent logs
```bash
sudo journalctl -u jihclubs.service -n 100
```

## Service File Details

- **Service Name:** `jihclubs.service`
- **Working Directory:** `/root/jihclubs`
- **ExecStart:** `/root/jihclubs/start-all.sh`
- **Restart Policy:** Always restart on failure (5 second delay)
- **User:** root

## Logs

- **Systemd logs:** `sudo journalctl -u jihclubs.service`
- **Backend logs:** `/root/jihclubs/backend.log`
- **Frontend logs:** `/root/jihclubs/frontend.log`

## Troubleshooting

### Check if service is running
```bash
sudo systemctl is-active jihclubs
```

### Check service status
```bash
sudo systemctl status jihclubs
```

### View error logs
```bash
sudo journalctl -u jihclubs.service -p err
```

### Check if ports are in use
```bash
sudo lsof -i :8007  # Backend
sudo lsof -i :5176  # Frontend
```

### Manual stop (if service won't stop)
```bash
sudo systemctl stop jihclubs
/root/jihclubs/stop-all.sh
```

