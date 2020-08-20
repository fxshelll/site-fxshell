---
title: "Steghide"
date: 2020-08-19T23:23:34-03:00
draft: false
---

```sh
#para embedar um arquivo de texto dentro de uma imagem
$ steghide embed -cf picture.jpg -ef secret.txt

#para extrair o arquivo de dentro da imagem
$ steghide extract -sf picture.jpg

#para exibir informações sobre o arquivo de imagem com o embed
$ steghide info picture.jpg

