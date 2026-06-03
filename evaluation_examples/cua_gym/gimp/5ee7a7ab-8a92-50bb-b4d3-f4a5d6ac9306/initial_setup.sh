#!/usr/bin/env bash
# Initial setup script: two texture layers, top layer at 100 % opacity
XCF_PATH="/tmp/blend_opacity_task.xcf"

gimp -i -b "
(let* ((img  (car (gimp-image-new 800 600 RGB)))
       (base (car (gimp-layer-new img 800 600 RGB-IMAGE \"Base Texture\" 100 LAYER-MODE-NORMAL)))
       (top  (car (gimp-layer-new img 800 600 RGB-IMAGE \"Top Texture\" 100 LAYER-MODE-NORMAL))))
  ;; Insert layers
  (gimp-image-insert-layer img base 0 0)
  (gimp-image-insert-layer img top 0 0)

  ;; Fill base layer with medium gray
  (gimp-context-set-foreground '(120 120 120))
  (gimp-edit-fill base FILL-FOREGROUND)

  ;; Fill top layer with red
  (gimp-context-set-foreground '(200 50 50))
  (gimp-edit-fill top FILL-FOREGROUND)

  ;; Save and quit
  (gimp-xcf-save RUN-NONINTERACTIVE img base \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0))" >/dev/null 2>&1

# Open the file for the user to perform the task
DISPLAY=:0 gimp "${XCF_PATH}" &