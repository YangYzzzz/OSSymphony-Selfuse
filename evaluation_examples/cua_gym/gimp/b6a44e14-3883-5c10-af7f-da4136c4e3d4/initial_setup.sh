#!/usr/bin/env bash
# Initial Setup Script: creates a low-contrast image that looks “washed-out”

XCF_PATH="/tmp/contrast_boost_task.xcf"

# --- Generate the initial low-contrast XCF in batch mode ---
gimp -i -b "
(let* (
       ;; Create a new 800×600 RGB image
       (img (car (gimp-image-new 800 600 RGB)))

       ;; Add a single background layer
       (bg  (car (gimp-layer-new img 800 600 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL))
       ))

  ;; Insert the layer as the bottom layer
  (gimp-image-insert-layer img bg 0 0)

  ;; Fill the whole layer with a very light gray (washed-out)
  (gimp-context-set-foreground '(200 200 200))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Make a subtle darker rectangle on the left half (still low contrast)
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 0 0 400 600)
  (gimp-context-set-foreground '(160 160 160))
  (gimp-edit-fill bg FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Save the XCF file
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")

  ;; Exit GIMP
  (gimp-quit 0)
)" >/dev/null 2>&1

# --- Open the generated XCF for the user ---
DISPLAY=:0 gimp "${XCF_PATH}" &