from __future__ import with_statement
from __future__ import absolute_import
from __future__ import division

import sys
import struct
import math
from PIL import Image


class Icon(object):
    def __init__(self, image_paths=None, output_path=None):
        self.image_paths = []
        if image_paths:
            self.image_paths = image_paths
        self.output_path = None
        if output_path:
            self.output_path = output_path

        self._ico_data = ""
        self._img_data = ""

    def build(self):
        self._ico_data = ""
        self._img_data = ""

        if not len(self.image_paths):
            raise Exception("No images added")

        num_images = len(self.image_paths)

        self._ico_data = self.write_header(num_images)

        # Size of all the headers (image headers + file header)
        dataoffset = struct.calcsize('BBBBHHII') * num_images + \
                struct.calcsize('HHH')

        for image in self.image_paths:
            icondirentry, imgdata, dataoffset = self.write_icondirentry(
                    image, dataoffset)
            self._ico_data += icondirentry
            self._img_data += imgdata

        if self.output_path:
            self.save()

    def getdata(self):
        return self._ico_data + self._img_data

    def save(self):
        if not self._ico_data or not self._img_data:
            self.build()

        if self.output_path:
            with open(self.output_path, 'wb') as f:
                f.write(self._ico_data)
                f.write(self._img_data)
        else:
            raise Exception("Missing output path.")

    def calcstride(self, width_in_bits):
        length = (width_in_bits + 31) // 32
        return length * 4

    def write_header(self, num_images):
        return struct.pack('HHH', 0, 1, num_images)

    def write_icondirentry(self, image_path, dataoffset):
        img = Image.open(image_path)
        img.load()

        #img = img.convert('RGB')
        if img.mode == 'RGB':
            imgdata = img.tostring('raw', 'BGR', 0, -1)
        elif img.mode == 'RGBA':
            r, g, b, a = img.split()
            img = Image.merge('RGBA', (b, g, r, a))
            imgdata = img.tostring('raw', 'RGBA', 0, -1)
        elif img.mode == 'P':
            imgdata = img.tostring('raw', 'P', 0, -1)

        bWidth = img.size[0]
        bHeight = img.size[1]
        bReserved = 0
        wPlanes = 0 # FIXME

        # Bit count
        if img.mode == 'RGB':
            wBitCount = 24
            bColorCount = 0
        elif img.mode == 'RGBA':
            wBitCount = 32
            bColorCount = 0
        elif img.mode == 'P':
            wBitCount = 8
            bColorCount = len(img.palette.getdata()[1]) // 3

        dwImageOffset = dataoffset

        # Num bytes in image section
        length = len(imgdata) + self.calcstride(img.size[0]) * img.size[1]

        # Generate bitmapinfoheader and prepend this to the pixel data
        bmpinfoheader = self.write_icon_image(bWidth, bHeight, wPlanes,
                wBitCount, length, bColorCount)

        data = bmpinfoheader
        if img.mode == 'RGB' or img.mode == 'RGBA':
            # XOR mask (Image)
            data += imgdata
            palette_alpha = False
        elif img.mode == 'P':
            # Write the palette
            palette_data = img.palette.getdata()
            if palette_data[0] == 'RGB;L':
                palette_alpha = False
                for x in range(0, len(palette_data[1]), 3):
                    data += palette_data[1][x + 2] # B
                    data += palette_data[1][x + 1] # G
                    data += palette_data[1][x]     # R
                    data += struct.pack('B', 0)
                data += imgdata
            elif palette_data[0] == 'RGBA;L':
                palette_alpha = True
                #for x in range(4): data += struct.pack('B', 0)
                for x in range(0, len(palette_data[1]), 3):
                    data += palette_data[1][x + 2] # B
                    data += palette_data[1][x + 1] # G
                    data += palette_data[1][x]     # R
                    data += struct.pack('B', 0)
                for byte in imgdata:
                    if ord(byte) == 0:
                        data += struct.pack('B', 0)
                    else:
                        data += struct.pack('B', ord(byte))

        # AND mask (Transparency)
        if not palette_alpha:
            rowstride = self.calcstride(img.size[0])
            print("rowstride", rowstride)
            data += struct.pack('B', 0) * (rowstride * img.size[1])
        else:
            rowstride = self.calcstride(img.size[0])
            print("rowstride", rowstride)
            bytes = [0 for x in range(rowstride * img.size[1])]
            for y in range(img.size[1] - 1, -1, -1):
                for x in range(0, img.size[0], 8): # still assuming multiple of eight
                    i = (y * rowstride + x // 8)
                    for b in range(8):
                        if img.getpixel((x + b, y)) == 0:
                            bytes[i] |= 2 ** (7 - b)
            for y in range(img.size[1] - 1, -1, -1):
                for x in range(rowstride):
                    data += struct.pack('B', bytes[y * rowstride + x])

        # Increment the data offset pointer
        dataoffset += len(data)

        # Size of the dir entry + image data
        dwBytesInRes = len(data)

        # Pack the icondirentry header
        print bWidth, bHeight, bColorCount, bReserved
        icondirentry = struct.pack('BBBBHHII',
                bWidth, bHeight, bColorCount, bReserved, wPlanes, wBitCount,
                dwBytesInRes, dwImageOffset)

        return icondirentry, data, dataoffset

    def write_icon_image(self, width, height, planes, bit_count, size_image, colors_used):
        # BitmapInfoHeader
        biSize = struct.calcsize('IIIHHIIiiII')
        biWidth = width
        biHeight = height * 2 # Include the mask height
        biPlanes = 1 # Must be 1
        biBitCount = bit_count
        biCompression = 0
        biSizeImage = size_image
        biXPelsPerMeter = 0
        biYPelsPerMeter = 0
        biClrUsed = colors_used
        biClrImportant = 0

        return struct.pack('IIIHHIIiiII', biSize, biWidth, biHeight, biPlanes,
                biBitCount, biCompression, biSizeImage, biXPelsPerMeter,
                biYPelsPerMeter, biClrUsed, biClrImportant)

if __name__ == '__main__':
    #output_file = "icon/fs-uae.ico"
    #icon_paths = []
    #for name in ["16", "32", "48s", "64s"]:
    #    icon_paths.append("icon/" + name + ".png")
    #i = Icon(icon_paths, output_file)
    #i.save()

    output_file = "icon/fs-uae-launcher.ico"
    icon_paths = []
    for name in ["16", "32", "48s", "64s"]:
        icon_paths.append("icon/fs-uae-launcher/" + name + ".png")
    i = Icon(icon_paths, output_file)
    i.save()

