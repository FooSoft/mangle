all: \
	mangle/ui/resources_rc.py \
	mangle/ui/about_ui.py \
	mangle/ui/options_ui.py \
	mangle/ui/book_ui.py

mangle/ui/resources_rc.py: dev/res/resources.qrc
	pyrcc4 $< -o $@

mangle/ui/about_ui.py: dev/ui/about.ui
	pyuic4 $< -o $@

mangle/ui/options_ui.py: dev/ui/options.ui
	pyuic4 $< -o $@

mangle/ui/book_ui.py: dev/ui/book.ui
	pyuic4 $< -o $@
