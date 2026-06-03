"""
Initial Setup: Vim autowrite setting - web search and config task
Task ID: osworld_multi_apps_web_search_config_003
Domain: os (multi-app: terminal + Chrome)

Creates ~/.vimrc with typical Vim settings but WITHOUT any autowrite settings.
Opens Terminal and Chrome browser to represent the initial state.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_search_config_003'
VIMRC_PATH = '/home/user/.vimrc'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create a realistic ~/.vimrc WITHOUT any autowrite settings
    # (The task is to search for and add the autowrite setting)
    vimrc_content = """\
" ~/.vimrc - Vim configuration file

" General settings
set nocompatible
set encoding=utf-8
set fileformats=unix,dos,mac

" Appearance
set number
set relativenumber
set cursorline
set colorcolumn=80
set laststatus=2
set ruler
set showcmd
set showmode

" Indentation
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent

" Search
set hlsearch
set incsearch
set ignorecase
set smartcase

" Editing
set backspace=indent,eol,start
set clipboard=unnamedplus
set mouse=a

" Folding
set foldmethod=indent
set foldlevel=99

" Backup and swap
set noswapfile
set nobackup

" Syntax and file type
syntax on
filetype plugin indent on

" Key mappings
let mapleader = ","
nnoremap <leader>w :w<CR>
nnoremap <leader>q :q<CR>
nnoremap <leader>e :e!<CR>
nnoremap <C-n> :NERDTreeToggle<CR>

" Split navigation
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Statusline
set statusline=%F%m%r%h%w\ [FORMAT=%{&ff}]\ [TYPE=%Y]\ [POS=%l,%v][%p%%]

" Plugin settings (vim-plug)
" call plug#begin('~/.vim/plugged')
" Plug 'scrooloose/nerdtree'
" Plug 'tpope/vim-fugitive'
" Plug 'vim-airline/vim-airline'
" call plug#end()
"""

    # Write the .vimrc file
    Path(VIMRC_PATH).write_text(vimrc_content)
    print(f'Initial .vimrc created: {VIMRC_PATH}')

    # GUI-ready startup: open Terminal and Chrome (as described in context)
    # Launch GNOME Terminal
    launch_gui('gnome-terminal', delay_sec=2.0)

    # Launch Chrome browser (for web search)
    launch_gui('google-chrome --new-window "https://www.google.com"', delay_sec=2.5)

    print('GUI_READY: launched Terminal and Chrome with DISPLAY=:0')


create_initial()
