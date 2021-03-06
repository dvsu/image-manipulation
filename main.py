#!/usr/bin/python3

import os
from PIL import Image


class ImageManipulation:

    def __init__(self, source_dir: str, output_dir: str, target_extension: str):
        self.__source_dir = source_dir
        self.__output_dir = output_dir
        self.__target_extension = target_extension
        self.__recognized_extensions = ["", "jpg", "jpeg", "png", "bmp"]
        self._directory_check()
        self._extension_check()

    def _directory_check(self) -> None:
        if not os.path.exists(self.__source_dir):
            raise NameError("Directory not found")

        if not os.listdir(self.__source_dir):
            raise FileNotFoundError(
                "No image files found in the source directory")

        if not os.path.exists(self.__output_dir):
            os.mkdir(self.__output_dir)

    def _extension_check(self) -> None:
        if self.__target_extension not in self.__recognized_extensions:
            raise NameError(
                f"Target extension '{self.__target_extension}' is not recognized")

    def _rotate(self, img: Image, degrees: int) -> Image:
        return img.rotate(degrees)

    def _resize(self, img: Image, target_size: tuple) -> Image:
        return img.resize(target_size)

    def _resize_percent(self, img: Image, resize_percent_width: int, resize_percent_length: int) -> Image:
        return img.resize((resize_percent_width, resize_percent_length))

    def transform(self, rotate: int = 0, resize: tuple = (), resize_percent: int = 0) -> None:

        for file in os.listdir(self.__source_dir):
            filename, file_ext = os.path.splitext(file)

            if file_ext.replace(".", "") not in self.__recognized_extensions:
                continue

            with Image.open(f"{self.__source_dir}/{file}") as img:
                if rotate:
                    img = self._rotate(img=img, degrees=rotate)

                if resize_percent:
                    width, length = img.size
                    img = self._resize_percent(img=img, resize_percent_width=int(
                        width*resize_percent/100), resize_percent_length=int(length*resize_percent/100))

                if resize:
                    if len(resize) != 2:
                        raise TypeError("resize has to be in '(width,length)'")
                    img = self._resize(img=img, target_size=resize)

                img.convert("RGB").save(
                    f"{self.__output_dir}/{filename}.{self.__target_extension}", self.__target_extension.upper(), quality=100)


im = ImageManipulation(source_dir='path/to/source',
                       output_dir='path/to/output', target_extension="jpeg")

im.transform(resize=(1080, 720))
