https://www.immobiliare.it/api-next/search-list/real-estates/
path= -> Deve rimanere vuoto
idContratto= { "1": "Vendita", "2": "Affitto", "14": "Asta" }
criterio=prezzo
pag= pagina
prezzoMinimo=0
prezzoMassimo=100000
idProvincia=AO
idCategoria= "options": [
          {
            "label": "Case - Appartamenti",
            "value": { "idCategoria": 1 },
            "options": [
              {
                "label": "Appartamento",
                "value": { "idTipologia": "4" },
                "path": "0.0"
              },
              {
                "label": "Attico - Mansarda",
                "value": { "idTipologia": "5" },
                "path": "0.1"
              },
              {
                "label": "Casa indipendente",
                "value": { "idTipologia": "7" },
                "path": "0.2"
              },
              {
                "label": "Loft",
                "value": { "idTipologia": "31" },
                "path": "0.3"
              },
              {
                "label": "Rustico - Casale",
                "value": { "idTipologia": "11" },
                "path": "0.4"
              },
              {
                "label": "Villa",
                "value": { "idTipologia": "12" },
                "path": "0.5"
              },
              {
                "label": "Villetta a schiera",
                "value": { "idTipologia": "13" },
                "path": "0.6"
              }
            ],
            "path": "0",
            "depth": 1
          },
          {
            "label": "Nuove costruzioni",
            "value": { "idCategoria": 6 },
            "options": [
              {
                "label": "Appartamento",
                "value": { "idTipologia": "54" },
                "path": "1.0"
              },
              {
                "label": "Attico - Mansarda",
                "value": { "idTipologia": "85" },
                "path": "1.1"
              },
              {
                "label": "Capannone",
                "value": { "idTipologia": "59" },
                "path": "1.2"
              },
              {
                "label": "Loft",
                "value": { "idTipologia": "60" },
                "path": "1.3"
              },
              {
                "label": "Magazzino",
                "value": { "idTipologia": "61" },
                "path": "1.4"
              },
              {
                "label": "Negozio",
                "value": { "idTipologia": "55" },
                "path": "1.5"
              },
              {
                "label": "Ufficio",
                "value": { "idTipologia": "56" },
                "path": "1.6"
              },
              {
                "label": "Villa - Villetta",
                "value": { "idTipologia": "58" },
                "path": "1.7"
              }
            ],
            "path": "1",
            "depth": 1
          },
          {
            "label": "Stanze - Posti letto",
            "value": { "idCategoria": 4 },
            "options": [
              {
                "label": "Stanza completa",
                "joinWith": "in",
                "value": { "categoriaStanza": 2 },
                "path": "2.0"
              },
              {
                "label": "Posto letto",
                "joinWith": "in",
                "value": { "categoriaStanza": 1 },
                "path": "2.1"
              }
            ],
            "path": "2",
            "depth": 1
          },
          {
            "label": "Garage - Posti auto",
            "value": { "idCategoria": 22 },
            "options": [],
            "path": "3",
            "depth": 0
          },
          {
            "label": "Palazzi - Edifici",
            "value": { "idCategoria": 20 },
            "options": [],
            "path": "4",
            "depth": 0
          },
          {
            "label": "Uffici - Coworking",
            "value": { "idCategoria": 23 },
            "options": [],
            "path": "5",
            "depth": 0
          },
          {
            "label": "Negozi - Locali commerciali",
            "value": { "idCategoria": 26 },
            "options": [
              {
                "label": "Locale commerciale",
                "value": { "tipologiaCommerciale": 1 },
                "path": "6.0"
              },
              {
                "label": "Laboratorio",
                "value": { "tipologiaCommerciale": 2 },
                "path": "6.1"
              },
              {
                "label": "Attivit\u00e0 commerciale",
                "value": { "tipologiaCommerciale": 3 },
                "path": "6.2"
              }
            ],
            "path": "6",
            "depth": 1
          },
          {
            "label": "Magazzini - Depositi",
            "value": { "idCategoria": 21 },
            "options": [],
            "path": "7",
            "depth": 0
          },
          {
            "label": "Capannoni",
            "value": { "idCategoria": 25 },
            "options": [],
            "path": "8",
            "depth": 0
          },
          {
            "label": "Terreni",
            "value": { "idCategoria": 24 },
            "options": [
              {
                "label": "Terreno Agricolo",
                "value": { "idTipologia": 106 },
                "path": "9.0"
              },
              {
                "label": "Terreno edificabile",
                "value": { "idTipologia": 107 },
                "path": "9.1"
              }
            ],
            "path": "9",
            "depth": 1
          }
        ],




All'interno del JSON c'è maxPages -> Se maxPages > 80 -> Bisogna ridurre il numero di annunci nella richiesta