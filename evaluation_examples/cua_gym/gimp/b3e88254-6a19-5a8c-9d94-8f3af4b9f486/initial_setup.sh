#!/usr/bin/env bash
# ------------------------------------------------------------
# Initial setup script for the “Save As” task.
# It creates a multi-layer mock-up and stores it as /tmp/mockup_start.xcf,
# then opens it in the GUI so the user can perform “File ▸ Save As…”
# to /tmp/website_mockup.xcf
# ------------------------------------------------------------
XCF_PATH="/tmp/mockup_start.xcf"

# Run GIMP in batch mode to generate the starting file
gimp -i -b "
(let* ((img     (car (gimp-image-new 960 540 RGB)))                              ; New RGB image
       (bg      (car (gimp-layer-new img 960 540 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))
       (header  (car (gimp-layer-new img 960 100 RGB-IMAGE \"Header\" 100 LAYER-MODE-NORMAL))))
  ;; Insert layers
  (gimp-image-insert-layer img bg     0 0)
  (gimp-image-insert-layer img header 0 1)

  ;; Fill layers with simple flat colours
  (gimp-context-set-foreground '(240 240 240))   ; Light grey background
  (gimp-edit-fill bg FILL-FOREGROUND)

  (gimp-context-set-foreground '(30 120 200))    ; Blue header bar
  (gimp-edit-fill header FILL-FOREGROUND)

  ;; Save the starting file
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")

  ;; Quit batch mode
  (gimp-quit 0)
)" >/dev/null 2>&1

# Open the file for the trainee
DISPLAY=:0 gimp "${XCF_PATH}" &