\# AUDIO/VIDEO EXTRACTOR FROM VIDEOS



\*\*Version 1.0 by ADPHouse\*\*



A Windows-based Python utility for batch processing video files and extracting their original audio streams using \*\*FFmpeg\*\* and \*\*FFprobe\*\*.



The application is designed to be portable: all required working folders are automatically created \*\*in the same directory where `Extract\_Audio.py` is located\*\*.



\---



\## 1. Overview



\*\*Audio/Video Extractor From Videos\*\* is a non-destructive media utility designed for fast and lossless audio extraction from video files.



The current Version 1.0 provides:



\* Automatic application-folder creation

\* Automatic FFmpeg/FFprobe detection

\* Optional FFmpeg installation through Windows `winget`

\* Explicit user permission before FFmpeg installation

\* Batch video processing

\* Recursive folder scanning

\* Lossless audio stream copying

\* Automatic audio output extension selection

\* Existing-file detection and skipping

\* Audio-stream detection

\* Metadata preservation

\* JSON processing logs

\* Detailed console reporting

\* Error handling

\* Non-destructive source processing



The primary operation is \*\*audio extraction\*\*, while the application structure also creates an `Extracted Video` directory for future video-extraction functionality.



\---



\# 2. Core Principle



The application is an \*\*extractor\*\*, not an audio converter.



Its primary FFmpeg operation is:



```text

\-vn

\-c:a copy

```



\### `-vn`



Removes the video stream from the output.



\### `-c:a copy`



Copies the original audio stream without re-encoding it.



Therefore, the application does not intentionally perform an additional lossy compression step.



For example:



```text

MP4

&#x20;└── AAC audio

&#x20;      ↓

&#x20;    Extract

&#x20;      ↓

M4A containing the original AAC stream

```



Or:



```text

WEBM

&#x20;└── Opus audio

&#x20;      ↓

&#x20;    Extract

&#x20;      ↓

OPUS containing the original Opus stream

```



\---



\# 3. Version



```text

Application : AUDIO/VIDEO EXTRACTOR FROM VIDEOS

Version     : 1.0

Author      : ADPHouse

Platform    : Windows

Language    : Python

Media Tool  : FFmpeg

Media Probe : FFprobe

```



\---



\# 4. Requirements



\## Operating System



The application is designed for:



\* Windows 10

\* Windows 11



\## Required Software



The application requires:



\* Python

\* FFmpeg

\* FFprobe



Python is required to execute the application itself.



FFmpeg and FFprobe are used for media processing.



\---



\# 5. Python Requirement



Python must already be installed because `Extract\_Audio.py` is a Python application.



Check Python:



```powershell

python --version

```



or:



```powershell

py --version

```



If Python is not installed, install Python separately before running the application.



The application does not attempt to bootstrap Python.



\---



\# 6. FFmpeg Requirement



The application requires:



```text

ffmpeg.exe

ffprobe.exe

```



It first checks whether both programs are available.



Run manually to verify:



```powershell

ffmpeg -version

```



and:



```powershell

ffprobe -version

```



If they are available, the application continues normally.



\---



\# 7. Automatic FFmpeg Installation



If FFmpeg is not detected, the application checks whether Windows `winget` is available.



Check:



```powershell

winget --version

```



If `winget` is available, the application can request installation of:



```text

Gyan.FFmpeg

```



The application does \*\*not silently install FFmpeg\*\*.



It displays a permission prompt similar to:



```text

FFmpeg is not installed.



Continue? \[Y/N]:

```



Only after the user chooses `Y` does the application execute the `winget` installation request.



Windows may additionally display its own permission or installation prompt.



\---



\# 8. Security and Permission Model



The application follows a user-consent approach for software installation.



\### It does:



\* Check whether FFmpeg exists

\* Check whether FFprobe exists

\* Check whether `winget` exists

\* Ask the user before requesting FFmpeg installation

\* Verify FFmpeg after installation



\### It does not:



\* Silently install FFmpeg

\* Automatically download arbitrary executables

\* Modify the original video files

\* Delete source videos

\* Upload videos

\* Download media from the internet

\* Require a third-party Python package for its core operation



The FFmpeg installation path uses Windows `winget` rather than directly embedding an arbitrary download URL into the Python program.



\---



\# 9. Portable Folder Structure



One of the most important features of Version 1.0 is that the application does \*\*not use a hard-coded drive or folder\*\*.



The application determines its own location using:



```python

BASE\_FOLDER = Path(\_\_file\_\_).resolve().parent

```



