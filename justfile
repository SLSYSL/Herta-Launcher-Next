set shell := ["powershell.exe", "-c"]

# 默认命令
default: help

# 安装uv
install-uv:
    @if ($IsWindows -or $env:OS -eq 'Windows_NT') { Invoke-RestMethod -Uri https://astral.sh/uv/install.ps1 | Invoke-Expression } else { sh -c "curl -LsSf https://astral.sh/uv/install.sh | sh" }

# 安装项目依赖
install:
    uv sync

# 运行项目
run:
    uv run textual run --dev main.py

# 构建项目
build:
    uv run pyinstaller main.spec

# 显示所有可用命令
help:
    @just --list