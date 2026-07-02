# -= ml_pasteImagePlane.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Revision 1
#   / / / / / / /  2026-03-23
#  /_/ /_/ /_/_/  _________
#               /_________/
#
#     ______________
# - -/__ License __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Copyright 2026 Morgan Loomis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR OTHER DEALINGS IN THE SOFTWARE.
#
#     __________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Paste a raster image from the Windows clipboard into the saved scene directory
# as imagePlane1.png, imagePlane2.bmp, and so on, and create a camera-local image
# plane on the viewport camera (via ml_utilities.getCurrentCamera).
#
#     ____________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Save the scene, place an image on the clipboard (PNG or standard bitmap), then
# run from the Script Editor or a shelf button:
#
#     import ml_pasteImagePlane
#     ml_pasteImagePlane.main()
#
#     ___________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - -
#
# This script requires the ml_utilities module. Clipboard paste is supported on
# Windows only (stdlib ctypes / Win32).
#
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -

__author__ = 'Morgan Loomis'
__license__ = 'MIT'
__revision__ = 1
__category__ = 'utilities'

import os
import re
import struct
import sys
import ctypes
from ctypes import wintypes

import maya.cmds as mc

try:
    import ml_utilities as utl
except ImportError:
    utl = None

# --- Win32 clipboard (read-only; never EmptyClipboard) ---

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

CF_DIB = 8

OpenClipboard = user32.OpenClipboard
OpenClipboard.argtypes = (wintypes.HWND,)
OpenClipboard.restype = wintypes.BOOL

CloseClipboard = user32.CloseClipboard
CloseClipboard.restype = wintypes.BOOL

IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
IsClipboardFormatAvailable.argtypes = (wintypes.UINT,)
IsClipboardFormatAvailable.restype = wintypes.BOOL

GetClipboardData = user32.GetClipboardData
GetClipboardData.argtypes = (wintypes.UINT,)
GetClipboardData.restype = wintypes.HANDLE

RegisterClipboardFormatW = user32.RegisterClipboardFormatW
RegisterClipboardFormatW.argtypes = (wintypes.LPCWSTR,)
RegisterClipboardFormatW.restype = wintypes.UINT

GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = (wintypes.HANDLE,)
GlobalLock.restype = wintypes.LPVOID

GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = (wintypes.HANDLE,)
GlobalUnlock.restype = wintypes.BOOL

GlobalSize = kernel32.GlobalSize
GlobalSize.argtypes = (wintypes.HANDLE,)
GlobalSize.restype = ctypes.c_size_t

_PNG_MAGIC = b'\x89PNG\r\n\x1a\n'
_IMAGE_PLANE_RE = re.compile(r'^imagePlane(\d+)\.(png|bmp)$', re.IGNORECASE)


def _handle_global_bytes(handle):
    if not handle:
        return None
    ptr = GlobalLock(handle)
    if not ptr:
        return None
    try:
        size = GlobalSize(handle)
        if size == 0:
            return b''
        return ctypes.string_at(ptr, size)
    finally:
        GlobalUnlock(handle)


def _clipboard_read_png_bytes():
    """Try registered PNG formats; return raw PNG bytes or None."""
    for name in ('PNG', 'image/png'):
        fmt = RegisterClipboardFormatW(name)
        if not fmt or not IsClipboardFormatAvailable(fmt):
            continue
        if not OpenClipboard(None):
            continue
        try:
            h = GetClipboardData(fmt)
            data = _handle_global_bytes(h)
            if data and data.startswith(_PNG_MAGIC):
                return data
        finally:
            CloseClipboard()
    return None


