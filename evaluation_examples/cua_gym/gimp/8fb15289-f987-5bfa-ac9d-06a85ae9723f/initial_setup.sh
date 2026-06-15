#!/usr/bin/env bash
# Initial setup script – creates an image that still has an active selection
set -e

XCF_PATH="/tmp/deselect_task.xcf"

# Generate the initial XCF with an active rectangular selection
gimp -i -b "
(let* ((img (car (gimp-image-new 512 512 RGB)))                                   ; create image
       (bg  (car (gimp-layer-new img 512 512 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL))) )
  (gimp-image-insert-layer img bg 0 0)                                             ; add layer
  (gimp-context-set-foreground '(197 6 78))                                        ; set color
  (gimp-edit-fill bg FILL-FOREGROUND)                                              ; fill layer
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 100 100 200 200)             ; create selection
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")        ; save with selection active
  (gimp-quit 0))" >/dev/null 2>&1

# Open the generated file so the user sees the marching-ants selection
DISPLAY=:0 gimp "${XCF_PATH}" &