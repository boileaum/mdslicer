# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-10-31

### Added

- expose a `split_header_and_content()` function to split the header and the content of a markdown file

## [0.2.0] - 2024-10-31

### Added

- Use doctest to test the code

### Changed

- Enhance the documentation
- The `MDSlicer` initializer uses `kwargs` to pass the parameters to the `Markdown` parser
- Split between a `.slice_file()` and a `.slice_content()` method


## [0.1.8] - 2024-10-30

### Added

- First working version
