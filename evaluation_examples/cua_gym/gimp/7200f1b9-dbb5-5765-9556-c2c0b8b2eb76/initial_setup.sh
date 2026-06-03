#!/usr/bin/env bash
# Initial Setup Script: creates a single 4000×3000 image that still needs to be scaled
XCF_PATH="/tmp/batch_resize_task.xcf"

# Run GIMP in batch mode to create the initial file
gimp -i -b '
(let* ((img  (car (gimp-image-new 4000 3000 RGB)))                           ; create 4000×3000 RGB image
       (bg   (car (gimp-layer-new img 4000 3000 RGB-IMAGE                   ; background layer
                                   "Background" 100 LAYER-MODE-NORMAL))))
  (gimp-image-insert-layer img bg 0 0)                                      ; add layer to image
  (gimp-context-set-foreground '\''(117 199 174))                           ; set a pleasant teal tone
  (gimp-edit-fill bg FILL-FOREGROUND)                                       ; fill layer with the color
  (gimp-xcf-save RUN-NONINTERACTIVE img bg                                  ; save the XCF
                 "/tmp/batch_resize_task.xcf"
                 "/tmp/batch_resize_task.xcf")
  (gimp-quit 0))' >/dev/null 2>&1

# Open the generated file in a normal GIMP window for user interaction
DISPLAY=:0 gimp "$XCF_PATH" &