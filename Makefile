#
# Matthew's makefile for dadbot
#

CREATE= -czvf
EXTRACT= -xzvf

all: extract create


create:
	tar $(CREATE) images.tar.gz images/*

extract:
	tar $(EXTRACT) images.tar.gz

clean:
	-rm -f images/*

