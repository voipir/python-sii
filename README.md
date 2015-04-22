# Chilean Tax Revenue Office (SII) interaction Library.
---
## What is it?
It is a Python library aimed at facilitating the interactions with Chile's SII (Tax Revenue Office) requirements for information. This includes (by SII schema definition standards):
  * [DONE] Creation of sales documents.
  * [TODO] Creation of accounting documents.
  * [DONE] Connecting and authentication with SII servers. (automatic session negociation)
  * [ALMOST DONE] Signing of documents with x509 key/cert. (ask if you want to know how to get them from your .pfx)
  * [TODO] Uploading of sales documents.
  * [TODO] Uploading of accounting reports.
  * [DONE] Printing of various documents including the mandatory PDF417 barcode.

## Requirements
#### Currently this library has been developed and tested on:
  * GNU/Linux Debian 8.0 (Jessie, in the making as the time of writing)

#### Library Dependencies:
  * Python3 (though it should be quite trivial to backport to 2.7 via __future__ includes)
  * suds-jerko (currently first choice of SUDS fork that has support for Python3)
  * lxml (xml creation and handling)
  * xmlsec (signing and verifying of documents)
  * jinja2 (for templating of TeX template which then is made a PDF by pdflatex)
  * pdflatex (PDF building, could be made optional to ease porting to a Microsoft OS)

#### Testsuite Dependencies:
  * pytest
  * pytest-timeout (optional but recomended because of server auth flakyness)

For support for a Microsoft OS, it should be possible, but will not be officially supported. We don't work with it, so if anybody wants to take up that task instead, be welcome to do so. We will acommodate your needs on porting as well as we can.

## How-To
#### Use:
Currently there is no detailed documentation on usage available (TODO). The next best thing to get startet is to take a look at `tests/*`. You will find the promises this library makes and how the interface is intended to be interacted with. For any help or further info, please create an issue with the tag `help`.

#### Test:
To run the testsuite you first will need to install the package (you might want to do so in a virtualenv) with either one of commands below:
```bash
python3 setup.py install
python3 setup.py develop
```
Then you run the testsuite by running (you will need `Make` installed):
```bash
make test ARG_KEY="/path/to/key/file.pem" ARG_CERT="/path/to/cert/file.pem"
```
Since tests against the auth server are flaky at the moment, dropping every Nth connection and currently not correctly verifying certificate signatures, you might want to take a look at the py.test "timeout" plugin to put a hard limit and avoid getting stuck mid-test.

## Licence
The library is licenced as LGPLv3 as you can make out in the LICENSE file. You can do what ever you want with this code, as long as you keep any changes or enhancements to this library (not your code that interacts with it!) public. Other than that we would also kindly ask you for fair play and collaboration. We all have the same itch to scratch here, and would greatly benefit from each other, even if by means of a bug report. Thank you!.

---
Enjoy!