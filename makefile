#
# Convencience Makefile to automate common tasks.
#
ARGS     := ""	# any custom arguments for py.test you can think of
ARG_KEY  := ""	# mandatory
ARG_CERT := ""	# mandatory


.PHONY: test


test:
	python tests/test.py $(ARGS) --key-path $(ARG_KEY) --cert-path $(ARG_CERT) tests/*
