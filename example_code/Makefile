test:
	for path in $$(ls ./*.py); \
			do \
					echo "\n\nRunning $$path"; \
					$$path 0</dev/null; \
					if [ $$? -ne 0 ]; then \
						echo "FAIL: $$path"; \
						exit 1; \
					fi; \
			done
