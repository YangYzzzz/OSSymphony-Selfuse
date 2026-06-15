#!/usr/bin/env bash
# Initial setup script: creates an 800×600 image with colourful rectangles.
# The user’s task will be to pixel-ate the whole image into 10×10 px blocks.
set -e

XCF_PATH="/tmp/pixelate_task.xcf"

# Generate the initial XCF in batch mode
gimp -i -b "
(let* ((img (car (gimp-image-new 800 600 RGB)))
       (bg  (car (gimp-layer-new img 800 600 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL))))
  ;; Add layer to image
  (gimp-image-insert-layer img bg 0 0)

  ;; Fill full background with bright green
  (gimp-context-set-foreground '(65 236 16))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Big red rectangle
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 150 150 300 200)
  (gimp-context-set-foreground '(255 0 0))
  (gimp-edit-fill bg FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Small blue square
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 50 50 100 100)
  (gimp-context-set-foreground '(0 0 255))
  (gimp-edit-fill bg FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Save and quit
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0))
" >/dev/null 2>&1

# Open the file for the user
DISPLAY=:0 gimp "${XCF_PATH}" &