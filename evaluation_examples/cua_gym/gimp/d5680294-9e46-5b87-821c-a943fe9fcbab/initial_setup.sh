#!/usr/bin/env bash
# === Initial Setup Script ===
# Creates an XCF with a single layer still bearing its default name "Layer"
# Task for the user: rename that layer to “New Layer”

set -e

XCF_PATH="/tmp/rename_layer_task.xcf"

# 1. Generate initial XCF via Script-Fu in non-interactive batch mode
gimp -i -b "
(let* ((img    (car (gimp-image-new 800 600 RGB)))                     ; New RGB image
       (layer1 (car (gimp-layer-new img 800 600 RGB-IMAGE \"Layer\"     ; Default-named layer
                                      100 LAYER-MODE-NORMAL))))
  (gimp-image-insert-layer img layer1 0 0)                             ; Add layer to image
  (gimp-context-set-foreground '(125 139 244))                         ; Set paint color
  (gimp-edit-fill layer1 FILL-FOREGROUND)                              ; Fill layer
  (gimp-xcf-save RUN-NONINTERACTIVE img layer1                         ; Save XCF
                 \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0))" >/dev/null 2>&1

# 2. Automatically open the generated file for the user
DISPLAY=:0 gimp "${XCF_PATH}" &