---
title: "A Development Workflow"
date: 2018-08-19T20:32:21-05:00
draft: false
---

From my first programming steps, I used a bunch of different IDEs to code, depending on the times and the
programming language used: `Borland C++`, `Code::Blocks` (for C), `Visual Studio` (C, C++), `Matlab IDE`,
`IDLE` (Python native IDE), `Eclipse` (With `PyDev` for `Python`), `Spyder`, `Sublime Text`, `Vim`, `VS Code`, etc.

This is somehow chronological. I lately used `VS Code` because of three main reasons: This is a great software from
Microsoft, I needed to work on Windows (unfortunately) and wanted something great for switching between languages.

Since I recentely came back to MacOS / Linux, I felt the need to restore my "old school" development workflow, with
`vim` and `tmux`. This is what this note is about.

## Terminals
* [iTerm2](https://iterm2.com/) on MacOS.
* [Terminator](https://gnometerminator.blogspot.com/) on Linux

## Vim
A couple of years now I have been using `Vim`. I still feel as a newbie considering the wide options it offers, but also feel
productive with it. I use it in the shell, but also with `Sublime Text` and `VS Code` thanks to the plugins.

`Vim` in the shell with some configuration and plugins is a killer tool for developping in any language.
![vim](/vim.png)

[Here](https://github.com/cedricleroy/config/blob/master/.vimrc) is my vim configuration file (`.vimrc`). Here is what is worth
mentionning:

* I use [vundle](https://github.com/VundleVim/Vundle.vim) as vim package manager.
  Installing a plugin is simple: ``:PluginInstall``, after adding ``Plugin "<name>"`` in ``.vimrc``.
* My leader key is `\`
* Plugins:
  * [Nerdtree](https://github.com/scrooloose/nerdtree) (left buffer of the screenshot above)
  * [nerdtree-git-plugin](https://github.com/Xuyuanp/nerdtree-git-plugin): A plugin of NERDTree showing git status flags.
  * [VimDevIcons](https://github.com/ryanoasis/vim-devicons). This plugin is to have file icons showing up in the menu (like VSCode). It requires having a patched font (I am using Fira Code with ligatures enabled as standard font, and Hack Nerd Font as Non-ASCII font). Those needs be be configured in the terminal (iTerm2 in my case). They are installed with the following commands on Mac:
  ```
  brew tap homebrew/cask-fonts
  brew cask install font-fira-code
  brew cask install font-hack-nerd-font
  ```
  * [colorschemes](https://github.com/flazz/vim-colorschemes) (I usually use `molokai`).
  * Vim [airline](https://github.com/vim-airline/vim-airline) with [airline-themes](https://github.com/vim-airline/vim-airline-themes) for status/tabline. 
  * [ale](https://github.com/dense-analysis/ale) for async linting.
  * [YouCompleteMe](https://github.com/ycm-core/YouCompleteMe) for autocompletion.
  * [Vim Fugitive](https://github.com/tpope/vim-fugitive) as Git wrapper.
  * [fzf](https://github.com/junegunn/fzf) as main fuzzy file finder.
* A few key binding:
  * `jj` as second `ESC`.
  * `TAB` with `.` (repeat)
  * `CTRL+N` to toggle nerdtree
  * leader + f to trigger `fzf` for fuzzy finding (`:Files`).
  * leader + q to trigger `fzf` with git filtering (`:GFiles`).
