
============================================
|icon| Italian Withholding Tax 12.0.2.1.0_12
============================================


.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/l10n-italy/12.0/l10n_it_withholding_tax/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| Withholding tax


|

|it| Gestione della ritenuta d'acconto


|

Usage / Utilizzo
----------------

Per prima cosa dovremo creare una ritenuta d’acconto dove inserire tutti i campi necessari per un corretto calcolo.

Visto che le aliquote possono variare nel corso del tempo, nella codifica sono previsti scaglioni temporali di competenza.

E’ necessario anche inserire i conti contabili che verranno utilizzati quando il modulo si occuperà di generare registrazioni contabili per la rilevazione della ritenuta.

.. figure:: static/img/ritenuta-acconto-odoo-codifica-768x457.png
   :alt: Withholding tax
   :width: 600 px

Una volta aggiunta, nella tabella ritenute, potrà essere utilizzata all’interno della fattura, in corrispondenza delle righe soggette a ritenute.

Per ogni riga è possibile utilizzare più di una ritenuta. Per alcune casistiche il moduo ritenute viene usato anche per rilevare le trattenute INPS.

Il modulo ritenute calcolerà i valori corrispondenti e ne mostrerà il dettaglio nell’apposita area ritenute, dove è possibile verificare per ogni codice ritenuta usato, l’imponibile e l’importo ritenuta applicato.

In calce ai totali, verrà totalizzato l’ammontare della ritenuta e il netto a pagare. Questa sezione sarà visibile solamente in presenza di almeno una ritenuta

.. figure:: static/img/fattura-fornitore-768x517.png
   :alt: Supplier invoice
   :width: 600 px

Successivamente andando nella sezione situazione ritenute d’acconto il sistema vi mostrerà una situazione riepilogativa delle varie ritenute divisa per documento di origine.

I campi principalmente da tenere in considerazione in questa tabella sono: ritenuta dovuta, ritenuta applicata e ritenuta versata.

*Ritenuta dovuta* contiene il valore della ritenuta contenuta nella fattura.

*Ritenuta applicata* mostra il valore della ritenuta rilevata al momento del pagamento della fattura.

*Ritenuta versata* contiene l’importo di ritenuta, già applicata, che è stata versata all’erario

.. figure:: static/img/foto-3-1-1024x505.png
   :alt: WT statement
   :width: 600 px


|

OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+


|
|

Getting started / Come iniziare
===============================

|Try Me|


|

Installation / Installazione
----------------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instructions are just an  | Istruzioni di esempio valide solo per    |
| example; use on Linux CentOS 7+ | distribuzioni Linux CentOS 7+,           |
| Ubuntu 14+ and Debian 8+        | Ubuntu 14+ e Debian 8+                   |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__    |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/12.0                                                                 |
+----------------------------------------------------------------------------+

::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository installation; OCB repository must be installed
    odoo_install_repository l10n-italy -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_withholding_tax** > Install


|

Upgrade / Aggiornamento
-----------------------


::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository upgrade
    odoo_install_repository l10n-italy -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese `Powerp <http://www.powerp.it/>`__

Developer companies are / I soci sviluppatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/PowERP-cloud/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


If you have a proposal to change this module, you may want to send an email to <info@powerp.it> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.2.1.0_11 (2021-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug POW-540 riconciliazioni mancate

12.0.2.1.0_11 (2021-11-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug multi righe movimenti pagamento

12.0.2.1.0_10 (2021-09-28)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito bug conti sul residuo pagamenti

12.0.2.1.0_9 (2021-09-07)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato visibilita fissa Rda nella riga

12.0.2.1.0_8 (2021-09-06)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato totali corretti nel form / wizard dei pagamenti

12.0.2.1.0_7 (2021-09-01)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato il filtro sui pagamenti della fattura solo se questa ha la ritenuta d'acconto
* [FIX] POW-466 - Abilitazione campo ritenuta sulle righe fattura

12.0.2.1.0_6 (2021-08-02)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-434 - Filtro sul registro

12.0.2.1.0_5 (2021-07-14)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Verificato e risolto bug POW-409 - Nascosto campo pagamento netto residuo

12.0.2.1.0_4 (2021-07-12)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato filtro corretto sui movimenti contabili per la registrazione del pagamento

12.0.2.1.0_3 (2021-07-02)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring account_move_create

12.0.2.1.0_2 (2021-07-01)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato l'importo corretto nel wizard del pagamento

12.0.2.1.0_1 (2021-06-21)
~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato numero di versione con incrementante interno



|
|

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)



|

Authors / Autori
----------------

* `powERP <https://www.powerp.it>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__
* `Didotech srl <https://www.didotech.com>`__


Contributors / Collaboratori
----------------------------

* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Marco Tosato <marco.tosato@didotech.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>


Maintainer / Manutenzione
-------------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese Powerp <http://www.powerp.it/>
Developer companies are / I soci sviluppatori sono:
* Didotech s.r.l. <http://www.didotech.com>
* SHS-AV s.r.l. <https://www.shs-av.com/>


|

----------------


|en| **Powerp** is an Italian enterprises network, whose mission is to develop high-level addons designed for Italian enterprise companies.

`Powerp <http://www.powerp.it/>`__ code adds new enhanced features to Italian localization and it released under `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ or `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__ licenses.

|it| `Powerp <http://www.powerp.it/>`__ è una rete di imprese italiane, nata con la missione di sviluppare moduli per le PMI.

Il codice di `Powerp <http://www.powerp.it/>`__ aggiunge caratteristiche evolute alla localizzazione italiana; il codice è rilasciato con licenze `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ e `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__

I soci fondatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__
* `Xplain s.r.l. <http://x-plain.it//>`__



|chat_with_us|


|

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2021-12-14

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/PowERP-cloud/l10n-italy.svg?branch=12.0
    :target: https://travis-ci.com/PowERP-cloud/l10n-italy
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/PowERP-cloud/l10n-italy/badge.svg?branch=12.0
    :target: https://coveralls.io/github/PowERP-cloud/l10n-italy?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0
    :alt: Codecov
.. |Tech Doc| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-12.svg
    :target: https://wiki.zeroincombenze.org/en/Odoo/12.0/dev
    :alt: Technical Documentation
.. |Help| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-12.svg
    :target: https://wiki.zeroincombenze.org/it/Odoo/12.0/man
    :alt: Technical Documentation
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-12.svg
    :target: https://erp12.zeroincombenze.it
    :alt: Try Me
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy/branch/12.0
    :alt: Codecov
.. |Odoo Italia Associazione| image:: https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png
   :target: https://odoo-italia.org
   :alt: Odoo Italia Associazione
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
.. |chat_with_us| image:: https://www.shs-av.com/wp-content/chat_with_us.gif
   :target: https://t.me/Assitenza_clienti_powERP

