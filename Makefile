#
# Just a clean target: clean up after quickstart results
#

default :

clean-results :
	[[ -d results/ ]] && rm -rf results/ || true
	mkdir results
	echo '*' > results/.gitignore


.PHONY: default clean-results

