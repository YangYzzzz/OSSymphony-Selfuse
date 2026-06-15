#!/usr/bin/env bash
# Initial Setup Script: creates an 800×800 graphic that needs canvas expansion
XCF_PATH="/tmp/instagram_canvas_task.xcf"

gimp -i -b "
(let* ((img (car (gimp-image-new 800 800 RGB)))
       (bg  (car (gimp-layer-new img 800 800 RGB-IMAGE \"Graphic\" 100 LAYER-MODE-NORMAL)))
      )
  (gimp-image-insert-layer img bg 0 0)
  (gimp-context-set-foreground '(0 120 200))  ; blue fill
  (gimp-edit-fill bg FILL-FOREGROUND)
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"$XCF_PATH\" \"$XCF_PATH\")
  (gimp-quit 0))" >/dev/null 2>&1

# Open the generated XCF for the user
DISPLAY=:0 gimp "$XCF_PATH" &