import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


# ============================================================
# AUDIO/VIDEO EXTRACTOR FROM VIDEOS
# Version 1.0 by (ADPHouse)
# ============================================================

APP_NAME = "AUDIO/VIDEO EXTRACTOR FROM VIDEOS"
APP_VERSION = "1.0"
AUTHOR = "(ADPHouse)"


# ============================================================
# APPLICATION LOCATION
# ============================================================
# All folders are created beside this Python script.
#
# Example:
#
# D:\My Tools\
#     Extract_Audio.py
#     Videos\
#     Extracted Audio\
#     Extracted Video\
#     Logs\
#
# ============================================================

BASE_FOLDER = Path(__file__).resolve().parent

VIDEO_FOLDER = BASE_FOLDER / "Videos"
AUDIO_FOLDER = BASE_FOLDER / "Extracted Audio"
EXTRACTED_VIDEO_FOLDER = BASE_FOLDER / "Extracted Video"
LOG_FOLDER = BASE_FOLDER / "Logs"


# ============================================================
# SETTINGS
# ============================================================

RECURSIVE_SCAN = True

# If True, an existing output file will not be processed again.
SKIP_EXISTING = True

# Supported input video formats.
VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm",
    ".flv",
    ".wmv",
    ".mpeg",
    ".mpg",
    ".m4v",
    ".ts",
    ".mts",
    ".m2ts",
}


# ============================================================
# CONSOLE COLORS
# ============================================================

class Color:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"


# ============================================================
# DISPLAY
# ============================================================

def print_header():
    print()
    print("=" * 72)
    print(APP_NAME.center(72))
    print(f"Version {APP_VERSION} by {AUTHOR}".center(72))
    print("=" * 72)
    print()
    print("Fast • Lossless • Smart Batch Extraction")
    print()


def ask_permission(message):
    print()
    print(Color.YELLOW + message + Color.RESET)
    print()

    while True:
        answer = input("Continue? [Y/N]: ").strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter Y or N.")


# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

def create_required_folders():

    folders = [
        VIDEO_FOLDER,
        AUDIO_FOLDER,
        EXTRACTED_VIDEO_FOLDER,
        LOG_FOLDER,
    ]

    print("Checking application folders...")
    print()

    for folder in folders:

        try:

            if folder.exists():

                if folder.is_dir():

                    print(
                        Color.GREEN +
                        f"✓ Exists: {folder.name}" +
                        Color.RESET
                    )

                else:

                    print(
                        Color.RED +
                        f"✗ Path exists but is not a folder: {folder}" +
                        Color.RESET
                    )

                    return False

            else:

                folder.mkdir(
                    parents=True,
                    exist_ok=True
                )

                print(
                    Color.GREEN +
                    f"✓ Created: {folder.name}" +
                    Color.RESET
                )

        except PermissionError:

            print()
            print(
                Color.RED +
                "Permission denied:" +
                Color.RESET
            )

            print(folder)

            return False

        except OSError as error:

            print()
            print(
                Color.RED +
                f"Could not create {folder}: {error}" +
                Color.RESET
            )

            return False

    return True


# ============================================================
# PROGRAM DETECTION
# ============================================================

def find_program(program):

    return shutil.which(program)


def ffmpeg_available():

    return (
        find_program("ffmpeg") is not None
        and
        find_program("ffprobe") is not None
    )


def winget_available():

    return find_program("winget") is not None


# ============================================================
# REFRESH WINDOWS PATH
# ============================================================

def refresh_path():

    if os.name != "nt":
        return

    try:

        import ctypes

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A

        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            0x0002,
            5000,
            None,
        )

    except Exception:
        pass


# ============================================================
# SEARCH COMMON FFMPEG LOCATIONS
# ============================================================

