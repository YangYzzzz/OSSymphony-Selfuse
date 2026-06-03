#!/usr/bin/env bash
# Initial setup script: generates a horizontally-mirrored “selfie”
XCF_PATH="/tmp/flip_selfie_task.xcf"

# Remove any existing file with the same name
rm -f "$XCF_PATH"

# Create the initial (mirrored) image in batch mode
gimp -i -b "
(let* ((img   (car (gimp-image-new 640 480 RGB)))                                   ; create image
       (layer (car (gimp-layer-new img 640 480 RGB-IMAGE \"Selfie\" 100 LAYER-MODE-NORMAL)))
      )
  (gimp-image-insert-layer img layer 0 0)                                            ; add layer

  ;; Fill entire layer white
  (gimp-context-set-foreground '(255 255 255))
  (gimp-selection-all img)
  (gimp-edit-fill layer FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; LEFT half (0–319) — RED  ➜ represents phone in “left” hand
  (gimp-context-set-foreground '(200 50 50))
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 0 0 320 480)
  (gimp-edit-fill layer FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; RIGHT half (320–639) — BLUE
  (gimp-context-set-foreground '(50 50 200))
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 320 0 320 480)
  (gimp-edit-fill layer FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Save and quit
  (gimp-xcf-save RUN-NONINTERACTIVE img layer \"$XCF_PATH\" \"$XCF_PATH\")
  (gimp-quit 0)
)" >/dev/null 2>&1

# Open the generated file for the user
DISPLAY=:0 gimp "$XCF_PATH" &