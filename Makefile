
.PHONY: build run test clean
.DEFAULT: build


UIs := $(wildcard ui/*.ui)
RCs := $(wildcard ui/*.qrc)
PYs := $(UIs:ui/%.ui=scorebee/ui/%.py) $(RCs:ui/%.qrc=scorebee/ui/%_rc.py)

build: $(PYs)

scorebee/ui/%.py: ui/%.ui
	pyuic4 $< > $@
	
scorebee/ui/%_rc.py: ui/%.qrc
	pyrcc4 $< > $@

run: build
	python -m scorebee.main

test: build
	python -m scorebee.main --debug

clean:
	- rm scorebee/ui/*_window.py
	- find scorebee -name "*.pyc" | xargs rm -v
	- rm -rf build dist
