

TIME_MODE_SECONDS = 'seconds'
TIME_MODE_FRAMES = 'frames'
_next_time_mode_map = {
    TIME_MODE_SECONDS: TIME_MODE_FRAMES,
    TIME_MODE_FRAMES: TIME_MODE_SECONDS
}

def next_time_mode(mode=None):
    return _next_time_mode_map.get(mode, TIME_MODE_FRAMES)

def format_time(time, fps, mode):
    if mode == TIME_MODE_FRAMES:
        frames = int(time * fps + 0.1)
        seconds, frames = divmod(frames, fps)
        minutes, seconds = divmod(seconds, 60)
        return '%02d:%02d:%02d' % (minutes, seconds, frames)
    elif mode == TIME_MODE_SECONDS:
        return '%.2f' % time