#!/usr/bin/env bash
# ----------------------------------------------------------
# Initial setup script: creates a multi-layer 2048×2048 image
# ----------------------------------------------------------
XCF_PATH="/tmp/merge_visible_layers_task.xcf"

# Run GIMP in batch mode to build the initial file
gimp -i -b "
(let* ((img   (car (gimp-image-new 2048 2048 RGB)))
       (bg    (car (gimp-layer-new img 2048 2048 RGB-IMAGE \"Background\"    100 LAYER-MODE-NORMAL)))
       (rect  (car (gimp-layer-new img 2048 2048 RGB-IMAGE \"Red Rectangle\" 100 LAYER-MODE-NORMAL)))
       (sq    (car (gimp-layer-new img 2048 2048 RGB-IMAGE \"Blue Square\"   100 LAYER-MODE-NORMAL)))
      )

  ;; Insert layers (Background at bottom, others above)
  (gimp-image-insert-layer img bg   0 0)
  (gimp-image-insert-layer img rect 0 1)
  (gimp-image-insert-layer img sq   0 2)

  ;; Background – white fill
  (gimp-context-set-foreground '(255 255 255))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; Red rectangle layer – centred 1200×1200 rectangle
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 400 400 1200 1200)
  (gimp-context-set-foreground '(255 0 0))
  (gimp-edit-fill rect FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Blue square layer – centred 600×600 square
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 700 700 600 600)
  (gimp-context-set-foreground '(0 0 255))
  (gimp-edit-fill sq FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; Save the XCF
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0)
)" >/dev/null 2>&1

# Open the file in the GUI so the trainee can perform the task
DISPLAY=:0 gimp "${XCF_PATH}" &