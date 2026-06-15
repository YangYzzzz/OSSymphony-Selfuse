#!/usr/bin/env bash
# Initial Setup Script: creates a gray logo that needs thresholding
XCF_PATH="/tmp/threshold_logo.xcf"
WIDTH=400
HEIGHT=400

# Create the initial XCF in batch mode
gimp -i -b "
(let* ((img (car (gimp-image-new ${WIDTH} ${HEIGHT} RGB)))               ; New RGB image
       (bg  (car (gimp-layer-new img ${WIDTH} ${HEIGHT} RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))
      )
  (gimp-image-insert-layer img bg 0 0)                                   ; Add background layer
  (gimp-context-set-foreground '(255 255 255))                           ; Set FG to white
  (gimp-edit-fill bg FILL-FOREGROUND)                                    ; Fill background white

  ;; Draw a mid-gray rectangle simulating a scanned logo
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 100 50 200 300)    ; Select rectangle
  (gimp-context-set-foreground '(150 150 150))                           ; Mid-gray color
  (gimp-edit-fill bg FILL-FOREGROUND)                                    ; Fill rectangle gray
  (gimp-selection-none img)                                              ; Clear selection

  ;; Save and quit
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0)
)
" >/dev/null 2>&1

# Open the generated XCF for user interaction
DISPLAY=:0 gimp "${XCF_PATH}" &