.PHONY : languages
languages:
	@echo "Getting repo languages..."
	python main.py languages

.PHONY : analyze
analyze:
	@echo "Analyzing repositories..."
	python main.py analyze

.PHONY : visualize
visualize:
	@echo "Visualizing analysis..."
	python main.py visualize

.PHONY : clean
clean:
	@echo "Cleaning up all cloned repos..."
	rmdir /S /Q cloned_repos/*