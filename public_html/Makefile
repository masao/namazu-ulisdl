INDEXDIR = /opt/namazu/var/namazu/index

HEAD = $(INDEXDIR)/NMZ.head.ja
BODY = $(INDEXDIR)/NMZ.body.ja
FOOT = $(INDEXDIR)/NMZ.foot.ja

all: index.html help.html

index.html: $(HEAD) body.txt $(FOOT)
	cat $(HEAD) body.txt $(FOOT) > $@

help.html: $(HEAD) $(BODY) $(FOOT)
	cat $(HEAD) $(BODY) $(FOOT) > $@
