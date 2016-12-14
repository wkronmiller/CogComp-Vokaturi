"""
Shared configuration properties for project components
"""
import sys

# Audio sample rate
RATE = 44100
# Audio sample width
CHUNK = 65536

# Rabbit connection settings
RABBIT_HOST = sys.argv[1]
RABBIT_PORT = int(sys.argv[2])
