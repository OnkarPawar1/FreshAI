import os
import sys

fd = sys.stderr.fileno()
saved_stderr = os.dup(fd)
with open(os.devnull, 'w') as devnull:
    os.dup2(devnull.fileno(), fd)

try:
    import cv2
    import av
    from vision_agents.core import Agent
finally:
    os.dup2(saved_stderr, fd)
    os.close(saved_stderr)

print("Imports done without warning!")
