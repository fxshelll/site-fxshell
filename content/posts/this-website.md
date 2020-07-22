---
title: "This Website"
date: 2018-08-18T21:00:14-05:00
draft: true
---

This website uses [hugo](https://gohugo.io/), a static website generator.
There is no particular reasons for me choosing `hugo`. There are tons of other solutions available.
I needed something simple enough to avoid the hassle of learning a new framework, being static and 
support of [markdown](https://en.wikipedia.org/wiki/Markdown). `Google` leaded me to `hugo`.

## Installation
(MacOS)
```
>> brew install hugo
```

## Creating a new site
```
hugo new mynewsite
```

## Themes
Hugo uses [themes](https://gohugo.io/themes/). I picked up [after dark](https://themes.gohugo.io/after-dark/), a minimalist
dark theme. The installation is pretty easy (from `~/mynewsite/themes/`):

```
>> git clone https://git.habd.as/comfusion/after-dark.git
```

## Configuration
The name of the theme needs to be added to `config.toml` (it uses [toml](https://github.com/toml-lang/toml) by default, yet
another configuration language...)
```toml
theme = "after-dark"
```

## New post
```
hugo new posts/my-first-post.md
```

## A few hacks
Here the interesting things begin. The default behavior was not working quiet as desired. First I wanted the first page
to be a static page, vs. displaying the list of the posts.
This behavior is handled in the theme layouts (`layouts/index.html`). It uses a templating language (which reminds
[Jinja](http://jinja.pocoo.org/)).
```html
{{ define "title" -}}
  {{ .Site.Title }}
{{- end }}
{{ define "header" }}
  {{ partial "menu.html" . }}
{{ end }}
{{ define "main" }}
  <header>
    <h1>{{ .Title }}</h1>
  </header>
  {{ range (.Paginate (where .Data.Pages "Type" "post")).Pages }}
    {{ partial "page-summary.html" . }}
  {{ end }}
{{ end }}
{{ define "footer" }}
  {{ partial "pagination.html" . }}
  {{ partial "powered-by.html" . }}
{{ end }}
```
Without knowing the details about how this is working, it is pretty obvious to figure out what it does:

* Display the title of the site
* Inject the content of the menu
* Another title
* Loop over the posts and render them as defined in `page-summary.html`
* Inject a couple of things in the footer

The loop is the interesting piece. We want to replace this behavior. It will be replaced by the following:
```html
{{ define "title" -}}
  {{ .Site.Title }}
{{- end }}
{{ define "header" }}
  {{ partial "menu.html" . }}
{{ end }}
{{ define "main" }}
  {{ range .Data.Pages }}
    {{if eq .Type "index" }} 
      {{.Content}}
    {{end}}
  {{ end }}
{{ end }}
{{ define "footer" }}
  {{ partial "powered-by.html" . }}
{{ end }}
```
This loops over the pages, and if it finds a page of a type `index`, it will display it.
The `index` page will be saved in the content (`index.md`), with the following header:
```
---
title: ""
type: index
---
```
We also remove the title, not really needed in the homepage.

We could replace the theme layout, but it is better to keep it as it is. We can overwrite the theme layout,
having `index.html` in the `layouts/` folder of the site. A similar strategy is used for 
`layouts/partials/page-summary.html` for changing the display of the list of posts.

## Deploying with GitHub

I am following the official [hugo doc](https://gohugo.io/hosting-and-deployment/hosting-on-github/#github-user-or-organization-pages) for this.

There are two git repos: One for the source, and another one for the generated site. The generated site is in the `public/` folder of the source
repo (with `public/` in `.gitignore` to avoid source controlling two times the generated site)

Typing `hugo` just generates the website in `public/`. `hugo serve` is used for local display.
