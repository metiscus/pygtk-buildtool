default: project

.PHONY:project
project:
	@echo "Asdfasdf"
	@dd if=/dev/urandom of=/dev/stdout bs=10M count=10 | base64 | tee derp.txt

clean:
	rm -f derp.txt

remake: clean default