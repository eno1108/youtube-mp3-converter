import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_FFMPEG_RELATIVE = Path(__file__).resolve().parents[1] / "ffmpeg" / "ffmpeg-8.1.1-full_build-shared" / "bin" / "ffmpeg.exe"


def windows_long_path(path: Path) -> str:
    path_str = str(path)
    if os.name != "nt":
        return path_str
    if path_str.startswith("\\\\?\\"):
        return path_str
    if path_str.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path_str.lstrip("\\")
    return "\\\\?\\" + path_str


def find_ffmpeg(explicit_path: Path | None = None) -> Path | None:
    if explicit_path:
        explicit_path = explicit_path.expanduser().resolve()
        if explicit_path.exists():
            return explicit_path
        return None

    if DEFAULT_FFMPEG_RELATIVE.exists():
        return DEFAULT_FFMPEG_RELATIVE

    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return Path(ffmpeg_path)

    return None


def convert_file(ffmpeg_path: Path, input_file: Path, output_file: Path, bitrate: str) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        windows_long_path(ffmpeg_path),
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        windows_long_path(input_file),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-b:a",
        bitrate,
        windows_long_path(output_file),
    ]
    subprocess.run(cmd, check=True)


def collect_files(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return sorted(folder.rglob("*.mp4"))
    return sorted(folder.glob("*.mp4"))
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_FFMPEG_RELATIVE = Path(__file__).resolve().parents[1] / "ffmpeg" / "ffmpeg-8.1.1-full_build-shared" / "bin" / "ffmpeg.exe"


def windows_long_path(path: Path) -> str:
    path_str = str(path)
    if os.name != "nt":
        return path_str
    if path_str.startswith("\\\\?\\"):
        return path_str
    if path_str.startswith("\\\\"):
        return "\\\\?\\UNC\\" + path_str.lstrip("\\")
    return "\\\\?\\" + path_str


def find_ffmpeg(explicit_path: Path | None = None) -> Path | None:
    if explicit_path:
        explicit_path = explicit_path.expanduser().resolve()
        if explicit_path.exists():
            return explicit_path
        return None

    if DEFAULT_FFMPEG_RELATIVE.exists():
        return DEFAULT_FFMPEG_RELATIVE

    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return Path(ffmpeg_path)

    return None


def convert_file(ffmpeg_path: Path, input_file: Path, output_file: Path, bitrate: str) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        windows_long_path(ffmpeg_path),
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        windows_long_path(input_file),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-b:a",
        bitrate,
        windows_long_path(output_file),
    ]
    subprocess.run(cmd, check=True)


def collect_files(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return sorted(folder.rglob("*.mp4"))
    return sorted(folder.glob("*.mp4"))


def convert_folder(
    input_folder: Path,
    output_folder: Path | None,
    bitrate: str,
    ffmpeg_path: Path,
    recursive: bool,
    overwrite: bool,
) -> int:
    files = collect_files(input_folder, recursive)
    if not files:
        print(f"MP4ファイルが見つかりません: {input_folder}")
        return 0

    failed = 0
    for source in files:
        relative = source.relative_to(input_folder)
        target = (output_folder / relative).with_suffix(".mp3") if output_folder else source.with_suffix(".mp3")
        if target.exists() and not overwrite:
            print(f"スキップ: 既に存在します -> {target}")
            continue

        print(f"変換: {source} -> {target}")
        try:
            convert_file(ffmpeg_path, source, target, bitrate)
        except subprocess.CalledProcessError as exc:
            print(f"失敗: {source} (ffmpeg code={exc.returncode})")
            failed += 1
        except Exception as exc:
            print(f"失敗: {source} ({exc})")
            failed += 1

    print(f"完了: {len(files) - failed}/{len(files)} 件 成功, {failed} 件 失敗")
    return failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="フォルダ内の MP4 を MP3 に一括変換します。")
    parser.add_argument("input_folder", type=Path, help="変換対象のフォルダ")
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=None,
        help="出力先フォルダ。省略時は入力フォルダに同名の mp3 を作成します。",
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="MP3 のビットレート (例: 192k)。デフォルトは 192k です。",
    )
    parser.add_argument(
        "--ffmpeg",
        type=Path,
        default=None,
        help="ffmpeg.exe のパス。省略時はローカルの ffmpeg または PATH 上の ffmpeg を検索します。",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="サブフォルダ内の MP4 も再帰的に変換します。",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="既存の MP3 ファイルを上書きします。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_folder = args.input_folder.expanduser().resolve()
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"エラー: 入力フォルダが見つかりません: {input_folder}")
        return 1

    output_folder = args.output_folder
    if output_folder is not None:
        output_folder = output_folder.expanduser().resolve()
        output_folder.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = find_ffmpeg(args.ffmpeg)
    if ffmpeg_path is None:
        print("エラー: ffmpeg が見つかりません。--ffmpeg でパスを指定するか、PATH に追加してください。")
        return 2

    convert_folder(
        input_folder=input_folder,
        output_folder=output_folder,
        bitrate=args.bitrate,
        ffmpeg_path=ffmpeg_path,
        recursive=args.recursive,
        overwrite=args.overwrite,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def convert_folder(
    input_folder: Path,
    output_folder: Path | None,
    bitrate: str,
    ffmpeg_path: Path,
    recursive: bool,
    overwrite: bool,
) -> int:
    files = collect_files(input_folder, recursive)
    if not files:
        print(f"MP4ファイルが見つかりません: {input_folder}")
        return 0

    failed = 0
    for source in files:
        relative = source.relative_to(input_folder)
        target = (output_folder / relative).with_suffix(".mp3") if output_folder else source.with_suffix(".mp3")
        if target.exists() and not overwrite:
            print(f"スキップ: 既に存在します -> {target}")
            continue

        print(f"変換: {source} -> {target}")
        try:
            convert_file(ffmpeg_path, source, target, bitrate)
        except subprocess.CalledProcessError as exc:
            print(f"失敗: {source} (ffmpeg code={exc.returncode})")
            failed += 1
        except Exception as exc:
            print(f"失敗: {source} ({exc})")
            failed += 1

    print(f"完了: {len(files) - failed}/{len(files)} 件 成功, {failed} 件 失敗")
    return failed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="フォルダ内の MP4 を MP3 に一括変換します。")
    parser.add_argument("input_folder", type=Path, help="変換対象のフォルダ")
    parser.add_argument(
        "--output-folder",
        type=Path,
        default=None,
        help="出力先フォルダ。省略時は入力フォルダに同名の mp3 を作成します。",
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help="MP3 のビットレート (例: 192k)。デフォルトは 192k です。",
    )
    parser.add_argument(
        "--ffmpeg",
        type=Path,
        default=None,
        help="ffmpeg.exe のパス。省略時はローカルの ffmpeg または PATH 上の ffmpeg を検索します。",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="サブフォルダ内の MP4 も再帰的に変換します。",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="既存の MP3 ファイルを上書きします。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_folder = args.input_folder.expanduser().resolve()
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"エラー: 入力フォルダが見つかりません: {input_folder}")
        return 1

    output_folder = args.output_folder
    if output_folder is not None:
        output_folder = output_folder.expanduser().resolve()
        output_folder.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = find_ffmpeg(args.ffmpeg)
    if ffmpeg_path is None:
        print("エラー: ffmpeg が見つかりません。--ffmpeg でパスを指定するか、PATH に追加してください。")
        return 2

    convert_folder(
        input_folder=input_folder,
        output_folder=output_folder,
        bitrate=args.bitrate,
        ffmpeg_path=ffmpeg_path,
        recursive=args.recursive,
        overwrite=args.overwrite,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