def search_for_ffmpeg():

    if ffmpeg_available():
        return True

    possible_roots = []

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        possible_roots.append(
            Path(local_app_data)
        )

    program_files = os.environ.get("ProgramFiles")

    if program_files:
        possible_roots.append(
            Path(program_files)
        )

    program_files_x86 = os.environ.get(
        "ProgramFiles(x86)"
    )

    if program_files_x86:
        possible_roots.append(
            Path(program_files_x86)
        )

    possible_roots.extend([
        Path(r"C:\ffmpeg"),
        Path(r"C:\ProgramData"),
    ])

    for root in possible_roots:

        if not root.exists():
            continue

        try:

            ffmpeg_matches = list(
                root.rglob("ffmpeg.exe")
            )

            for ffmpeg_path in ffmpeg_matches:

                ffmpeg_dir = ffmpeg_path.parent

                ffprobe_path = (
                    ffmpeg_dir / "ffprobe.exe"
                )

                if ffprobe_path.exists():

                    current_path = os.environ.get(
                        "PATH",
                        ""
                    )

                    if str(ffmpeg_dir) not in current_path:

                        os.environ["PATH"] = (
                            str(ffmpeg_dir)
                            + os.pathsep
                            + current_path
                        )

                    return ffmpeg_available()

        except (
            PermissionError,
            OSError,
        ):
            continue

    return False


# ============================================================
# INSTALL FFMPEG USING WINGET
# ============================================================

def install_ffmpeg():

    if not winget_available():

        print()
        print(
            Color.RED +
            "Windows Package Manager (winget) was not found." +
            Color.RESET
        )

        print()
        print(
            "Automatic FFmpeg installation is unavailable."
        )

        print(
            "Please install FFmpeg manually and make sure"
        )

        print(
            "ffmpeg.exe and ffprobe.exe are available in PATH."
        )

        return False

    print()
    print("=" * 72)
    print("FFMPEG INSTALLATION")
    print("=" * 72)
    print()

    print("The following package will be requested:")
    print()
    print("  Gyan.FFmpeg")
    print()

    print(
        "Windows may display its own installation or "
        "administrator permission prompt."
    )

    if not ask_permission(
        "FFmpeg is not installed. "
        "Allow the program to request FFmpeg installation?"
    ):

        print()
        print(
            Color.YELLOW +
            "FFmpeg installation cancelled." +
            Color.RESET
        )

        return False

    command = [
        "winget",
        "install",
        "--id",
        "Gyan.FFmpeg",
        "--exact",
        "--source",
        "winget",
    ]

    print()
    print(
        Color.CYAN +
        "Starting FFmpeg installation..." +
        Color.RESET
    )

    try:

        result = subprocess.run(
            command,
            check=False
        )

    except OSError as error:

        print()
        print(
            Color.RED +
            f"Could not start winget: {error}" +
            Color.RESET
        )

        return False

    if result.returncode != 0:

        print()
        print(
            Color.RED +
            "FFmpeg installation was not completed." +
            Color.RESET
        )

        print(
            f"winget exit code: {result.returncode}"
        )

        return False

    print()
    print(
        Color.GREEN +
        "✓ FFmpeg installation completed." +
        Color.RESET
    )

    return True


# ============================================================
# ENSURE FFMPEG
# ============================================================

def ensure_ffmpeg():

    print()
    print("Checking required software...")
    print()

    refresh_path()

    if ffmpeg_available():

        print(
            Color.GREEN +
            "✓ FFmpeg detected." +
            Color.RESET
        )

        print(
            Color.GREEN +
            "✓ FFprobe detected." +
            Color.RESET
        )

        return True

    # Search common locations before installing.
    if search_for_ffmpeg():

        print(
            Color.GREEN +
            "✓ FFmpeg detected." +
            Color.RESET
        )

        print(
            Color.GREEN +
            "✓ FFprobe detected." +
            Color.RESET
        )

        return True

    print(
        Color.YELLOW +
        "FFmpeg and/or FFprobe were not found." +
        Color.RESET
    )

    if not winget_available():

        print()
        print(
            Color.RED +
            "winget is not available." +
            Color.RESET
        )

        print()
        print(
            "Install FFmpeg manually and restart this program."
        )

        return False

    if not install_ffmpeg():

        return False

    print()
    print("Verifying FFmpeg...")

    time.sleep(2)

    refresh_path()

    if ffmpeg_available():

        print(
            Color.GREEN +
            "✓ FFmpeg is ready." +
            Color.RESET
        )

        print(
            Color.GREEN +
            "✓ FFprobe is ready." +
            Color.RESET
        )

        return True

    # Search again.
    if search_for_ffmpeg():

        print(
            Color.GREEN +
            "✓ FFmpeg is ready." +
            Color.RESET
        )

        print(
            Color.GREEN +
            "✓ FFprobe is ready." +
            Color.RESET
        )

        return True

    print()
    print(
        Color.YELLOW +
        "FFmpeg was installed, but this running Python "
        "process cannot see it yet." +
        Color.RESET
    )

    print()
    print(
        "Please close this window, open a new PowerShell "
        "window, and run the script again."
    )

    return False


