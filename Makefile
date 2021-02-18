.DEFAULT_GOAL := send

.PHONY: send
send:
	cp CIRCUITPY/code.py ~/disks/CIRCUITPY/

.PHONY: init
init:
	cp -r CIRCUITPY/* ~/disks/CIRCUITPY/
