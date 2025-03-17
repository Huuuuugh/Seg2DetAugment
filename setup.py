import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Seg2DetAugment",
    version="0.0.3",
    author="XavierHugh",
    author_email="2396392765@qq.com",
    description="A data augmentation package for converting segmentation data to detection data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Huuuuugh/Seg2DetAugment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
        "opencv-python",
    ]
)
