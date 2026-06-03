#!/usr/bin/env bash
# -----------------------------------------------------------
# Initial setup script for “Color Grading backup” duplication task
# -----------------------------------------------------------

XCF_PATH="/tmp/color_grading_poster.xcf"

# Create the initial XCF in non-interactive batch mode
gimp -i -b "
(let* ((img      (car (gimp-image-new 2400 3000 RGB)))                       ; 2400×3000 px RGB image
       (bg       (car (gimp-layer-new img 2400 3000 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))
       (grading  (car (gimp-layer-new img 2400 3000 RGB-IMAGE \"Color Grading\" 100 LAYER-MODE-NORMAL))))
  ;; Insert layers: Background at bottom, Color Grading on top (active layer)
  (gimp-image-insert-layer img bg 0 0)
  (gimp-image-insert-layer img grading 0 0)

  ;; Fill Background with white
  (gimp-context-set-foreground '(255 255 255))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Give the Color Grading layer a distinctive blue tint
  (gimp-context-set-foreground '(24 43 183))
  (gimp-edit-fill grading FILL-FOREGROUND)

  ;; Save to XCF
  (gimp-xcf-save RUN-NONINTERACTIVE img grading \"${XCF_PATH}\" \"${XCF_PATH}\")

  ;; Quit batch mode
  (gimp-quit 0))" >/dev/null 2>&1

# Open the generated XCF so the user can start working
DISPLAY=:0 gimp "${XCF_PATH}" &