import asyncio
import numpy as np
from vision_agents.plugins.getstream.stream_edge_transport import PcmData

async def main():
    # Make a tiny chunk of 24k sine wave (100ms)
    t = np.linspace(0, 0.1, 2400, endpoint=False)
    wave = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
    
    pcm = PcmData.from_bytes(wave.tobytes(), sample_rate=24000)
    print("Original PcmData duration:", pcm.duration)
    
    resampled = pcm.resample(48000, target_channels=2)
    print("Resampled PcmData duration:", resampled.duration)
    
    bytes_data = resampled.to_bytes()
    print("Resampled bytes length:", len(bytes_data))
    
    # Are the bytes all zeros?
    arr = np.frombuffer(bytes_data, dtype=np.int16)
    print("Max amplitude:", np.max(np.abs(arr)))

if __name__ == "__main__":
    asyncio.run(main())
