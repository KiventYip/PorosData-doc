# Secure Makefile for Sphinx documentation
# Security: Prevents common make vulnerabilities
# Robustness: Better error handling and validation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Security: Prevent dangerous variable values
ifeq ($(SPHINXBUILD),)
    $(error SPHINXBUILD is not set)
endif

# Validate build environment
.PHONY: check-env
check-env:
	@echo "Validating build environment..."
	@command -v $(SPHINXBUILD) >/dev/null 2>&1 || { echo "Error: $(SPHINXBUILD) not found"; exit 1; }
	@python3 --version >/dev/null 2>&1 || { echo "Error: Python 3 not found"; exit 1; }
	@test -f conf.py || { echo "Error: conf.py not found"; exit 1; }
	@echo "Environment validation passed."

# Clean build artifacts securely
.PHONY: clean
clean: check-env
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILDDIR)/*
	@echo "Clean completed."

# Build with security checks
.PHONY: html
html: check-env clean
	@echo "Building HTML documentation..."
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo "Build completed successfully."

# Put it first so that "make" without argument is like "make help".
.PHONY: help
help: check-env
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile check-env clean html

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile check-env
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
