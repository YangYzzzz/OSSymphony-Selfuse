#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# Initial setup script
# Generates a 1200×628 px banner with a headline “placeholder”
# layer that still needs a drop-shadow effect.
# ──────────────────────────────────────────────────────────────
XCF_PATH="/tmp/web_banner_shadow.xcf"

gimp -i -b "
(let* ((img       (car (gimp-image-new 1200 628 RGB)))
       (bg        (car (gimp-layer-new img 1200 628 RGB-IMAGE  \"Background\" 100 LAYER-MODE-NORMAL)))
       (headline  (car (gimp-layer-new img 1200 628 RGBA-IMAGE \"Headline\"   100 LAYER-MODE-NORMAL))))
  ;; layer stack ─ background at bottom, headline on top
  (gimp-image-insert-layer img bg       0 0)
  (gimp-image-insert-layer img headline 0 1)

  ;; background colour
  (gimp-context-set-foreground '(200 220 240))
  (gimp-edit-fill bg FILL-FOREGROUND)

  ;; draw the white “headline” rectangle (pretends to be text)
  (gimp-image-select-rectangle img CHANNEL-OP-REPLACE 200 200 800 80)
  (gimp-context-set-foreground '(255 255 255))
  (gimp-edit-fill headline FILL-FOREGROUND)
  (gimp-selection-none img)

  ;; save & quit
  (gimp-xcf-save RUN-NONINTERACTIVE img bg \"$XCF_PATH\" \"$XCF_PATH\")
  (gimp-quit 0))"  >/dev/null 2>&1

# open the generated file for the user
DISPLAY=:0 gimp "$XCF_PATH" &