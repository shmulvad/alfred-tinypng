# Alfred TinyPNG

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/shmulvad/alfred-tinypng?sort=semver&style=flat-square)][releases]
![Languages supported](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?style=flat-square)
[![GitHub downloads](https://img.shields.io/github/downloads/shmulvad/alfred-tinypng/total?style=flat-square)][releaseLatest]
[![GitHub issues](https://img.shields.io/github/issues/shmulvad/alfred-tinypng?style=flat-square)][issues]
[![GitHub license](https://img.shields.io/github/license/shmulvad/alfred-tinypng?style=flat-square)][license]


An [Alfred][alfred] workflow for quickly compressing and resizing images using [TinyPNG][tinypng]. Simply select a collection of images or a folder in Finder and activate the workflow.

<p align="center">
  <img width="1200" height="auto" src="images/compressing.gif?raw=true">
</p>

⭐ If you find this repo useful, please consider starring it to let me know.


## Installation and Getting Started
1. Install [alfred-tinypng][releaseLatest] workflow.
2. All further updates are handled automatically.

You will need to configure the workflow with an API key from TinyPNG. Type `tinypng_api` to get a link to [the page][tinyApi] where you can get your API key and to actually set the key when you have gotten it.

<p align="center">
  <img width="1200" height="auto" src="images/tinypng_api.png?raw=true">
</p>

The workflow only supports Python 3+. If you have any errors running the code, try changing the `pythonDir` environment variable in the workflow to the the path at which you have Python 3 installed.

## Usage
Select either a folder, image file or a number of image files in Finder. Afterward, open Alfred and type `tinypng`. You are presented with the following choices:

<p align="center">
  <img width="1200" height="auto" src="images/tinypng.png?raw=true">
</p>

Choose an item based on what you want. When selected, the workflow will start compressing/resizing the image(s). After it is done, they will be saved to the same directory and with the same filename as the original image. The original image will be preserved with `.bak` prepended before the file extension. I.e. if compressing `img.jpg`, this will now become `img.bak.jpg` and the compressed image will be saved as `img.jpg`.

Refer to the TinyPNG documentation for a full explanation of the different resizing options.


## Why? [Another TinyPNG workflow][tinypngOtherAlfred] already exists

* It doesn't support choosing the files based on what is selected in Finder (which I personally prefer).
* Only simple compression is supported whereas all TinyPNG compressions and resizing options are supported in this workflow.
* It seems to be abandoned by the creator (has not been updated since 2015).


## Credits
The workflow makes use of the following:

* [OneUpdater][oneUpdater] by vitorgalvao for handling automatic updates.
* [TinyPNG Python API][tinypngApi]

[alfred]: https://www.alfredapp.com/
[license]: https://github.com/shmulvad/alfred-tinypng/blob/master/LICENSE
[issues]: https://github.com/shmulvad/alfred-tinypng/issues
[tinyApi]: https://tinypng.com/developers
[tinypng]: https://tinypng.com
[releases]: https://github.com/shmulvad/alfred-tinypng/releases
[releaseLatest]: https://github.com/shmulvad/alfred-tinypng/releases/latest/download/TinyPNG.alfredworkflow
[oneUpdater]: https://github.com/vitorgalvao/alfred-workflows/tree/master/OneUpdater
[tinypngApi]: https://tinypng.com/developers/reference/python
[tinypngOtherAlfred]: https://www.alfredforum.com/topic/1520-tiny-png-workflow-updated-to-v12/