#!/usr/bin/env bash
# Initial setup: create an image that contains a 512×512 “Logo” layer and a background.
XCF_PATH="/tmp/logo_export_task.xcf"

gimp -i -b "
(let* ((img  (car (gimp-image-new 1024 768 RGB)))                       ; create 1024×768 RGB image
       (bg   (car (gimp-layer-new img 1024 768 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))
       (logo (car (gimp-layer-new img 512 512 RGBA-IMAGE \"Logo\" 100 LAYER-MODE-NORMAL))))
  (gimp-image-insert-layer img bg   0 0)                                ; insert background
  (gimp-image-insert-layer img logo 0 1)                                ; insert logo above background
  (gimp-context-set-foreground '(255 255 255))                          ; white background
  (gimp-edit-fill bg FILL-FOREGROUND)
  (gimp-context-set-foreground '(0 120 200))                            ; blue logo block
  (gimp-edit-fill logo FILL-FOREGROUND)
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\") ; save XCF
  (gimp-quit 0))" >/dev/null 2>&1

# Open the generated XCF for the user
DISPLAY=:0 gimp "${XCF_PATH}" &