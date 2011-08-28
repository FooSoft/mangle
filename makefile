all: \
	ui/resources_rc.py \
	ui/about_ui.py \
	ui/options_ui.py \
	ui/book_ui.py

ui/resources_rc.py: dev/res/resources.qrc
	pyrcc4 $< -o $@

ui/about_ui.py: dev/ui/about.ui
	pyuic4 $< -o $@

ui/options_ui.py: dev/ui/options.ui
	pyuic4 $< -o $@

ui/book_ui.py: dev/ui/book.ui
	pyuic4 $< -o $@
