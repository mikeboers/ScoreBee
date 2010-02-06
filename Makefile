
default: build

%.py: %.ui
	pyuic4-2.6 $< > $@

build:
	# BUILD

run: build
	# RUN