Therefore, if the application is located at:



```text

D:\\ADPHouse\\Audio Tool\\Extract\_Audio.py

```



the application automatically uses:



```text

D:\\ADPHouse\\Audio Tool\\

```



as its base directory.



\---



\# 10. Automatic Folder Creation



The application automatically creates:



```text

Videos

Extracted Audio

Extracted Video

Logs

```



Example:



```text

Audio Tool\\

│

├── Extract\_Audio.py

│

├── Videos\\

│

├── Extracted Audio\\

│

├── Extracted Video\\

│

└── Logs\\

```



No manual folder setup is required.



\---



\# 11. Folder Descriptions



\## `Videos`



Input directory.



Place source videos here.



Example:



```text

Videos\\

├── Rain.mp4

├── Ocean.webm

├── Music.mkv

└── Nature.mov

```



\---



\## `Extracted Audio`



Output directory for extracted audio.



Example:



```text

Extracted Audio\\

├── Rain.m4a

├── Ocean.opus

├── Music.flac

└── Nature.mka

```



\---



\## `Extracted Video`



Reserved for video-extraction functionality.



Version 1.0 creates this folder, but the current processing workflow is focused on audio extraction.



\---



\## `Logs`



Contains JSON processing reports.



Example:



```text

Logs\\

└── extraction\_2026-08-18\_16-30-25.json

```



\---



\# 12. Supported Video Formats



The application scans for the following extensions:



```text

.mp4

.mkv

.avi

.mov

.webm

.flv

.wmv

.mpeg

.mpg

.m4v

.ts

.mts

.m2ts

```



File-extension matching is case-insensitive.



Therefore:



```text

VIDEO.MP4

video.mp4

Video.Mp4

```



are all recognized.



\---



\# 13. Recursive Scanning



Recursive scanning is enabled by default:



```python

RECURSIVE\_SCAN = True

```



This means the application searches inside subdirectories.



For example:



```text

Videos\\

│

├── Rain\\

│   ├── Rain1.mp4

│   └── Rain2.mp4

│

├── Ocean\\

│   ├── Ocean1.webm

│   └── Ocean2.webm

│

└── Nature\\

&#x20;   └── Forest.mkv

```



All supported videos can be discovered automatically.



The corresponding structure is preserved in the output:



```text

Extracted Audio\\

│

├── Rain\\

│   ├── Rain1.m4a

│   └── Rain2.m4a

│

├── Ocean\\

│   ├── Ocean1.opus

│   └── Ocean2.opus

│

└── Nature\\

&#x20;   └── Forest.mka

```



\---



\# 14. Audio Detection



Before extracting a video, the application uses FFprobe to inspect the first audio stream:



```text

a:0

```



It retrieves information including:



\* Audio codec

\* Codec description

\* Sample rate

\* Number of channels

\* Channel layout

\* Bitrate

\* Duration



If no audio stream is found, the application reports:



```text

NO AUDIO STREAM

```



and moves to the next video.



\---



\# 15. Automatic Output Format



The application selects an output extension based on the detected audio codec.



| Codec         | Output Extension |

| ------------- | ---------------- |

| AAC           | `.m4a`           |

| ALAC          | `.m4a`           |

| MP3           | `.mp3`           |

| Opus          | `.opus`          |

| Vorbis        | `.ogg`           |

| FLAC          | `.flac`          |

| AC-3          | `.ac3`           |

| E-AC-3        | `.eac3`          |

| DTS           | `.dts`           |

| PCM           | `.wav`           |

| Other/unknown | `.mka`           |



The purpose is to avoid unnecessary audio transcoding.



\---



\# 16. Lossless Stream Copy



The application uses:



```text

\-c:a copy

```



This instructs FFmpeg to copy the audio stream instead of encoding it again.



For example:



```text

Original:



AAC 256 kbps

&#x20;     ↓

\-c:a copy

&#x20;     ↓

AAC 256 kbps

```



The application is not intentionally performing:



```text

AAC → MP3

```



or:



```text

FLAC → AAC

```



conversions.



\---



\# 17. Important Meaning of "Lossless"



The term \*\*lossless extraction\*\* means that the application does not re-encode the existing audio stream during extraction.



It does \*\*not\*\* mean that the original audio was necessarily lossless.



For example:



```text

Original video

└── AAC 128 kbps

```



will produce:



```text

Extracted audio

└── AAC 128 kbps

```



The AAC remains lossy because AAC itself may be a lossy codec, but the extraction does not add another encoding generation.



Likewise:



