#!/usr/bin/env bash
# Initial setup script: creates a 1200×1200 image where the active
# “SALE 50% OFF” layer is buried under a “Product Photo” layer.

XCF_PATH="/tmp/sale_layer_order_task.xcf"

gimp -i -b "
(let* (
       ;; 1. Create the base image
       (img  (car (gimp-image-new 1200 1200 RGB)))

       ;; 2. Background (bottom layer)
       (bg   (car (gimp-layer-new img 1200 1200 RGB-IMAGE \"Background\" 100 LAYER-MODE-NORMAL)))

       ;; 3. Product Photo (will be on top of Background)
       (prod (car (gimp-layer-new img 1200 1200 RGB-IMAGE \"Product Photo\" 100 LAYER-MODE-NORMAL)))

       ;; 4. SALE text layer – inserted *under* the product layer but it becomes the active layer
       (sale (car (gimp-layer-new img 1200 1200 RGB-IMAGE \"SALE 50% OFF\" 100 LAYER-MODE-NORMAL)))
      )

  ;; Insert layers in the correct order
  (gimp-image-insert-layer img bg   0 0)   ;; Background first (index 0)
  (gimp-context-set-foreground '(255 255 255))
  (gimp-edit-fill bg FILL-FOREGROUND)

  (gimp-image-insert-layer img prod 0 0)   ;; Product now at top (index 0)
  (gimp-context-set-foreground '(0 120 220))
  (gimp-edit-fill prod FILL-FOREGROUND)

  (gimp-image-insert-layer img sale 0 1)   ;; SALE inserted at index 1 (below Product)
  (gimp-context-set-foreground '(255 0 0))
  (gimp-edit-fill sale FILL-FOREGROUND)
  ;; ‘sale’ is now the ACTIVE layer but visually hidden by ‘prod’

  ;; Save and quit batch mode
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"${XCF_PATH}\" \"${XCF_PATH}\")
  (gimp-quit 0)
)" >/dev/null 2>&1

# Open the generated XCF so the user immediately sees the file
DISPLAY=:0 gimp "${XCF_PATH}" &