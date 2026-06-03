#!/usr/bin/env bash
# ------------------------------------------------------------
# Initial setup script for “Flood-Fill Selection with Brand Orange”
# ------------------------------------------------------------
XCF_PATH="/tmp/flood_fill_orange_task.xcf"

# Remove any previous file with the same name
rm -f "$XCF_PATH"

# Run GIMP in batch-mode to create the initial file
gimp -i -b "
(let* (
       ;; 1. Create a new 800×600 RGB image
       (img (car (gimp-image-new 800 600 RGB)))

       ;; 2. Add a single background layer
       (bg  (car (gimp-layer-new img        ; image ID
                                 800 600    ; width height
                                 RGB-IMAGE  ; layer type
                                 \"Background\" ; name
                                 100        ; opacity
                                 LAYER-MODE-NORMAL)))) ; mode
  (gimp-image-insert-layer img bg 0 0)

  ;; 3. Fill the layer with a neutral grey
  (gimp-context-set-foreground '(200 200 200))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; 4. Create a rectangular selection (remains active on open)
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE
                               200 150     ; X Y
                               400 300)    ; Width Height

  ;; 5. Save the image as XCF
  (gimp-xcf-save RUN-NONINTERACTIVE img bg
                 \"$XCF_PATH\" \"$XCF_PATH\")

  ;; 6. Quit batch mode
  (gimp-quit 0))
" >/dev/null 2>&1

# 7. Open the generated file for the user
DISPLAY=:0 gimp "$XCF_PATH" &