```text

Original video

└── FLAC

```



can be extracted without re-encoding the FLAC stream.



\---



\# 18. Metadata Preservation



The FFmpeg command uses:



```text

\-map\_metadata 0

```



to preserve source metadata where supported by the destination container.



Metadata support varies depending on the source and output format.



\---



\# 19. Existing File Protection



The application uses:



```python

SKIP\_EXISTING = True

```



By default, if the expected output already exists and has a non-zero file size, the application skips that file.



Example:



```text

Videos\\

└── Rain.mp4



Extracted Audio\\

└── Rain.m4a

```



On the next run:



```text

Rain.mp4

&#x20;    ↓

Rain.m4a already exists

&#x20;    ↓

SKIPPED

```



This is useful for large batch operations.



\---



\# 20. Interrupted Processing



If processing is interrupted, the program can be started again.



Files that were successfully extracted and still exist in the output directory are skipped.



Remaining files are processed.



This allows the application to function as a resumable batch workflow.



\---



\# 21. Non-Destructive Processing



The original videos are not deleted.



The application reads from:



```text

Videos\\

```



and writes extracted audio to:



```text

Extracted Audio\\

```



The source video remains untouched.



\---



\# 22. Failed Extraction Handling



If FFmpeg fails to process a file, the application reports:



```text

✗ FAILED

```



The FFmpeg error message is displayed.



If an incomplete output file was created during the failed operation, the application attempts to remove that incomplete output.



The source video is left untouched.



\---



\# 23. JSON Logging



Every processing run generates a JSON log.



Example:



```text

Logs\\

└── extraction\_2026-08-18\_16-30-25.json

```



The log contains:



```text

Application name

Version

Author

Timestamp

Application folder

Source folder

Audio output folder

Total files

Completed files

Skipped files

Files without audio

Failed files

Individual processing results

```



For individual files, the log can contain:



```text

Source path

Output path

Status

Codec

Codec description

Sample rate

Channels

Channel layout

Bitrate

Duration

Output size

Error information

```



\---



\# 24. Example JSON Structure



A simplified log looks like:



```json

{

&#x20;   "application": "AUDIO/VIDEO EXTRACTOR FROM VIDEOS",

&#x20;   "version": "1.0",

&#x20;   "author": "ADPHouse",

&#x20;   "timestamp": "2026-08-18\_16-30-25",

&#x20;   "application\_folder": "D:\\\\Audio Tool",

&#x20;   "source\_folder": "D:\\\\Audio Tool\\\\Videos",

&#x20;   "audio\_output\_folder": "D:\\\\Audio Tool\\\\Extracted Audio",

&#x20;   "total\_files": 10,

&#x20;   "completed": 8,

&#x20;   "skipped": 1,

&#x20;   "no\_audio": 0,

&#x20;   "failed": 1,

&#x20;   "results": \[]

}

```



The actual log contains the individual file results as well.



\---



\# 25. Console Workflow



When launched, the application performs three major stages.



```text

\[1/3] Checking application folders...



\[2/3] Checking required software...



\[3/3] Searching for videos...

```



Then it processes the discovered videos.



\---



\# 26. Example Startup



```text

========================================================================

&#x20;            AUDIO/VIDEO EXTRACTOR FROM VIDEOS

&#x20;                   Version 1.0 by ADPHouse

========================================================================



Fast • Lossless • Smart Batch Extraction



\[1/3] Checking application folders...



✓ Exists: Videos

✓ Exists: Extracted Audio

✓ Exists: Extracted Video

✓ Exists: Logs



\[2/3] Checking required software...



✓ FFmpeg detected.

✓ FFprobe detected.



\[3/3] Searching for videos...



✓ Found 25 video(s).

```



\---



\# 27. Example Processing



```text

\------------------------------------------------------------------------



\[1/25] Rain.mp4

&#x20;  ✓ DONE

&#x20;  Codec    : aac

&#x20;  Duration : 01:00:00

&#x20;  Output   : D:\\Audio Tool\\Extracted Audio\\Rain.m4a

&#x20;  Size     : 82.41 MB



\[2/25] Ocean.webm

&#x20;  ✓ DONE

&#x20;  Codec    : opus

&#x20;  Duration : 00:45:12

&#x20;  Output   : D:\\Audio Tool\\Extracted Audio\\Ocean.opus

&#x20;  Size     : 51.23 MB



\[3/25] Music.mkv

&#x20;  → SKIPPED — already exists



\[4/25] Silent.mp4

&#x20;  ! NO AUDIO STREAM

```



