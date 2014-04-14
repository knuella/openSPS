Zielstellung
============

Mit dem Projekt RPi-SPS aka kraut-SPS aka crowd-SPS soll eine
speicherprogrammierbare Steuerung entwickelt werden, die quelloffen, modular
und kostengünstig ist.

Um dies zu erreichen sind folgende Punkte definiert worden:

  #. Kopfstation
       Es wird ein Einplatinencomputer als "Kopf" der SPS eingesetzt. In dem
       "Kopf" oder der "Kopfstation" läuft das Programm, das die Ein- und
       Ausgänge der Module steuert.

  #. Ein- und Ausgangsmodule
       Es werden Ein- und Ausgangsmodule eingesetzt, die über ein Bus mit der
       Kopfstation kommunizieren. Diese Baugruppen dienen der Erfassung bzw.
       der Ausgabe elektrischer Signale und damit als Schnittstelle zur "realen"
       Welt. Sie ermöglichen einen modularen und skalierbaren Aufbau.

  #. objektorientierte Kommunikation
       Es wird ein Kommunikationsprotokoll zur objektorientierte (strukturierten)
       Übertragung von Daten zwischen mehreren Kopfstation eingebunden. Dieses
       soll einen vorhandenen Standard nutzen und sich damit auch zur
       Kommunikation mit anderen Geräten eignen.

  #. Deterministische Kommunikation
       Es wird ein Kommunikationsprotokoll eingebunden, das eine deterministische
       Kommunikation zwischen Kopfstationen ermöglicht.

  #. HMI-Entwicklung
       Es soll eine Umgebung geschaffen werden, die die Entwicklung von
       platformunabhängigen Mensch-Maschine Schnittstellen (HMIs) auf einfache
       Art und Weise ermöglicht.

  #. Steuerungsprogramm-Entwicklung
       Es soll eine Umgebung geschaffen werden, die die Entwicklung von
       Steuerungs- und Regelprogrammen auf einfache Art und Weise ermöglicht.

  #. strikte Trennung
       Das eigentliche Steuerungs-, Regel- und HMI-Programm muss strikt von der
       Software getrennt sein, die die Bereitstellung der
       Datenpunkteigenschaften übernimmt. Die Software zur
       Datenpunkteigenschaftsbereitstellung erledigt z.B. Ausgabe von Werten an
       die Module oder die Werteaktualisierung des HMI.

  #. Austauschbare Hardware
       Als Kopfstation und als Module sollen mehrere verschiedene Geräte
       eingesetzt werden können. Diese müssen untereinander ohne großen Aufwand
       bzw. zusätzlicher Programmierleistung ausgetauscht werden können. 

  #. Erweiterbar
       Die Unterstützung für weitere Fabrikate für die Kopfstation oder für die
       Module muss leicht nachgerüstet werden können.

  #. Strukturierte Datenspeicherung
       Die Datenpunkteigenschaften (Name, Wert, ...) wird in einer Struktur
       unabhängig von der Programmausführung gespeichert. Diese Struktur ist
       die einzige Schnittstelle zwischen den verschiedenen Softwareteilen. 

  #. Integrierbarkeit
       In der Kopfstation werden weitere Kommunikationsprotokolle eingebunden um
       einen Betrieb der entwickelten Lösung in bestehenden
       Automatisierungskonzepten zu ermöglichen.

  #. Offen
       Neben dem Quelltext der Software wird ein Wiki oder eine ähnliche
       Informationsstruktur veröffentlicht, die den Nachbau und eine
       Weiterentwicklung der offenen SPS ermöglichen.
