#!/usr/bin/env python3
"""Call RollDek's OpenAI-compatible GPT Image API.

Examples:
  ROLLDEK_API_KEY=... ./rolldek_image.py --prompt 'a red fox' --output fox.png
  ROLLDEK_API_KEY=... ./rolldek_image.py --prompt 'add a hat' --image fox.png --output edited.png
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, NoReturn

BASE_URL = "https://rolldek.com/v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit images through the RollDek GPT Image API."
    )
    parser.add_argument("--prompt", required=True, help="Image prompt")
    parser.add_argument(
        "--model",
        default="gpt-image-2",
        choices=("gpt-image-2", "gpt-image-2-high"),
    )
    parser.add_argument("--size", help="Supported WxH size, for example 1024x1024")
    parser.add_argument(
        "--quality", choices=("medium", "high"), help="Image quality"
    )
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-10)")
    parser.add_argument(
        "--response-format",
        choices=("b64_json", "url"),
        default="b64_json",
    )
    parser.add_argument(
        "--image",
        action="append",
        default=[],
        help="Reference image; repeat for multiple images (edits only)",
    )
    parser.add_argument(
        "--output",
        help="Output file. With --n > 1, additional files get -2, -3 suffixes.",
    )
    parser.add_argument(
        "--print-response",
        action="store_true",
        help="Print the API response JSON (may be large with b64_json)",
    )
    return parser.parse_args()


def fail(message: str) -> NoReturn:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def auth_header() -> str:
    key = os.environ.get("ROLLDEK_API_KEY")
    if not key:
        fail("ROLLDEK_API_KEY is not set")
    return key


def validate(args: argparse.Namespace) -> None:
    if not 1 <= args.n <= 10:
        fail("--n must be between 1 and 10")
    if args.model == "gpt-image-2" and args.quality == "high":
        fail("gpt-image-2 only supports medium quality; use gpt-image-2-high for high")
    if len(args.image) > 16:
        fail("at most 16 reference images are supported")
    if args.output and args.response_format == "url":
        # URLs are downloaded below, so this is valid; keep the behavior explicit.
        pass
    for image in args.image:
        path = Path(image)
        if not path.is_file():
            fail(f"reference image does not exist: {image}")


def request_json(args: argparse.Namespace, key: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "response_format": args.response_format,
    }
    if args.size:
        payload["size"] = args.size
    if args.quality:
        payload["quality"] = args.quality
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{BASE_URL}/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    return perform(request)


def multipart_body(args: argparse.Namespace) -> tuple[bytes, str]:
    boundary = "----RollDekGPTImg" + uuid.uuid4().hex
    chunks: list[bytes] = []

    def field(name: str, value: str) -> None:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )

    def file_field(name: str, filename: str) -> None:
        path = Path(filename)
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{path.name}"\r\n'
                ).encode(),
                f"Content-Type: {content_type}\r\n\r\n".encode(),
                path.read_bytes(),
                b"\r\n",
            ]
        )

    field("model", args.model)
    field("prompt", args.prompt)
    if args.size:
        field("size", args.size)
    if args.quality:
        field("quality", args.quality)
    field("n", str(args.n))
    field("response_format", args.response_format)
    for image in args.image:
        file_field("image[]", image)
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def request_edit(args: argparse.Namespace, key: str) -> dict[str, Any]:
    body, boundary = multipart_body(args)
    request = urllib.request.Request(
        f"{BASE_URL}/images/edits",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )
    return perform(request)


def perform(request: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"RollDek returned HTTP {exc.code}: {detail[:2000]}")
    except urllib.error.URLError as exc:
        fail(f"request failed: {exc.reason}")
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail("RollDek returned a non-JSON response")
    if not isinstance(parsed, dict):
        fail("unexpected response shape")
    return parsed


def output_path(path: Path, index: int, total: int) -> Path:
    if total == 1:
        return path
    return path.with_name(f"{path.stem}-{index + 1}{path.suffix}")


def save_results(response: dict[str, Any], args: argparse.Namespace) -> None:
    if not args.output:
        return
    data = response.get("data")
    if not isinstance(data, list) or not data:
        fail("response contains no image data")
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            fail("unexpected image item in response")
        target = output_path(destination, index, len(data))
        if args.response_format == "b64_json":
            encoded = item.get("b64_json")
            if not isinstance(encoded, str):
                fail("response does not contain b64_json")
            try:
                target.write_bytes(base64.b64decode(encoded, validate=True))
            except (ValueError, base64.binascii.Error) as exc:
                fail(f"invalid b64_json: {exc}")
        else:
            url = item.get("url")
            if not isinstance(url, str):
                fail("response does not contain url")
            try:
                with urllib.request.urlopen(url, timeout=180) as source:
                    target.write_bytes(source.read())
            except (urllib.error.URLError, urllib.error.HTTPError) as exc:
                fail(f"could not download image URL: {exc}")
        print(f"Saved {target}")


def main() -> None:
    args = parse_args()
    validate(args)
    key = auth_header()
    response = request_edit(args, key) if args.image else request_json(args, key)
    save_results(response, args)
    if args.print_response or not args.output:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    elif response.get("data"):
        print(f"RollDek returned {len(response['data'])} image(s)")


if __name__ == "__main__":
    main()
