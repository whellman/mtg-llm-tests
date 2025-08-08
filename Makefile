# Name of the output tarball
PACKAGE_NAME := mypack.tar.gz

# Exclude the tarball itself, git data, node_modules, etc. if desired
EXCLUDES := --exclude=$(PACKAGE_NAME) --exclude=.git 

# Default target
package:
	tar czf $(PACKAGE_NAME) $(EXCLUDES) .
	@echo "Created $(PACKAGE_NAME)"
