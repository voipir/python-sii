#
# Convencience Makefile to automate common tasks.
#
ARG_KEY  := ""
ARG_CERT := ""


.PHONY: test


test:
	python tests/test.py --key-path $(ARG_KEY) --cert-path $(ARG_KEY) tests/*
