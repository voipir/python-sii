# Chilean Tax Revenue Office (SII) Library.
---
## What is it?
It is a Python library aimed at facilitating the interactions with Chile's SII (Tax Revenue Office) requirements for information. This includes (by SII schema definition standards):
  - [x] Creation of <DTE> from <Documento>
  - [x] Creation of LibroVentas.
  - [x] Connecting and authentication with SII servers. (automatic session negociation)
  - [x] Signing of documents with x509 key/cert. (ask if you want to know how to get them from your .pfx)
  - [x] Uploading of sales documents.
  - [ ] Uploading of accounting reports.
  - [x] Generation of TeX Template. (Unix/Linux)
  - [x] Generation of PDF from TeX Template. (Unix/Linux)
  - [x] Printing of PDF and TeX Templates (Unix/Linux).

## Dependants
  * [python-sii-utils](https://github.com/voipir/python-sii-utils.git) (Command Line Utilities)

## Requirements
#### Currently this library has been developed and tested on:
  * GNU/Linux Debian 8.x Jessie

For support for a Microsoft OS, it should be possible, but will not be officially supported. We don't work with it, so if anybody wants to take up that task instead, be welcome to do so. We will acommodate your needs on porting as well as we can.

#### Library Dependencies:
  * Python3 (though it should be quite trivial to backport to 2.7 via __future__ includes)
  * suds-jerko (currently first choice of SUDS fork that has support for Python3)
  * lxml (xml creation and handling)
  * xmlsec (signing and verifying of documents)
  * jinja2 (for templating of TeX template which then is made a PDF by pdflatex)
  * pdflatex (PDF building, could be made optional to ease porting to a Microsoft OS)

## How-To
#### Use:
Currently there is no detailed documentation on usage available (TODO). The next best thing to get startet is to take a look at [python-sii-utils](https://github.com/voipir/python-sii-utils.git). There you can see usage cases of the library, covering pretty much all the library functionality. For any help or further info, please create an issue with the tag `help`.

## Licence
The library is licenced as LGPLv3 as you can make out in the LICENSE file. You can do what ever you want with this code, as long as you keep any changes or enhancements to this library (not your code that interacts with it!) public. Other than that we would also kindly ask you for fair play and collaboration. We all have the same itch to scratch here, and would greatly benefit from each other, even if by means of a bug report. Thank you!.

---
Enjoy!