def _dib_to_bmp_file_bytes(dib):
    """
    Build a BMP file (header + DIB) from CF_DIB memory.
    Supports 24/32 bpp BI_RGB only.
    """
    if len(dib) < 40:
        raise ValueError('Clipboard DIB is too small to be a valid bitmap.')

    biSize = struct.unpack_from('<I', dib, 0)[0]
    if biSize < 40:
        raise ValueError('Invalid DIB: BITMAPINFOHEADER size.')

    biWidth = struct.unpack_from('<i', dib, 4)[0]
    biHeight = struct.unpack_from('<i', dib, 8)[0]
    biPlanes = struct.unpack_from('<H', dib, 12)[0]
    biBitCount = struct.unpack_from('<H', dib, 14)[0]
    biCompression = struct.unpack_from('<I', dib, 16)[0]

    if biPlanes != 1:
        raise ValueError('Unsupported DIB: expected one color plane.')
    if biCompression != 0:
        raise ValueError('Unsupported DIB: only uncompressed (BI_RGB) bitmaps are supported.')
    if biBitCount not in (24, 32):
        raise ValueError('Unsupported DIB: need 24 or 32 bits per pixel.')

    header_plus_palette = biSize
    if header_plus_palette > len(dib):
        raise ValueError('Invalid DIB: header extends past buffer.')

    w = abs(biWidth)
    h = abs(biHeight)
    row_bytes = ((w * biBitCount + 31) // 32) * 4
    expected_pixels = row_bytes * h
    pixel_len = len(dib) - header_plus_palette
    if pixel_len < expected_pixels:
        raise ValueError('Unsupported DIB: pixel data size does not match dimensions.')

    file_size = 14 + len(dib)
    off_bits = 14 + header_plus_palette
    bfh = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, off_bits)
    return bfh + dib


def _clipboard_read_dib_bmp_bytes():
    """Read CF_DIB and return BMP file bytes, or None if unavailable."""
    if not IsClipboardFormatAvailable(CF_DIB):
        return None
    if not OpenClipboard(None):
        return None
    try:
        h = GetClipboardData(CF_DIB)
        dib = _handle_global_bytes(h)
        if not dib:
            return None
        return _dib_to_bmp_file_bytes(dib)
    finally:
        CloseClipboard()


def read_clipboard_image_bytes():
    """
    Return (file_bytes, extension) where extension is '.png' or '.bmp'.
    Raises RuntimeError if no supported image is on the clipboard.
    """
    if sys.platform != 'win32':
        raise RuntimeError('Clipboard image paste is only supported on Windows.')

    png = _clipboard_read_png_bytes()
    if png:
        return png, '.png'

    try:
        bmp = _clipboard_read_dib_bmp_bytes()
    except ValueError as e:
        raise RuntimeError('Could not read bitmap from clipboard (DIB): %s' % e)

    if bmp:
        return bmp, '.bmp'

    raise RuntimeError('No PNG or DIB image on the clipboard.')


def next_image_plane_path(directory, ext):
    """
    Next sequential path: imagePlane<N>.ext scanning existing .png and .bmp;
    N = max existing index + 1 (or 1). ext is '.png' or '.bmp'.
    """
    max_n = 0
    try:
        names = os.listdir(directory)
    except OSError:
        names = []
    for name in names:
        m = _IMAGE_PLANE_RE.match(name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    n = max_n + 1
    basename = 'imagePlane%d%s' % (n, ext)
    return os.path.abspath(os.path.join(directory, basename)), ext


def _require_utl():
    if utl is None:
        mc.confirmDialog(
            title='Module Not Found',
            message='This tool requires the ml_utilities module.',
            button=['OK'],
            defaultButton='OK')
        return False
    return True


def _saved_scene_directory():
    """
    Return absolute normalized directory of the saved scene, or None if invalid.
    """
    scene_path = mc.file(query=True, sceneName=True)
    if not scene_path or not str(scene_path).strip():
        return None
    scene_path = os.path.abspath(os.path.normpath(scene_path))
    directory = os.path.dirname(scene_path)
    if not directory or not os.path.isdir(directory):
        return None
    return directory


def main():
    if not _require_utl():
        return

    if sys.platform != 'win32':
        utl.error('Paste image plane is only supported on Windows.')
        return

    out_dir = _saved_scene_directory()
    if not out_dir:
        utl.error('Save the scene first. Paste image plane writes next to the scene file.')
        return

    try:
        file_bytes, ext = read_clipboard_image_bytes()
    except RuntimeError as e:
        utl.error(str(e))
        return

    out_path, _ = next_image_plane_path(out_dir, ext)

    try:
        with open(out_path, 'wb') as f:
            f.write(file_bytes)
    except OSError as e:
        utl.error('Could not write image file: %s' % e)
        return

    cam = utl.getCurrentCamera()
    if not cam:
        utl.error('Could not resolve the current viewport camera. Highlight a model panel and try again.')
        return

    try:
        mc.imagePlane(camera=cam, fileName=out_path.replace('\\', '/'))
    except RuntimeError as e:
        utl.error('Could not create image plane: %s' % e)


if __name__ == '__main__':
    main()
