#!/usr/bin/env bash
# Initial setup script – prepares the canvas that still needs the 200 × 300 px selection

XCF_PATH="/tmp/rect_selection_task.xcf"

# 1) Create the initial image via Script-Fu (non-interactive)
gimp -i -b "
(let* ((img      (car (gimp-image-new 800 600 RGB)))                                   ; new 800×600 RGB image
       (bg       (car (gimp-layer-new img 800 600 RGB-IMAGE  \"Background\" 100 LAYER-MODE-NORMAL)))
       (overlay  (car (gimp-layer-new img 800 600 RGBA-IMAGE \"Highlight\"  100 LAYER-MODE-NORMAL))))
  ;; Insert layers
  (gimp-image-insert-layer img bg      0 0)
  (gimp-image-insert-layer img overlay 0 0)

  ;; Fill the background with a light blue tone
  (gimp-context-set-foreground '(200 200 255))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Draw a visual hint rectangle (but remove selection afterwards)
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 300 150 200 300)  ; x=300 y=150 w=200 h=300
  (gimp-context-set-foreground '(241 241 159))
  (gimp-edit-fill overlay FILL-FOREGROUND)
  (gimp-selection-none img)                                             ; clear selection for the task

  ;; Save and quit
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0))
" >/dev/null 2>&1

# 2) Open the generated file in GUI so the trainee can work
DISPLAY=:0 gimp "${XCF_PATH}" &