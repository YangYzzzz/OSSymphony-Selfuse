#!/usr/bin/env bash
# ------------------------------------------------------------
# Initial Setup Script
# Generates a 300×300 px XCF with two placeholder “product” layers.
# The user must create a 150×150 px thumbnail version and export it.
# ------------------------------------------------------------
XCF_PATH="/tmp/product_thumbnail_task.xcf"

# Ensure a clean start
rm -f "$XCF_PATH"

gimp -i -b "
(let* ((img    (car (gimp-image-new 300 300 RGB))) ; create base image
       (prodA  (car (gimp-layer-new img 300 300 RGB-IMAGE \"product_A\" 100 LAYER-MODE-NORMAL)))
       (prodB  (car (gimp-layer-new img 300 300 RGB-IMAGE \"product_B\" 100 LAYER-MODE-NORMAL))))
  ;; Insert layers
  (gimp-image-insert-layer img prodA 0 0)
  (gimp-image-insert-layer img prodB 0 1)
  ;; Fill each layer with a solid color so they’re visually distinct
  (gimp-context-set-foreground '(255 0 0))
  (gimp-edit-fill prodA FILL-FOREGROUND)
  (gimp-context-set-foreground '(0 0 255))
  (gimp-edit-fill prodB FILL-FOREGROUND)
  ;; Save the initial state
  (gimp-xcf-save RUN-NONINTERACTIVE img prodA \"$XCF_PATH\" \"$XCF_PATH\")
  (gimp-quit 0))" >/dev/null 2>&1

# Open the generated file for user interaction
DISPLAY=:0 gimp "$XCF_PATH" &