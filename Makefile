# Name of the output tarball
PACKAGE_NAME := mypack.tar.gz

# Exclude the tarball itself, git data, node_modules, etc. if desired
EXCLUDES := --exclude=$(PACKAGE_NAME) --exclude=.git --exclude=venv_local 

# Default target
package:
	tar czf $(PACKAGE_NAME) $(EXCLUDES) .

# Test targets
test:
	python -m pytest tests/ -v

test-structured:
	python test_structured_output.py

# Run tests with structured output
run-structured:
	python runner.py --structured --format detailed

# Run tests with regular output
run-regular:
	python runner.py --format detailed
