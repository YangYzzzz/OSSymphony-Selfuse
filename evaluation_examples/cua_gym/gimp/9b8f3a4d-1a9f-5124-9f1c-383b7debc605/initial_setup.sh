#!/usr/bin/env bash
# ------------------------------------------------------------
# Initial setup script: generates a 2400×2400 image with
# a white background and a red “logo” rectangle positioned
# 30 px from the top-left corner (user must move it to the
# bottom-right and reduce opacity later).
# ------------------------------------------------------------
XCF_PATH="/tmp/product_logo_task.xcf"

# Create the initial XCF file via Script-Fu in batch mode
gimp -i -b "
(let* ((img  (car (gimp-image-new 2400 2400 RGB)))
       (bg   (car (gimp-layer-new img 2400 2400 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))
       (logo (car (gimp-layer-new img 2400 2400 RGB-IMAGE \"Logo\"       100 LAYER-MODE-NORMAL))))
  ;; Insert layers
  (gimp-image-insert-layer img bg   0 0)
  (gimp-image-insert-layer img logo 0 0)

  ;; Fill background white
  (gimp-context-set-foreground '(255 255 255))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Draw the logo rectangle at (30,30)
  (gimp-context-set-foreground '(200 0 0))
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 30 30 300 100)
  (gimp-edit-fill logo FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Save XCF
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")

  ;; Quit batch mode
  (gimp-quit 0))" >/dev/null 2>&1

# Open the file in the regular GIMP GUI for user interaction
DISPLAY=:0 gimp "${XCF_PATH}" &