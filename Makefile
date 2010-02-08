
default: build

scorebee/ui/%.py: ui/%.ui
	pyuic4-2.6 $< > $@
	
scorebee/ui/%_rc.py: ui/%.qrc
	pyrcc4-2.6 $< > $@

status_window: scorebee/ui/status_window.py scorebee/ui/status_window_rc.py
info_window: scorebee/ui/info_window.py
timeline_window: scorebee/ui/timeline_window.py

build: status_window info_window timeline_window
	# BUILD

app: build
	python setup.py py2app --alias

dist: build
	python setup.py py2app

run: build
	# RUN
	python -m scorebee.main

clean:
	find scorebee -name "*.pyc" | xargs rm -v