12.0.3.7.49 (2023-02-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Error "Accredito" with refunc / Errore "Accredito" se NC

12.0.3.7.48 (2023-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Payment confirm for refund line / Conferma pagamento di righe con NC
* [TEST] Regression test: 21% (1438/1135)

12.0.4.7.47.1 (2023-01-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Nella descrizione delle righe della registrazione di insoluto viene riportato il numero fattura se il campo "name" di "account.invoice" non è valorizzato

12.0.3.7.47 (2022-12-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Confirm payment w/o company bank / Conferma pagamento segnala assenza banca azienda

12.0.3.7.46 (2022-11-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Confirm payment w/o company bank / Conferma pagamento segnala assenza banca azienda
* [FIX] Crash if not compiled portafoglio SBF / Crash se manca conto portafoglio SBF
* [FIX] Errato caricamento conto effetti attivi
* [IMP] Bank form: help and more info / Form banca: help + info dettagliate
* [IMP] Field account_move_line.payment_order_lines renamed to payment_line_ids

12.0.3.7.45 (2022-10-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione riconciliazioni degli insoluti

12.0.3.7.44 (2022-07-05)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Ricalcolo disponibilità

12.0.3.7.43 (2022-04-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato warning su differenza importo scadenze minore del delta impostato in configurazione

12.0.3.7.42 (2022-04-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Effettuato refactoring della registrazione del pagamento delle scadenze
* [FIX] Gestito riconciliazioni nella registrazione degli insoluti

12.0.3.7.41 (2022-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato ordinamento delle azioni nel rispettivo menù di pagamenti e scadenze

12.0.3.7.40 (2022-03-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato configurazione conti di abbuono e abbuono delta
* [FIX] Esposto in tutti i registri il conto spese bancarie

12.0.3.7.39 (2022-03-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito importi scadenze in insoluto standard

12.0.3.7.38 (2022-03-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Inserita data accredito da wizard

12.0.3.7.37 (2022-03-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito controllo su distinte insolute

12.0.3.7.36 (2022-03-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito controllo su distinte riconciliate

12.0.3.7.35 (2022-03-03)
~~~~~~~~~~~~~~~~~~~~~~~~

 * [IMP] Gestione operazioni di registrazione pagamenti fornitori e compensazione tra fatture e note di credito nelle registrazioni
 * [IMP] Gestione spese bancarie

12.0.3.7.34 (2022-03-02)
~~~~~~~~~~~~~~~~~~~~~~~~

 * [IMP] Possibilità di scegliere sezionale e data registrazione contabile al momento della registrazione del pagamento
 * [FIX] Correzione nome modello

12.0.3.7.33 (2022-03-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito annullamento distinta che ha scadenze con incasso effettuato

12.0.3.7.32 (2022-03-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring ordine di pagamento in riga scadenza
* [FIX] Corretto la gestione del portafoglio nella registrazione dell'insoluto

12.0.3.7.31 (2022-03-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Resettato il flag incasso_effettuato a False nella registrazione dell'insoluto
* [IMP] Gestito conto spese bancarie con verifica del registro
* [IMP] Gestito il flag incasso_effettuato quando si riporta in bozza una distinta

12.0.3.7.30 (2022-02-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato controlli wizard conferma pagamenti

12.0.3.7.29 (2022-02-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato funzionalità registra pagamenti

12.0.3.7.26 (2022-01-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Update dependencies

12.0.3.7.25 (2022-01-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring impostazione conti trasferiti nel registro

12.0.3.7.24 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione visibiltà pulsante accredito

12.0.3.7.23 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione viste conto di portafoglio

12.0.3.7.22 (2022-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestione registrazioni contabili con conto di portafoglio

12.0.3.7.21 (2021-12-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato default per importo accreditato

12.0.3.7.20 (2021-12-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito conti bancari nelle scadenze

12.0.3.7.19 (2021-12-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Gestito iban non impostato

12.0.3.7.18 (2021-12-10)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corretto formattazione conti

12.0.3.7.17 (2021-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato metodo che valorizza il conto per il credit

12.0.3.7.16 (2021-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fix ricerca ordini in aggiungi a distinta

12.0.3.7.15 (2021-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato formattazione conto solo per tipo iban

12.0.3.7.14 (2021-11-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato in sola lettura il campo standard del conto bancario

12.0.3.7.13 (2021-11-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-573 Impostato e gestito il display name del conto bancario

12.0.3.7.12 (2021-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-556 Impostato e gestito il campo del conto bancario aziendale nei controlli di anticipo fattura

12.0.3.7.11_M (2021-11-24)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-573 Impostato nuovo formato per il nome del record

12.0.3.7.11 (2021-11-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-367 Verificato e corretto utilizzo campo banca impostata in fattura

12.0.3.7.10 (2021-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-524 Refactoring del codice per il campo Conto aziendale

12.0.3.7.9 (2021-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-526 Corretta la verifica dei conti bancari nel wizard di generazione ordini

12.0.3.7.8 (2021-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato popolamento registri nel wizard di generazione ordini

12.0.3.7.7 (2021-10-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-523 Fix popolamento registri nel wizard di generazione ordini

12.0.3.7.6 (2021-08-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] POW-464 Aggiornamento vista registri per conti di portafoglio

12.0.3.7.5 (2021-06-25)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] POW-401 Aggiornamento configurazione conto "Effetti allo sconto"

12.0.3.7.4 (2021-04-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato nella tab [Transfer journal entries] il riferimento a alla registrazione di accredito

12.0.3.7.3 (2021-03-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] lint error: F401 'odoo.exceptions.UserError' imported but unused

12.0.3.7.2 (2021-03-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato funzionalità aggiornamento metodo di pagamento

12.0.3.7.1 (2021-02-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornata gestione del registro per l'ordine in caso di anticipo fatture

12.0.3.6.3 (2021-02-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Check su dati banca in anticipo fatture

12.0.3.6.2 (2021-02-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Aggiornato messaggi di errore

12.0.3.6.1 (2021-02-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Trasferito i wizard per la creazione distinta e inserimento scadenze

12.0.3.5.14 (2021-02-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] No riferimento data bilancio

12.0.3.5.13 (2021-02-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornato numero versione dopo warning travis

12.0.3.5.12 (2021-02-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Modifica registrazione contabile degli insoluti

12.0.3.4.11 (2021-02-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Refactoring

12.0.3.4.10 (2021-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Impostato spese di default

12.0.3.4.9 (2021-01-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Aggiornato history

12.0.2.3.9 (2021-01-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Effettuato refactoring configurazione sul metodo di accreditamento

12.0.2.3.7 (2021-01-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Effettuato refactoring sul metodo di accreditamento

12.0.2.3.5 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Ordine di pagamento può essere eliminato solo se in stato "cancel" ("Annulla")

12.0.2.2.5 (2021-01-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactor wizard confirm payment / Reimplementato il wizard per conferma pagamento

12.0.2.2.4 (2021-01-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Update wizard confirm payment / Completato il wizard per conferma pagamento

12.0.2.2.3 (2020-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Set wizard confirm payment / Impostato il wizard per conferma pagamento

12.0.0.1.37 (2020-12-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added filter 'not in order' and state field / Impostato filtro 'Non in scadenza' e campo stato

12.0.0.1.36 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Warning on check duedate payments / Segnalazione al tentativo di annullamento con scadenze in pagamento

12.0.0.1.35 (2020-12-11)
~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring date effective / Aggiornato gestione data decorrenza

12.0.0.1.34 (2020-12-04)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Set vat on first duedate according to payment term flag / Impostato gestione iva sulla prima scadenza

12.0.0.1.33 (2020-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.32 (2020-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossa creazione righe scadenze se almeno una in pagamento

12.0.0.1.31 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set duedates creation from sale order / Impostato creazione scadenze da ordine di vendita

12.0.0.1.30 (2020-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set account invoice 13 more dependency / Inserita dipendenza modulo transizione

12.0.0.1.29 (2020-11-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Set default date effective / Impostato default data decorrenza

12.0.0.1.28 (2020-11-17)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Added missing dependency / inserita dipendenza mancante

12.0.0.1.27 (2020-11-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Added date effective / inserita data di decorrenza

12.0.0.1.26 (2020-11-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] impostato ricerca per ordine di pagamento

12.0.0.1.25 (2020-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] impostato campo ordine di pagamento nella view

12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestito validazione fattura da ordine di vendita

12.0.0.1.24 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretto calcolo ammontare fattura in account.move

12.0.0.1.23 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] gestione cancellazione ultima scadenza rimasta (mette una nuova riga di scadenza e una nuova riga contabile con scadenza parti alla data fattura e importo pari all'imposto dattura)

12.0.0.1.22 (2020-11-02)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] corretta gestione scadenze per fatture in stato bozza

12.0.0.1.21 (2020-10-28)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Update model, removed unused fields

12.0.0.1.18 (2020-10-23)
~~~~~~~~~~~~~~~~~~~~~~~~

* [MOD] Correzioni di forma la codice per adeguamento a segnalazioni Flake8

12.0.0.1.17 (2020-10-22)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Eliminazione righe di scadenza vuote, calcolo proposta per importo scadenze dopo modifica fattura, ricalcolo automaticp scadenze al cambio dei termini di pagamento

12.0.0.1.16 (2020-10-21)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Implementato totalizzazione totale scadenze e differenza tra scadenze e totale fattura

12.0.0.1.15 (2020-10-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Aggiornato duedate manager

12.0.0.1.14 (2020-10-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimosso campo duplicato (termine di pagamento)

12.0.0.1.13 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Aggiornamento bidirezionale di data scadenza e metodo di pagamento tra account.move.line e account.duedate_plus.line

12.0.0.1.12 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Inserita dipendenza modulo OCA Scadenziario account_due_list


12.0.0.1.11 (2020-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Rimossi controlli non validi
