#!/usr/bin/env bash

SESSION="ShmoopBot"
e
tmux has-session -t "$SESSION" 2>/dev/null
if [ $? -eq 0 ]; then
    exit 0
fi

tmux new-session -d -s "$SESSION" 'uv run main.py'
