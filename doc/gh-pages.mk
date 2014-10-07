REPO_URL=https://github.com/kenbeese/DataProcessor.git
REPO_DIR=gh-pages

.PHONY: gh-pages-clone gh-pages-push gh-pages-update gh-pages-all
.NOTPARALLEL: gh-pages-all

gh-pages-all: gh-pages-pull gh-pages-update gh-pages-push

gh-pages-clone:
	rm -rf $(REPO_DIR)
	git clone --branch gh-pages $(REPO_URL) $(REPO_DIR)

gh-pages-pull:
	cd $(REPO_DIR) && git pull

gh-pages-update:
	$(MAKE) clean html
	@echo "Clean $(REPO_DIR)"
	rm -rf $(REPO_DIR)/*

	@echo "Copy files: $(BUILDDIR)/html/* -> $(REPO_DIR)/"
	cp -r $(BUILDDIR)/html/* $(REPO_DIR)/

	@echo "Update gh-pages"
	cd $(REPO_DIR) && \
		git add . && \
		if [ -n "$$(git ls-files --deleted .)" ]; then \
			git ls-files --deleted . | xargs git rm; \
		fi && \
		git commit -m "Update API document"


gh-pages-push:
	cd $(REPO_DIR) && git push -u origin gh-pages
