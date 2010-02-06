
default: build

scorebee/ui/%.py: ui/%.ui
	pyuic4-2.6 $< > $@
	
scorebee/ui/%_rc.py: ui/%.qrc
	pyrcc4-2.6 $< > $@

status_window: scorebee/ui/status_window.py scorebee/ui/status_window_rc.py

build: status_window
	# BUILD

run: build
	# RUN
	python -m scorebee.main