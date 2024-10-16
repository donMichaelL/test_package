.PHONY: precommit test

precommit:
	pre-commit run --all-files

test:
	tox -- --cov-fail-under=70

check-main-branch:
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" != "main" ]; then \
		echo "Error: You are not on the main branch!"; \
		exit 1; \
	fi

bump: check-main-branch precommit test
	@if [ -z "$(NEW_VERSION)" ]; then \
		bump-my-version show-bump; \
		echo "Execut: make bump NEW_VERSION=x.x.x"; \
		exit 1; \
	fi
	bump-my-version bump --new-version $(NEW_VERSION)

push_main: bump
	git push origin main --follow-tags
	echo "Version bumped to $(NEW_VERSION) and pushed to GitHub."

pypi_release: push_main
	python -m build --sdist --wheel .
	twine upload dist/*
	echo "Released version $(NEW_VERSION) to PyPI."
