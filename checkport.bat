@echo off
CLS
set myRegistry=%~dp0/ports/
echo %myRegistry%

vcpkg install video-x --overlay-ports=ports --triplet x64-windows