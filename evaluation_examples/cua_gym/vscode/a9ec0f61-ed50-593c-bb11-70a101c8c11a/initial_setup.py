"""
Initial Setup: Sort the Outline view by position and navigate a complex CSS file.
Task ID: vscode_code_077
Domain: vs_code

Creates a CSS file with 200+ CSS rules organized in sections, then opens VSCode with it.
The VSCode Outline view should be in default (alphabetical) sort order initially.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_077'
CSS_DIR = '/home/user/web'
CSS_FILE = '/home/user/web/components.css'

VSCODE_USER = os.path.join('/home/user', '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_css_file():
    os.makedirs(CSS_DIR, exist_ok=True)

    css_content = """\
/* =============================================================================
   components.css — Full UI Component Library
   Version: 3.1.0
   Description: Comprehensive CSS component system for web applications
   ============================================================================= */

/* =============================================================================
   1. RESET & BASE STYLES
   ============================================================================= */

/* Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  font-size: 1rem;
  line-height: 1.5;
  color: #212529;
  background-color: #ffffff;
}

/* =============================================================================
   2. LAYOUT COMPONENTS
   ============================================================================= */

/* Layout */
.container {
  width: 100%;
  max-width: 1200px;
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
}

.container-fluid {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

.container-sm {
  max-width: 576px;
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
}

.container-md {
  max-width: 768px;
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
}

.container-lg {
  max-width: 992px;
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
}

.container-xl {
  max-width: 1400px;
  margin-right: auto;
  margin-left: auto;
  padding-right: 15px;
  padding-left: 15px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.flex {
  display: flex;
}

.flex-wrap {
  display: flex;
  flex-wrap: wrap;
}

.flex-col {
  display: flex;
  flex-direction: column;
}

.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.flex-start {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.flex-end {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* =============================================================================
   3. TYPOGRAPHY
   ============================================================================= */

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1rem;
  color: #1a1a2e;
  letter-spacing: -0.025em;
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 0.875rem;
  color: #1a1a2e;
  letter-spacing: -0.02em;
}

h3 {
  font-size: 1.75rem;
  font-weight: 600;
  line-height: 1.35;
  margin-bottom: 0.75rem;
  color: #2d2d44;
}

h4 {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 0.625rem;
  color: #2d2d44;
}

h5 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.45;
  margin-bottom: 0.5rem;
  color: #3d3d5c;
}

h6 {
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5;
  margin-bottom: 0.5rem;
  color: #3d3d5c;
}

p {
  margin-bottom: 1rem;
  line-height: 1.7;
  color: #495057;
}

.lead {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 1.6;
  color: #6c757d;
}

.text-muted {
  color: #6c757d !important;
}

.text-primary {
  color: #0d6efd !important;
}

.text-secondary {
  color: #6c757d !important;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.text-info {
  color: #0dcaf0 !important;
}

.text-light {
  color: #f8f9fa !important;
}

.text-dark {
  color: #212529 !important;
}

.text-white {
  color: #ffffff !important;
}

a {
  color: #0d6efd;
  text-decoration: underline;
}

a:hover {
  color: #0a58ca;
  text-decoration: underline;
}

/* =============================================================================
   4. BUTTONS
   ============================================================================= */

.btn {
  display: inline-block;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  background-color: transparent;
  border: 1px solid transparent;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  border-radius: 0.375rem;
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn:hover {
  color: #212529;
}

.btn:focus {
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.btn:disabled {
  pointer-events: none;
  opacity: 0.65;
}

.btn-primary {
  color: #ffffff;
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  color: #ffffff;
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.btn-primary:focus {
  color: #ffffff;
  background-color: #0b5ed7;
  border-color: #0a58ca;
  box-shadow: 0 0 0 0.25rem rgba(49, 132, 253, 0.5);
}

.btn-secondary {
  color: #ffffff;
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  color: #ffffff;
  background-color: #5c636a;
  border-color: #565e64;
}

.btn-secondary:focus {
  color: #ffffff;
  background-color: #5c636a;
  border-color: #565e64;
  box-shadow: 0 0 0 0.25rem rgba(130, 138, 145, 0.5);
}

.btn-success {
  color: #ffffff;
  background-color: #198754;
  border-color: #198754;
}

.btn-success:hover {
  color: #ffffff;
  background-color: #157347;
  border-color: #146c43;
}

.btn-danger {
  color: #ffffff;
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  color: #ffffff;
  background-color: #bb2d3b;
  border-color: #b02a37;
}

.btn-warning {
  color: #000000;
  background-color: #ffc107;
  border-color: #ffc107;
}

.btn-warning:hover {
  color: #000000;
  background-color: #ffca2c;
  border-color: #ffc720;
}

.btn-info {
  color: #000000;
  background-color: #0dcaf0;
  border-color: #0dcaf0;
}

.btn-info:hover {
  color: #000000;
  background-color: #31d2f2;
  border-color: #25cff2;
}

.btn-light {
  color: #000000;
  background-color: #f8f9fa;
  border-color: #f8f9fa;
}

.btn-light:hover {
  color: #000000;
  background-color: #f9fafb;
  border-color: #f9fafb;
}

.btn-dark {
  color: #ffffff;
  background-color: #212529;
  border-color: #212529;
}

.btn-dark:hover {
  color: #ffffff;
  background-color: #1c1f23;
  border-color: #1a1e21;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-primary:hover {
  color: #ffffff;
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #6c757d;
}

.btn-outline-secondary:hover {
  color: #ffffff;
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.25rem;
}

.btn-lg {
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  border-radius: 0.5rem;
}

/* =============================================================================
   5. FORMS
   ============================================================================= */

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  background-color: #ffffff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  appearance: none;
  border-radius: 0.375rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  color: #212529;
  background-color: #ffffff;
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-control:disabled {
  background-color: #e9ecef;
  opacity: 1;
}

.form-control::placeholder {
  color: #6c757d;
  opacity: 1;
}

.form-control-sm {
  min-height: calc(1.5em + 0.5rem + 2px);
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.25rem;
}

.form-control-lg {
  min-height: calc(1.5em + 1rem + 2px);
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  border-radius: 0.5rem;
}

.form-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-text {
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #6c757d;
}

.form-check {
  display: block;
  min-height: 1.5rem;
  padding-left: 1.5em;
  margin-bottom: 0.125rem;
}

.form-check-input {
  float: left;
  margin-left: -1.5em;
  width: 1em;
  height: 1em;
  margin-top: 0.25em;
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.25);
  border-radius: 0.25em;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-check-label {
  cursor: pointer;
  color: #374151;
}

.form-select {
  display: block;
  width: 100%;
  padding: 0.375rem 2.25rem 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  background-color: #ffffff;
  border: 1px solid #ced4da;
  border-radius: 0.375rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  appearance: none;
}

.form-select:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.invalid-feedback {
  display: none;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #dc3545;
}

.valid-feedback {
  display: none;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #198754;
}

/* =============================================================================
   6. CARDS
   ============================================================================= */

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #ffffff;
  background-clip: border-box;
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.card-header {
  padding: 1rem 1.25rem;
  margin-bottom: 0;
  background-color: rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
  font-weight: 600;
}

.card-header:first-child {
  border-radius: calc(0.5rem - 1px) calc(0.5rem - 1px) 0 0;
}

.card-body {
  flex: 1 1 auto;
  padding: 1.25rem;
}

.card-title {
  margin-bottom: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1a1a2e;
}

.card-subtitle {
  margin-top: -0.25rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.card-text {
  margin-bottom: 1rem;
  color: #495057;
}

.card-footer {
  padding: 0.75rem 1.25rem;
  background-color: rgba(0, 0, 0, 0.03);
  border-top: 1px solid rgba(0, 0, 0, 0.125);
}

.card-footer:last-child {
  border-radius: 0 0 calc(0.5rem - 1px) calc(0.5rem - 1px);
}

.card-img {
  width: 100%;
  border-radius: calc(0.5rem - 1px);
}

.card-img-top {
  width: 100%;
  border-top-left-radius: calc(0.5rem - 1px);
  border-top-right-radius: calc(0.5rem - 1px);
}

.card-img-bottom {
  width: 100%;
  border-bottom-right-radius: calc(0.5rem - 1px);
  border-bottom-left-radius: calc(0.5rem - 1px);
}

.card-link {
  color: #0d6efd;
  text-decoration: none;
}

.card-link:hover {
  color: #0a58ca;
}

/* =============================================================================
   7. NAVIGATION
   ============================================================================= */

.nav {
  display: flex;
  flex-wrap: wrap;
  padding-left: 0;
  margin-bottom: 0;
  list-style: none;
}

.nav-link {
  display: block;
  padding: 0.5rem 1rem;
  color: #0d6efd;
  text-decoration: none;
  transition: color 0.15s ease-in-out;
}

.nav-link:hover {
  color: #0a58ca;
}

.nav-link:focus {
  outline: 0;
  color: #0a58ca;
}

.nav-link.active {
  color: #0d6efd;
  font-weight: 600;
}

.nav-link.disabled {
  color: #6c757d;
  pointer-events: none;
  cursor: default;
}

.nav-tabs {
  border-bottom: 1px solid #dee2e6;
}

.nav-tabs .nav-link {
  margin-bottom: -1px;
  background: none;
  border: 1px solid transparent;
  border-top-left-radius: 0.375rem;
  border-top-right-radius: 0.375rem;
}

.nav-tabs .nav-link:hover {
  border-color: #e9ecef #e9ecef #dee2e6;
  isolation: isolate;
}

.nav-tabs .nav-link.active {
  color: #495057;
  background-color: #ffffff;
  border-color: #dee2e6 #dee2e6 #ffffff;
}

.nav-pills .nav-link {
  background: none;
  border: 0;
  border-radius: 0.375rem;
}

.nav-pills .nav-link.active {
  color: #ffffff;
  background-color: #0d6efd;
}

.navbar {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem;
}

.navbar-brand {
  padding-top: 0.3125rem;
  padding-bottom: 0.3125rem;
  margin-right: 1rem;
  font-size: 1.25rem;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
}

.navbar-nav {
  display: flex;
  flex-direction: column;
  padding-left: 0;
  margin-bottom: 0;
  list-style: none;
}

/* =============================================================================
   8. MODALS
   ============================================================================= */

.modal {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1055;
  display: none;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  outline: 0;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1050;
  width: 100vw;
  height: 100vh;
  background-color: #000000;
}

.modal-backdrop.fade {
  opacity: 0;
}

.modal-backdrop.show {
  opacity: 0.5;
}

.modal-dialog {
  position: relative;
  width: auto;
  margin: 0.5rem;
  pointer-events: none;
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  pointer-events: auto;
  background-color: #ffffff;
  background-clip: padding-box;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
  outline: 0;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  border-top-left-radius: calc(0.5rem - 1px);
  border-top-right-radius: calc(0.5rem - 1px);
}

.modal-title {
  margin-bottom: 0;
  line-height: 1.5;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-body {
  position: relative;
  flex: 1 1 auto;
  padding: 1rem;
}

.modal-footer {
  display: flex;
  flex-wrap: wrap;
  flex-shrink: 0;
  align-items: center;
  justify-content: flex-end;
  padding: 0.75rem;
  border-top: 1px solid #dee2e6;
  border-bottom-right-radius: calc(0.5rem - 1px);
  border-bottom-left-radius: calc(0.5rem - 1px);
  gap: 0.5rem;
}

/* =============================================================================
   9. ALERTS
   ============================================================================= */

.alert {
  position: relative;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.375rem;
}

.alert-primary {
  color: #084298;
  background-color: #cfe2ff;
  border-color: #b6d4fe;
}

.alert-secondary {
  color: #41464b;
  background-color: #e2e3e5;
  border-color: #d3d6d8;
}

.alert-success {
  color: #0f5132;
  background-color: #d1e7dd;
  border-color: #badbcc;
}

.alert-danger {
  color: #842029;
  background-color: #f8d7da;
  border-color: #f5c2c7;
}

.alert-warning {
  color: #664d03;
  background-color: #fff3cd;
  border-color: #ffecb5;
}

.alert-info {
  color: #055160;
  background-color: #cff4fc;
  border-color: #b6effb;
}

.alert-light {
  color: #636464;
  background-color: #fefefe;
  border-color: #fdfdfe;
}

.alert-dark {
  color: #141619;
  background-color: #d3d3d4;
  border-color: #bcbebf;
}

.alert-heading {
  color: inherit;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.alert-link {
  font-weight: 700;
}

.alert-dismissible {
  padding-right: 3rem;
}

/* =============================================================================
   10. BADGES
   ============================================================================= */

.badge {
  display: inline-block;
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 700;
  line-height: 1;
  color: #ffffff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.375rem;
}

.badge-primary {
  background-color: #0d6efd;
}

.badge-secondary {
  background-color: #6c757d;
}

.badge-success {
  background-color: #198754;
}

.badge-danger {
  background-color: #dc3545;
}

.badge-warning {
  color: #000000;
  background-color: #ffc107;
}

.badge-info {
  color: #000000;
  background-color: #0dcaf0;
}

.badge-light {
  color: #000000;
  background-color: #f8f9fa;
}

.badge-dark {
  background-color: #212529;
}

.badge-pill {
  border-radius: 50rem;
}

/* =============================================================================
   11. TABLES
   ============================================================================= */

.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
  vertical-align: top;
  border-color: #dee2e6;
}

.table > :not(caption) > * > * {
  padding: 0.5rem;
  border-bottom-width: 1px;
  box-shadow: inset 0 0 0 9999px transparent;
}

.table-striped > tbody > tr:nth-of-type(odd) > * {
  background-color: rgba(0, 0, 0, 0.05);
}

.table-hover > tbody > tr:hover > * {
  background-color: rgba(0, 0, 0, 0.075);
}

.table-bordered > :not(caption) > * {
  border-width: 1px 0;
}

.table-bordered > :not(caption) > * > * {
  border-width: 0 1px;
}

.table-sm > :not(caption) > * > * {
  padding: 0.25rem;
}

.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* =============================================================================
   12. UTILITIES
   ============================================================================= */

.d-none {
  display: none !important;
}

.d-inline {
  display: inline !important;
}

.d-inline-block {
  display: inline-block !important;
}

.d-block {
  display: block !important;
}

.d-flex {
  display: flex !important;
}

.d-grid {
  display: grid !important;
}

.d-table {
  display: table !important;
}

.mt-0 { margin-top: 0 !important; }
.mt-1 { margin-top: 0.25rem !important; }
.mt-2 { margin-top: 0.5rem !important; }
.mt-3 { margin-top: 1rem !important; }
.mt-4 { margin-top: 1.5rem !important; }
.mt-5 { margin-top: 3rem !important; }

.mb-0 { margin-bottom: 0 !important; }
.mb-1 { margin-bottom: 0.25rem !important; }
.mb-2 { margin-bottom: 0.5rem !important; }
.mb-3 { margin-bottom: 1rem !important; }
.mb-4 { margin-bottom: 1.5rem !important; }
.mb-5 { margin-bottom: 3rem !important; }

.ms-0 { margin-left: 0 !important; }
.ms-1 { margin-left: 0.25rem !important; }
.ms-2 { margin-left: 0.5rem !important; }
.ms-3 { margin-left: 1rem !important; }
.ms-4 { margin-left: 1.5rem !important; }
.ms-5 { margin-left: 3rem !important; }

.me-0 { margin-right: 0 !important; }
.me-1 { margin-right: 0.25rem !important; }
.me-2 { margin-right: 0.5rem !important; }
.me-3 { margin-right: 1rem !important; }
.me-4 { margin-right: 1.5rem !important; }
.me-5 { margin-right: 3rem !important; }

.p-0 { padding: 0 !important; }
.p-1 { padding: 0.25rem !important; }
.p-2 { padding: 0.5rem !important; }
.p-3 { padding: 1rem !important; }
.p-4 { padding: 1.5rem !important; }
.p-5 { padding: 3rem !important; }

.pt-0 { padding-top: 0 !important; }
.pt-1 { padding-top: 0.25rem !important; }
.pt-2 { padding-top: 0.5rem !important; }
.pt-3 { padding-top: 1rem !important; }
.pt-4 { padding-top: 1.5rem !important; }
.pt-5 { padding-top: 3rem !important; }

.w-25 { width: 25% !important; }
.w-50 { width: 50% !important; }
.w-75 { width: 75% !important; }
.w-100 { width: 100% !important; }
.w-auto { width: auto !important; }

.h-25 { height: 25% !important; }
.h-50 { height: 50% !important; }
.h-75 { height: 75% !important; }
.h-100 { height: 100% !important; }
.h-auto { height: auto !important; }

.text-center { text-align: center !important; }
.text-left { text-align: left !important; }
.text-right { text-align: right !important; }
.text-justify { text-align: justify !important; }

.text-uppercase { text-transform: uppercase !important; }
.text-lowercase { text-transform: lowercase !important; }
.text-capitalize { text-transform: capitalize !important; }

.font-weight-bold { font-weight: 700 !important; }
.font-weight-normal { font-weight: 400 !important; }
.font-weight-light { font-weight: 300 !important; }

.rounded { border-radius: 0.375rem !important; }
.rounded-sm { border-radius: 0.25rem !important; }
.rounded-lg { border-radius: 0.5rem !important; }
.rounded-circle { border-radius: 50% !important; }
.rounded-pill { border-radius: 50rem !important; }
.rounded-0 { border-radius: 0 !important; }

.shadow-none { box-shadow: none !important; }
.shadow-sm { box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important; }
.shadow { box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important; }
.shadow-lg { box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175) !important; }

.overflow-auto { overflow: auto !important; }
.overflow-hidden { overflow: hidden !important; }
.overflow-visible { overflow: visible !important; }
.overflow-scroll { overflow: scroll !important; }

.position-static { position: static !important; }
.position-relative { position: relative !important; }
.position-absolute { position: absolute !important; }
.position-fixed { position: fixed !important; }
.position-sticky { position: sticky !important; }

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* =============================================================================
   END OF COMPONENTS CSS
   ============================================================================= */
"""

    with open(CSS_FILE, 'w') as f:
        f.write(css_content)
    print(f'CSS file created: {CSS_FILE}')


def configure_initial_vscode_settings():
    """Set up VSCode settings for initial state (no outline sort order configured)."""
    os.makedirs(VSCODE_USER, exist_ok=True)

    # Load existing settings or start empty
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        import re
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        settings = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    # Ensure outline.sortOrder is NOT set to 'position' in initial state
    # Remove it if it was somehow set
    settings.pop('outline.sortOrder', None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f'VSCode settings configured (no outline.sortOrder): {SETTINGS_PATH}')


def create_initial():
    create_css_file()
    configure_initial_vscode_settings()

    # GUI-ready startup: open VSCode with the CSS file
    launch_gui(f'code "{CSS_FILE}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with components.css, DISPLAY=:0')


create_initial()
