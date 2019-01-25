# Makefile

BINDIR = ~/bin
SRCDIR = stevtb-v0.1
SRC = AppDef.py AppView.py AppFile.py AppCtrl.py main.py
BIN = stevtb

install:
	mkdir $(BINDIR)/$(SRCDIR)
	cp $(SRC) $(BINDIR)/$(SRCDIR)
	cp $(BIN) $(BINDIR)

uninstall:
	rm -f $(BINDIR)/$(BIN)
	rm -fr $(BINDIR)/$(SRCDIR)

clean:
	rm -f *.pyc

# end of file