\---



\# 28. Final Summary



At the end of processing:



```text

========================================================================

&#x20;                             COMPLETE

========================================================================



Total files : 25

Completed   : 22

Skipped     : 1

No Audio    : 1

Failed      : 1



Audio folder:

&#x20; D:\\Audio Tool\\Extracted Audio



Log file:

&#x20; D:\\Audio Tool\\Logs\\extraction\_2026-08-18\_16-30-25.json



========================================================================

```



\---



\# 29. Installation



\## Step 1 — Place the Script



Place:



```text

Extract\_Audio.py

```



inside any folder where you want the application to operate.



For example:



```text

D:\\ADPHouse\\Audio Extractor\\

└── Extract\_Audio.py

```



The folder does not need to have a particular name.



\---



\## Step 2 — Run the Script



Open PowerShell in that folder:



```powershell

cd "D:\\ADPHouse\\Audio Extractor"

```



Run:



```powershell

python Extract\_Audio.py

```



Alternatively:



```powershell

py Extract\_Audio.py

```



\---



\## Step 3 — Add Videos



After the first launch, the application creates:



```text

Videos\\

```



Place your videos there.



\---



\## Step 4 — Run Again



Run:



```powershell

python Extract\_Audio.py

```



The application detects the videos and begins extraction.



\---



\# 30. Moving the Application



The application can be moved to another folder.



For example:



```text

D:\\Audio Tool\\

```



can be moved to:



```text

E:\\Media Tools\\

```



The application automatically uses the new directory as its base folder.



No Python code needs to be changed.



\---



\# 31. Example Portable Setup



```text

USB Drive\\

│

└── Audio Extractor\\

&#x20;   │

&#x20;   ├── Extract\_Audio.py

&#x20;   │

&#x20;   ├── Videos\\

&#x20;   │

&#x20;   ├── Extracted Audio\\

&#x20;   │

&#x20;   ├── Extracted Video\\

&#x20;   │

&#x20;   └── Logs\\

```



The same structure can be used on another Windows drive, subject to Windows permissions and availability of Python/FFmpeg.



\---



\# 32. Configuration



The main configuration options are near the top of the Python file.



\## Recursive Scanning



```python

RECURSIVE\_SCAN = True

```



When enabled, subfolders are scanned.



To disable recursive scanning:



```python

RECURSIVE\_SCAN = False

```



\---



\## Skip Existing Files



Default:



```python

SKIP\_EXISTING = True

```



This prevents unnecessary reprocessing.



If changed to:



```python

SKIP\_EXISTING = False

```



the application will attempt to process existing outputs again.



\---



\# 33. Changing the Supported Formats



The supported input extensions are defined in:



```python

VIDEO\_EXTENSIONS = {

&#x20;   ".mp4",

&#x20;   ".mkv",

&#x20;   ".avi",

&#x20;   ".mov",

&#x20;   ".webm",

&#x20;   ".flv",

&#x20;   ".wmv",

&#x20;   ".mpeg",

&#x20;   ".mpg",

&#x20;   ".m4v",

&#x20;   ".ts",

&#x20;   ".mts",

&#x20;   ".m2ts",

}

```



Additional formats can be added if required.



For example:



```python

".3gp",

```



could be added to the set.



Whether FFmpeg can actually process the file depends on the media inside the container.



\---



\# 34. FFmpeg Command Used for Extraction



The core extraction operation is equivalent to:



```powershell

ffmpeg -hide\_banner -loglevel error -y -i "input.mp4" -map 0:a:0 -vn -c:a copy -map\_metadata 0 "output.m4a"

```



\### Important options



| Option            | Purpose                                      |

| ----------------- | -------------------------------------------- |

| `-hide\_banner`    | Reduces unnecessary FFmpeg startup output    |

| `-loglevel error` | Shows important FFmpeg errors                |

| `-y`              | Allows the program to manage the output file |

| `-i`              | Specifies the input video                    |

| `-map 0:a:0`      | Selects the first audio stream               |

| `-vn`             | Removes video from the output                |

| `-c:a copy`       | Copies audio without re-encoding             |

| `-map\_metadata 0` | Copies source metadata where supported       |



\---



\# 35. Why FFprobe Is Used



FFmpeg can perform the extraction itself, but FFprobe provides structured information about the source media.



The application uses FFprobe to determine:



```text

Audio exists?

&#x20;       ↓

Codec?

&#x20;       ↓

Sample rate?

&#x20;       ↓

Channels?

&#x20;       ↓

Bitrate?

&#x20;       ↓

Duration?

&#x20;       ↓

Choose output extension

```