# ============================================================
# FIND VIDEO FILES
# ============================================================

def find_video_files():

    if RECURSIVE_SCAN:

        files = VIDEO_FOLDER.rglob("*")

    else:

        files = VIDEO_FOLDER.glob("*")

    return sorted(
        file
        for file in files
        if (
            file.is_file()
            and
            file.suffix.lower() in VIDEO_EXTENSIONS
        )
    )


# ============================================================
# GET AUDIO INFORMATION
# ============================================================

def get_audio_info(video_path):

    command = [
        "ffprobe",
        "-v",
        "error",

        "-select_streams",
        "a:0",

        "-show_entries",
        (
            "stream="
            "codec_name,"
            "codec_long_name,"
            "sample_rate,"
            "channels,"
            "channel_layout,"
            "bit_rate,"
            "duration"
        ),

        "-of",
        "json",

        str(video_path),
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    except OSError:

        return None

    if result.returncode != 0:

        return None

    try:

        data = json.loads(
            result.stdout
        )

    except json.JSONDecodeError:

        return None

    streams = data.get(
        "streams",
        []
    )

    if not streams:

        return None

    return streams[0]


# ============================================================
# SELECT OUTPUT FORMAT
# ============================================================

def choose_output_extension(codec):

    codec = (
        codec or ""
    ).lower()

    codec_extensions = {

        "aac": ".m4a",
        "alac": ".m4a",

        "mp3": ".mp3",

        "opus": ".opus",

        "vorbis": ".ogg",

        "flac": ".flac",

        "ac3": ".ac3",

        "eac3": ".eac3",

        "dts": ".dts",

        "pcm_s16le": ".wav",
        "pcm_s16be": ".wav",
        "pcm_s24le": ".wav",
        "pcm_s24be": ".wav",
        "pcm_s32le": ".wav",
        "pcm_s32be": ".wav",
        "pcm_f32le": ".wav",
        "pcm_f32be": ".wav",
        "pcm_f64le": ".wav",
        "pcm_f64be": ".wav",
    }

    return codec_extensions.get(
        codec,
        ".mka"
    )


# ============================================================
# FORMAT FILE SIZE
# ============================================================

def format_size(size):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    value = float(size)

    for unit in units:

        if value < 1024:

            return (
                f"{value:.2f} "
                f"{unit}"
            )

        value /= 1024

    return f"{value:.2f} PB"


# ============================================================
# FORMAT DURATION
# ============================================================

def format_duration(value):

    try:

        total_seconds = int(
            float(value)
        )

    except (
        TypeError,
        ValueError,
    ):

        return "Unknown"

    hours = (
        total_seconds // 3600
    )

    minutes = (
        total_seconds % 3600
    ) // 60

    seconds = (
        total_seconds % 60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


# ============================================================
# EXTRACT AUDIO
# ============================================================

def extract_audio(video_path):

    relative_path = (
        video_path.relative_to(
            VIDEO_FOLDER
        )
    )

    output_directory = (
        AUDIO_FOLDER /
        relative_path.parent
    )

    try:

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    except OSError as error:

        return {
            "status": "FAILED",
            "source": str(video_path),
            "error": (
                f"Could not create output folder: "
                f"{error}"
            ),
        }

    # --------------------------------------------------------
    # Detect audio
    # --------------------------------------------------------

    audio_info = get_audio_info(
        video_path
    )

    if not audio_info:

        return {
            "status": "NO_AUDIO",
            "source": str(video_path),
            "message": "No audio stream found.",
        }

    codec = audio_info.get(
        "codec_name",
        "unknown"
    )

    extension = choose_output_extension(
        codec
    )

    output_path = (
        output_directory /
        (
            video_path.stem +
            extension
        )
    )

    # --------------------------------------------------------
    # Existing output
    # --------------------------------------------------------

    if (
        SKIP_EXISTING
        and output_path.exists()
        and output_path.stat().st_size > 0
    ):

        return {
            "status": "SKIPPED",
            "source": str(video_path),
            "output": str(output_path),
            "codec": codec,
            "size": output_path.stat().st_size,
        }

    # --------------------------------------------------------
    # FFmpeg
    # --------------------------------------------------------

    command = [
        "ffmpeg",

        "-hide_banner",
        "-loglevel",
        "error",

        "-y",

        "-i",
        str(video_path),

        # First audio stream
        "-map",
        "0:a:0",

        # Remove video
        "-vn",

        # LOSSLESS AUDIO STREAM COPY
        "-c:a",
        "copy",

        # Preserve metadata
        "-map_metadata",
        "0",

        str(output_path),
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    except OSError as error:

        return {
            "status": "FAILED",
            "source": str(video_path),
            "output": str(output_path),
            "codec": codec,
            "error": str(error),
        }

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    if (
        result.returncode == 0
        and output_path.exists()
        and output_path.stat().st_size > 0
    ):

        return {
            "status": "DONE",
            "source": str(video_path),
            "output": str(output_path),
            "codec": codec,
            "codec_long_name": audio_info.get(
                "codec_long_name"
            ),
            "sample_rate": audio_info.get(
                "sample_rate"
            ),
            "channels": audio_info.get(
                "channels"
            ),
            "channel_layout": audio_info.get(
                "channel_layout"
            ),
            "bit_rate": audio_info.get(
                "bit_rate"
            ),
            "duration": audio_info.get(
                "duration"
            ),
            "size": output_path.stat().st_size,
        }

    # --------------------------------------------------------
    # Failure
    # --------------------------------------------------------

    error_message = (
        result.stderr.strip()
        if result.stderr
        else "Unknown FFmpeg error."
    )

    # Remove incomplete output.
    if output_path.exists():

        try:
            output_path.unlink()
        except OSError:
            pass

    return {
        "status": "FAILED",
        "source": str(video_path),
        "output": str(output_path),
        "codec": codec,
        "error": error_message,
    }


# ============================================================
# SAVE LOG
# ============================================================

def save_log(
    results,
    total,
    completed,
    skipped,
    no_audio,
    failed,
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    log_file = (
        LOG_FOLDER /
        f"extraction_{timestamp}.json"
    )

    log_data = {

        "application": APP_NAME,

        "version": APP_VERSION,

        "author": AUTHOR,

        "timestamp": timestamp,

        "application_folder":
            str(BASE_FOLDER),

        "source_folder":
            str(VIDEO_FOLDER),

        "audio_output_folder":
            str(AUDIO_FOLDER),

        "total_files":
            total,

        "completed":
            completed,

        "skipped":
            skipped,

        "no_audio":
            no_audio,

        "failed":
            failed,

        "results":
            results,
    }

    try:

        with open(
            log_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                log_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return log_file

    except OSError as error:

        print()
        print(
            Color.RED +
            f"Could not save log: {error}" +
            Color.RESET
        )

        return None


# ============================================================
# MAIN
# ============================================================

def main():

    print_header()

    # ========================================================
    # STEP 1 — APPLICATION FOLDERS
    # ========================================================

    print(
        Color.CYAN +
        "[1/3] Checking application folders..." +
        Color.RESET
    )

    print()

    if not create_required_folders():

        input(
            "\nPress Enter to exit..."
        )

        return

    # ========================================================
    # STEP 2 — FFMPEG
    # ========================================================

    print()

    print(
        Color.CYAN +
        "[2/3] Checking required software..." +
        Color.RESET
    )

    if not ensure_ffmpeg():

        input(
            "\nPress Enter to exit..."
        )

        return

    # ========================================================
    # STEP 3 — VIDEO SEARCH
    # ========================================================

    print()

    print(
        Color.CYAN +
        "[3/3] Searching for videos..." +
        Color.RESET
    )

    video_files = find_video_files()

    if not video_files:

        print()

        print(
            Color.YELLOW +
            "No supported video files were found." +
            Color.RESET
        )

        print()

        print(
            "Put your videos inside:"
        )

        print(
            f"  {VIDEO_FOLDER}"
        )

        input(
            "\nPress Enter to exit..."
        )

        return

    total = len(
        video_files
    )

    print()

    print(
        Color.GREEN +
        f"✓ Found {total} video(s)." +
        Color.RESET
    )

    print()

    print(
        f"Application : {BASE_FOLDER}"
    )

    print(
        f"Source      : {VIDEO_FOLDER}"
    )

    print(
        f"Audio       : {AUDIO_FOLDER}"
    )

    print()

    print("-" * 72)

    # ========================================================
    # STATISTICS
    # ========================================================

    completed = 0
    skipped = 0
    no_audio = 0
    failed = 0

    results = []

    # ========================================================
    # PROCESS
    # ========================================================

    for index, video_path in enumerate(
        video_files,
        start=1
    ):

        print()

        print(
            Color.CYAN +
            f"[{index}/{total}]" +
            Color.RESET +
            f" {video_path.name}"
        )

        result = extract_audio(
            video_path
        )

        results.append(
            result
        )

        status = result.get(
            "status"
        )

        # ----------------------------------------------------
        # DONE
        # ----------------------------------------------------

        if status == "DONE":

            completed += 1

            print(
                Color.GREEN +
                "   ✓ DONE" +
                Color.RESET
            )

            print(
                f"   Codec    : "
                f"{result.get('codec', 'Unknown')}"
            )

            print(
                f"   Duration : "
                f"{format_duration(result.get('duration'))}"
            )

            print(
                f"   Output   : "
                f"{result.get('output')}"
            )

            if result.get("size") is not None:

                print(
                    f"   Size     : "
                    f"{format_size(result['size'])}"
                )

        # ----------------------------------------------------
        # SKIPPED
        # ----------------------------------------------------

        elif status == "SKIPPED":

            skipped += 1

            print(
                Color.YELLOW +
                "   → SKIPPED — already exists" +
                Color.RESET
            )

            print(
                f"   Output   : "
                f"{result.get('output')}"
            )

        # ----------------------------------------------------
        # NO AUDIO
        # ----------------------------------------------------

        elif status == "NO_AUDIO":

            no_audio += 1

            print(
                Color.YELLOW +
                "   ! NO AUDIO STREAM" +
                Color.RESET
            )

        # ----------------------------------------------------
        # FAILED
        # ----------------------------------------------------

        elif status == "FAILED":

            failed += 1

            print(
                Color.RED +
                "   ✗ FAILED" +
                Color.RESET
            )

            error = result.get(
                "error",
                "Unknown error."
            )

            print(
                Color.GRAY +
                f"   {error}" +
                Color.RESET
            )

    # ========================================================
    # SAVE LOG
    # ========================================================

    log_file = save_log(
        results,
        total,
        completed,
        skipped,
        no_audio,
        failed,
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print()

    print("=" * 72)

    print(
        "COMPLETE".center(72)
    )

    print("=" * 72)

    print()

    print(
        f"Total files : {total}"
    )

    print(
        Color.GREEN +
        f"Completed   : {completed}" +
        Color.RESET
    )

    print(
        Color.YELLOW +
        f"Skipped     : {skipped}" +
        Color.RESET
    )

    print(
        Color.YELLOW +
        f"No Audio    : {no_audio}" +
        Color.RESET
    )

    print(
        Color.RED +
        f"Failed      : {failed}" +
        Color.RESET
    )

    print()

    print(
        "Audio folder:"
    )

    print(
        f"  {AUDIO_FOLDER}"
    )

    if log_file:

        print()

        print(
            "Log file:"
        )

        print(
            f"  {log_file}"
        )

    print()

    print("=" * 72)

    input(
        "\nPress Enter to exit..."
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print()

        print(
            Color.YELLOW +
            "Operation cancelled by user." +
            Color.RESET
        )

        sys.exit(1)

    except Exception as error:

        print()
        print()

        print(
            Color.RED +
            "Unexpected error:" +
            Color.RESET
        )

        print(
            str(error)
        )

        input(
            "\nPress Enter to exit..."
        )