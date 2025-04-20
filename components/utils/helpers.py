def format_lap_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{secs:02d}.{millis:03d}"