This allows the application to make a more informed output-format decision.



\---



\# 36. Multiple Audio Tracks



Version 1.0 explicitly maps:



```text

0:a:0

```



which means it processes the \*\*first audio stream\*\*.



For a video containing:



```text

Audio 1 — English

Audio 2 — Hindi

Audio 3 — Commentary

```



Version 1.0 extracts:



```text

Audio 1

```



only.



Multi-track extraction is not implemented in this version.



\---



\# 37. Subtitles



Version 1.0 is focused on audio extraction.



It does not separately extract:



\* SRT subtitles

\* ASS subtitles

\* WebVTT subtitles

\* Embedded subtitle streams



Subtitle extraction can be added as a future feature.



\---



\# 38. Video Extraction



The application creates:



```text

Extracted Video\\

```



but Version 1.0 primarily implements audio extraction.



The directory provides a predefined location for future video-stream extraction functionality.



\---



\# 39. What Version 1.0 Does Not Do



Version 1.0 does not intentionally perform:



\* Audio re-encoding

\* Audio normalization

\* Noise reduction

\* Volume boosting

\* Sample-rate conversion

\* Bitrate conversion

\* Audio enhancement

\* Video transcoding

\* Video compression

\* Subtitle extraction

\* Multi-audio-track extraction

\* Internet downloading

\* YouTube downloading

\* Social-media downloading

\* Cloud uploading

\* Automatic deletion of source files



The application is intentionally focused on safe, lossless audio-stream extraction.



\---



\# 40. Troubleshooting



\## Problem: Python is not recognized



Try:



```powershell

py --version

```



If that also fails, Python needs to be installed.



\---



\## Problem: FFmpeg is not detected



Run:



```powershell

ffmpeg -version

```



and:



```powershell

ffprobe -version

```



If both fail, the application will attempt to use `winget` if available and after user permission.



\---



\## Problem: `winget` is not available



The application cannot automatically install FFmpeg through its current installation mechanism.



Install FFmpeg manually and make sure:



```text

ffmpeg.exe

ffprobe.exe

```



are accessible through Windows `PATH`.



Then restart the application.



\---



\## Problem: No videos found



Check:



```text

Videos\\

```



and ensure the files have supported extensions.



For example:



```text

Videos\\

└── example.mp4

```



\---



\## Problem: No audio stream



The source video does not contain an audio stream that FFprobe can detect.



The application reports:



```text

! NO AUDIO STREAM

```



\---



\## Problem: Extraction failed



Check the console error and the JSON log.



The log is stored in:



```text

Logs\\

```



The application records the FFmpeg error returned for failed files.



\---



\## Problem: Permission denied



If the application cannot create folders or write files, Windows may be restricting access to the selected directory.



Try placing the application in a directory where the current Windows user has write permission.



For example:



```text

D:\\Tools\\Audio Extractor\\

```



rather than a protected system directory.



\---



\# 41. Data Safety



The application is designed to be non-destructive.



Source:



```text

Videos\\

```



Output:



```text

Extracted Audio\\

```



The original source video is not intentionally modified or deleted.



The application also attempts to remove incomplete output created by a failed extraction rather than leaving a potentially invalid output file behind.



\---



\# 42. Performance



Because audio is copied rather than re-encoded, the extraction process is generally much lighter than transcoding.



Performance depends on:



\* Storage speed

\* Source file size

\* Audio bitrate

\* Number of files

\* Container format

\* File-system performance

\* FFmpeg processing overhead



For very large collections, SSD storage can significantly improve file-access performance.



\---



\# 43. Large Batch Processing



The application is suitable for processing collections containing many files.



For example:



```text

Videos\\

├── 001.mp4

├── 002.mp4

├── 003.mp4

...

├── 500.mp4

```



The application processes the files sequentially.



If processing is interrupted, run the application again.



Existing successful outputs are skipped when:



```python

SKIP\_EXISTING = True

```



\---



\# 44. Recommended Workflow for Large Collections



Use:



```text

Videos\\

```



as the input location.



Do not manually move partially processed files between the source and output directories.



Run the application.



Allow it to complete.



Then inspect:



```text

Extracted Audio\\

```



and:



```text

Logs\\

```



for the final results.



\---



\# 45. Example Complete Directory



After processing:



