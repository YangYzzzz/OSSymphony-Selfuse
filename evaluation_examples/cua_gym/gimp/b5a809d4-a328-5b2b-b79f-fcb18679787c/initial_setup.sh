#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Initial Setup Script
# Creates a single high-resolution “product shot” XCF that still needs to be
# resized to 1024×1024 px, converted to WebP (quality 80) and stripped of
# metadata.  The file opens automatically in the running GIMP GUI so the
# learner can perform the required batch-conversion steps manually.
# -----------------------------------------------------------------------------

XCF_PATH="/tmp/product_batch_conversion.xcf"
WIDTH=1600       # larger than the required 1024×1024 so resizing is necessary
HEIGHT=1600

# Remove any previous file to avoid stale data
rm -f "$XCF_PATH"

# ------------------------------------------------------------------
# Use GIMP in batch mode to generate the initial XCF via Script-Fu
# ------------------------------------------------------------------
gimp -i -b "
(let* (
       ;; Create a new RGB image
       (img  (car (gimp-image-new ${WIDTH} ${HEIGHT} RGB)))
       
       ;; Add one layer representing a single product shot
       (prod (car (gimp-layer-new img ${WIDTH} ${HEIGHT} RGB-IMAGE \"ProductShot\" 100 LAYER-MODE-NORMAL)))
      )
  ;; Insert layer into image
  (gimp-image-insert-layer img prod 0 0)
  
  ;; Give the layer a light-gray fill to mimic a product background
  (gimp-context-set-foreground '(230 230 230))
  (gimp-edit-fill prod FILL-FOREGROUND)

  ;; Save to XCF
  (gimp-xcf-save RUN-NONINTERACTIVE img prod \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0)
)" >/dev/null 2>&1

# ---------------------------------------------------------------
# Automatically open the generated file in the desktop GIMP GUI
# ---------------------------------------------------------------
DISPLAY=:0 gimp "${XCF_PATH}" &