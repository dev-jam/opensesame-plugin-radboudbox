# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [4.6.0] - 2025-09-28

- only create keyboard item in dummy mode (fixes all kinds of multi-threading problems)
- more precise placement of lock
- bg item always join the thread

## [4.5.0] - 2025-09-19

- reorganization of code to make it more robust

## [4.4.0] - 2025-09-05

- convert string handling to f-strings

## [4.3.0] - 2025-09-03

- wait_buttons, get_buttons_wait: moved timeout to run stage
- code cleanup

## [4.2.0] - 2025-07-17

- license cleanup

## [4.1.1] - 2024-06-03

- add 1 ms pause after start thread to compensate for initialization of buttonbox
    
## [4.1.0] - 2024-05-24

- enable pulse mode
    
## [4.0.0] - 2024-05-23

- code improvement for send control item and send trigger item
- checkbox bitsi simple and extended
    
## [3.1.0] - 2023-12-04

- fixed item dependency checks when running an experiment
    
## [3.0.1] - 2023-08-30

- fixed dependencies
    
## [3.0.0] - 2023-08-15

- new style api OpenSesame 4.0
- lots of small fixes and code cleanup
    
## [2.5.0] - 2023-08-13

Final release for OpenSesame 3 API

- small bugfixes
    
## [v2.4.0] - 2023-07-03

- removed some legacy code, multiprocessing with spawn on Linux should work now.
    
## [v2.3.0] - 2022-11-25

- new plugin code style
- debian packaging fixed

## v2.0.0 - 2021-04-15

- First release

[Unreleased]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.6.0...HEAD
[4.6.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.5.0...4.6.0
[4.5.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.4.0...4.5.0
[4.4.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.3.0...4.4.0
[4.3.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.2.0...4.3.0
[4.2.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.1.1...4.2.0
[4.1.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.1.0...4.1.1
[4.1.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.0.0...4.1.0
[4.0.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.1.0...4.0.0
[3.1.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/2.5.0...3.0.0
[2.5.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.4.0...2.5.0
[v2.4.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.3.0...v2.4.0
[v2.3.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.0.0...v2.3.0
