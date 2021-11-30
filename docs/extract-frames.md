---
title: Extract frames from videos
---

The computer vision models are trained on video frames.
Therefore we have to extract frames from the source video files.

# Limits on files per directory

It's better for many systems to not have too many files in a single directory.
ALICE documentation mentions

> 100s, not 1000s

as a rule of thumb.
Our scripts try to work with these limitations.

# Using Python and OpenCV

This appears to be slower.

# Using Bash and ffmpeg

This appears to be faster.