```text

Audio Extractor\\

│

├── Extract\_Audio.py

│

├── Videos\\

│   ├── Rain\\

│   │   ├── Rain01.mp4

│   │   └── Rain02.mp4

│   │

│   ├── Ocean\\

│   │   └── Ocean01.webm

│   │

│   └── Music\\

│       └── Music01.mkv

│

├── Extracted Audio\\

│   ├── Rain\\

│   │   ├── Rain01.m4a

│   │   └── Rain02.m4a

│   │

│   ├── Ocean\\

│   │   └── Ocean01.opus

│   │

│   └── Music\\

│       └── Music01.flac

│

├── Extracted Video\\

│

└── Logs\\

&#x20;   └── extraction\_2026-08-18\_16-30-25.json

```



\---



\# 46. Design Goals



Version 1.0 is built around these principles:



\### Portable



The application uses its own directory as the base location.



\### Automatic



Required working folders are created automatically.



\### User Controlled



Software installation requires explicit permission.



\### Lossless



Existing audio streams are copied rather than re-encoded.



\### Non-Destructive



Source videos are preserved.



\### Resumable



Existing successful outputs can be skipped.



\### Auditable



Processing information is stored in JSON logs.



\### Scalable



Recursive scanning and batch processing support large collections.



\---



\# 47. Future Development



Potential future versions can extend the architecture with:



\## Audio Features



\* Extract all audio tracks

\* Select a specific audio language

\* Extract by stream index

\* Audio-only batch mode

\* Audio conversion mode

\* MP3 conversion

\* AAC conversion

\* FLAC conversion

\* WAV conversion

\* Audio normalization



\## Video Features



\* Extract video without audio

\* Copy video streams losslessly

\* Select video stream

\* Video codec detection

\* Video metadata extraction



\## Subtitle Features



\* Extract SRT

\* Extract ASS

\* Extract WebVTT

\* Extract all subtitle streams



\## Media Analysis



\* Resolution detection

\* FPS detection

\* HDR detection

\* Bit-depth detection

\* Codec analysis

\* Container analysis

\* Media information reports



\## User Interface



\* Graphical interface

\* Folder selection

\* Drag-and-drop support

\* Progress bar

\* Cancel button

\* Settings panel

\* Processing history



\## Advanced Processing



\* Parallel processing

\* Queue management

\* Automatic retry

\* Duplicate detection

\* Hash verification

\* Detailed media reports



These are potential future capabilities and are \*\*not part of the current Version 1.0 implementation\*\*.



\---



\# 48. License



No software license has been specified for this project.



If the project is published publicly, an appropriate license can be added later.



FFmpeg itself is a separate third-party project and has its own licensing terms. Users should review FFmpeg's licensing information when distributing FFmpeg binaries with this application.



\---



\# 49. Third-Party Software



This application relies on:



```text

Python

FFmpeg

FFprobe

Windows winget

```



FFmpeg/FFprobe are external media-processing tools.



The application does not claim ownership of FFmpeg.



\---



\# 50. Author



```text

ADPHouse

```



Project:



```text

AUDIO/VIDEO EXTRACTOR FROM VIDEOS

```



Version:



```text

1.0

```



\---



\# 51. Quick Start



The shortest setup is:



\### 1. Put the application anywhere



```text

My Tools\\

└── Extract\_Audio.py

```



\### 2. Run it



```powershell

python Extract\_Audio.py

```



\### 3. Put videos into



```text

My Tools\\

└── Videos\\

```



\### 4. Run it again



```powershell

python Extract\_Audio.py

```



\### 5. Get extracted audio from



```text

My Tools\\

└── Extracted Audio\\

```



\### 6. Check processing logs



```text

My Tools\\

└── Logs\\

```



\---



\# 52. One-Line Description



> \*\*A portable Windows Python utility by ADPHouse for fast, non-destructive, lossless batch extraction of audio streams from videos using FFmpeg and FFprobe.\*\*



\---



\# 53. Project Summary



```text

============================================================

AUDIO/VIDEO EXTRACTOR FROM VIDEOS

Version 1.0 by ADPHouse

============================================================



Input:

&#x20;   Videos/



Output:

&#x20;   Extracted Audio/



Future:

&#x20;   Extracted Video/



Logs:

&#x20;   Logs/



Processing:

&#x20;   FFmpeg + FFprobe



Audio mode:

&#x20;   Lossless stream copy



Source files:

&#x20;   Never intentionally modified



Installation:

&#x20;   Automatic FFmpeg detection

&#x20;   Optional winget installation

&#x20;   User permission required



Folder behavior:

&#x20;   Automatically created beside Extract\_Audio.py

============================================================

```



