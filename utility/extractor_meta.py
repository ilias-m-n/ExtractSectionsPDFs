# Auditor Applied Standard Section

_auditor_page_head = ["report of independent auditors",
                      "independent auditors report",
                      "independent audit report",
                      "auditors report",
                      "auditor report",
                      "audit report",
                     ]

_auditor_1 = ["we have audited the",
              "i have audited the",
              "has audited the",
              "we conducted an independent audit",
              "we have conducted an independent audit",
              "we expressed an ... audit opinion",
              ]
# maybe remove
_auditor_11 = ["management ... is responsible for the preparation and fair presentation",
               "the preparation of the ... are the responsibility of",
               "preparation of the ... is the responsibility of",
               "responsibilities for preparing the ... in accordance with",
               "these consolidated financial statements are the responsibility of",
               "is responsible for",
               "directors ... are responsible for the preparation",
               "are the responsibility of",
               "directors ... are responsible for preparing",
               ]

_auditor_12 = ["our responsibility is to express an opinion",
               "our responsibility is to audit the",
               "my responsibility is to express an opinion",
               "my responsibility is to audit the",
               "our responsibilities",
               'my responsibilities'
               ]

_auditor_2 = ["conducted our audits in accordance with",
              "conducted our audit ... in accordance with",
              "conducted an independent audit in order to express an opinion",
              "audit has been performed in accordance with",
              "audit was conducted",
              ]

_auditor_21 = ["an ... audit involves ",
               "an ... audit includes",
               ]

_auditor_3 = [
    "we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our ... opinion",
    "we believe that our audit provides a reasonable basis for our opinion",
    "we believe that our audits provide a reasonable basis for our opinion",
    "I believe that the ... audit evidence I have obtained ... is sufficient and appropriate to provide a basis for my ... opinion",
    "I believe that my audit provides a reasonable basis for my opinion",
    "I believe that my audits provide a reasonable basis for my opinion",
    "believes that the audit evidence ... has obtained is sufficient and appropriate to provide a basis"
    ]

_auditor_4 = [
"in the ... opinion ... in all material respects",

"in our opinion ... financial statements ... in conformity with",
"in our opinion ... financial statements ... in accordance with",
"in our opinion ... financial statements ... comply with",

"in my opinion ... financial statements ... in conformity with",
"in my opinion ... financial statements ... in accordance with",
"in my opinion ... financial statements ... comply with",
    
"in our opinion ... nancial statements ... in conformity with",
"in our opinion ... nancial statements ... in accordance with",
"in our opinion ... nancial statements ... comply with",

"in my opinion ... nancial statements ... in conformity with",
"in my opinion ... nancial statements ... in accordance with",
"in my opinion ... nancial statements ... comply with",

"in our opinion ... financial report ... in accordance with",
"in our opinion ... nancial report ... in accordance with"
]

_auditor_fin_std = [
    "in .... opinion ... ........nanci......... statements ... in conformity with",
    "in .... opinion ... ........nanci......... statements ... in accordance with",
    "in .... opinion ... ........nanci......... statements ... in compliance with",
    "in .... opinion ... ........nanci......... statements ... comply with",
    "in .... opinion ... ........nanci......... statements ... according to",
    "in .... opinion ... ........nanci......... statements ... aggreement with",
    "in .... opinion ... ........nanci......... statements ... with respect to",
    
    "in the ... opinion ... ........nanci......... statements ... in conformity with",
    "in the ... opinion ... ........nanci......... statements ... in accordance with",
    "in the ... opinion ... ........nanci......... statements ... in compliance with",
    "in the ... opinion ... ........nanci......... statements ... comply with",
    "in the ... opinion ... ........nanci......... statements ... according to",
    "in the ... opinion ... ........nanci......... statements ... in agreement with",
    "in the ... opinion ... ........nanci......... statements ... with respect to",
]

"""
                     "the ... accounts ... prepared ... in accordance with",
                     "the ... accounts ... prepared ... in conformity with",
                     "the ... accounts ... prepared ... in compliance with",
                     "the ... accounts ... prepared ... comply with",
                     "the ... accounts ... prepared ... according to",
                     "the ... accounts ... prepared ... aggreement with",
                     "the ... accounts ... prepared ... with respect to",
"""
_auditor_all_std = [ "in .... opinion ... ........nanci......... statements ... in conformity with",
                     "in .... opinion ... ........nanci......... statements ... in accordance with",
                     "in .... opinion ... ........nanci......... statements ... in compliance with",
                     "in .... opinion ... ........nanci......... statements ... comply with",
                     "in .... opinion ... ........nanci......... statements ... according to",
                     "in .... opinion ... ........nanci......... statements ... in agreement with",
                     "in .... opinion ... ........nanci......... statements ... with respect to",
                     
                     "in the ... opinion ... ........nanci......... statements ... in conformity with",
                     "in the ... opinion ... ........nanci......... statements ... in accordance with",
                     "in the ... opinion ... ........nanci......... statements ... in compliance with",
                     "in the ... opinion ... ........nanci......... statements ... comply with",
                     "in the ... opinion ... ........nanci......... statements ... according to",
                     "in the ... opinion ... ........nanci......... statements ... in agreement with",
                     "in the ... opinion ... ........nanci......... statements ... with respect to",

                     "in .... opinion ... ........nanci......... report ... in accordance with",
                     "in .... opinion ... ........nanci......... report ... in conformity with",
                     "in .... opinion ... ........nanci......... report ... in compliance with",
                     "in .... opinion ... ........nanci......... report ... comply with",
                     "in .... opinion ... ........nanci......... report ... according to",
                     "in .... opinion ... ........nanci......... report ... aggreement with",
                     "in .... opinion ... ........nanci......... report ... with respect to",

                     "in .... opinion ... annual report ... in accordance with",
                     "in .... opinion ... annual report ... in conformity with",
                     "in .... opinion ... annual report ... in compliance with",
                     "in .... opinion ... annual report ... comply with",
                     "in .... opinion ... annual report ... according to",
                     "in .... opinion ... annual report ... aggreement with",
                     "in .... opinion ... annual report ... with respect to",

                     "in .... opinion ... the ... accounts ... prepared ... in accordance with",
                     "in .... opinion ... the ... accounts ... prepared ... in conformity with",
                     "in .... opinion ... the ... accounts ... prepared ... in compliance with",
                     "in .... opinion ... the ... accounts ... prepared ... comply with",
                     "in .... opinion ... the ... accounts ... prepared ... according to",
                     "in .... opinion ... the ... accounts ... prepared ... aggreement with",
                     "in .... opinion ... the ... accounts ... prepared ... with respect to",
                   ]

_auditor_extr_std = ["in .... opinion ... ........nanci......... statements ... in conformity with",
                     "in .... opinion ... ........nanci......... statements ... in accordance with",
                     "in .... opinion ... ........nanci......... statements ... in compliance with",
                     "in .... opinion ... ........nanci......... statements ... comply with",
                     "in .... opinion ... ........nanci......... statements ... according to",
                     "in .... opinion ... ........nanci......... statements ... in agreement with",
                     "in .... opinion ... ........nanci......... statements ... with respect to",
                     "in .... opinion ... ........nanci......... statements ... published by",
                     
                     "in the ... opinion ... ........nanci......... statements ... in conformity with",
                     "in the ... opinion ... ........nanci......... statements ... in accordance with",
                     "in the ... opinion ... ........nanci......... statements ... in compliance with",
                     "in the ... opinion ... ........nanci......... statements ... comply with",
                     "in the ... opinion ... ........nanci......... statements ... according to",
                     "in the ... opinion ... ........nanci......... statements ... in agreement with",
                     "in the ... opinion ... ........nanci......... statements ... with respect to",
                     "in the ... opinion ... ........nanci......... statements ... published by",

                     "in .... opinion ... ........nanci......... report ... in accordance with",
                     "in .... opinion ... ........nanci......... report ... in conformity with",
                     "in .... opinion ... ........nanci......... report ... in compliance with",
                     "in .... opinion ... ........nanci......... report ... comply with",
                     "in .... opinion ... ........nanci......... report ... according to",
                     "in .... opinion ... ........nanci......... report ... aggreement with",
                     "in .... opinion ... ........nanci......... report ... with respect to",

                     "in .... opinion ... annual report ... in accordance with",
                     "in .... opinion ... annual report ... in conformity with",
                     "in .... opinion ... annual report ... in compliance with",
                     "in .... opinion ... annual report ... comply with",
                     "in .... opinion ... annual report ... according to",
                     "in .... opinion ... annual report ... aggreement with",
                     "in .... opinion ... annual report ... with respect to",

                     "in .... opinion ... the ... accounts ... in accordance with",
                     "in .... opinion ... the ... accounts ... in conformity with",
                     "in .... opinion ... the ... accounts ... in compliance with",
                     "in .... opinion ... the ... accounts ... comply with",
                     "in .... opinion ... the ... accounts ... according to",
                     "in .... opinion ... the ... accounts ... aggreement with",
                     "in .... opinion ... the ... accounts ... with respect to",
                   ]

# removed auditor_11
_auditor_sections = [_auditor_page_head, _auditor_1, _auditor_12, _auditor_2, _auditor_21, _auditor_3, _auditor_all_std, _auditor_all_std]
_auditor_standards = (_auditor_extr_std, )

#### Notes


# Notes Applied Standard Section

_notes_head = ["basis of preparation",
               "basis of presentation",
               "basis of accounting",
               "statement of compliance",
               "accounting convention",
               "presentation of accounts",
               'bases of preparation',
               'accounting policies',
               'accounting principles',
               #'financial information',
               ]

_notes_head2 = ["summary of accounting policies",
                "statement of compliance",
                "significant accounting policies",
                #"financial reporting standards",
                "basis of reporting",
                "presentation of ... financial statements",
                'applied rules',
                'general explanations',
                "consolidated statements and other financial information",
                ]

_notes_fin_std = [
                  # the/these ... financial/nancial stmts ... prepared/presented/drawn up
                  "the......... ... ........nanci......... statements ... ..... ... in accordance with",
                  "the......... ... ........nanci......... statements ... ..... ... in compliance with",
                  "the......... ... ........nanci......... statements ... ..... ... in conformity with",
                  "the......... ... ........nanci......... statements ... ..... ... comply ... with",
                  "the......... ... ........nanci......... statements ... ..... ... according to",

                  # the ... prepares/presents/draws up ... financial/nancial stmts
                  "the ... ...... ... ........nanci......... statements ... in accordance with",
                  "the ... ...... ... ........nanci......... statements ... in compliance with",
                  "the ... ...... ... ........nanci......... statements ... in conformity with",
                  "the ... ...... ... ........nanci......... statements ... comply ... with",
                  "the ... ...... ... ........nanci......... statements ... according to",

                  # prepared/presented/drawn up ... financial/nancial stmts
                  "..... ... ........nanci......... statements ... in accordance with",
                  "..... ... ........nanci......... statements ... in compliance with",
                  "..... ... ........nanci......... statements ... in conformity with",
                  "..... ... ........nanci......... statements ... in according to",
                  "..... ... ........nanci......... statements ... comply ... with",
             ]


"""
                  # accounts ... prepared/presented/drawn up
                  "the ... accounts ... ..... ... in accordance with",
                  "the ... accounts ... ..... ... in compliance with",
                  "the ... accounts ... ..... ... in conformity with",
                  "the ... accounts ... ..... ... comply ... with",
                  "the ... accounts ... ..... ... according to",
                  "the ... accounts ... ..... ... in agreement with",
                  "the ... accounts ... ..... ... with respect to",
"""
_notes_all_std = [# the/these ... financial/nancial stmts ... prepared/presented/drawn up
                  "the......... ... ........nanci......... statements ... ..... ... in accordance with",
                  "the......... ... ........nanci......... statements ... ..... ... in compliance with",
                  "the......... ... ........nanci......... statements ... ..... ... in conformity with",
                  "the......... ... ........nanci......... statements ... ..... ... comply ... with",
                  "the......... ... ........nanci......... statements ... ..... ... according to",
                  "the......... ... ........nanci......... statements ... ..... ... in agreement with",
                  "the......... ... ........nanci......... statements ... ..... ... with respect to",

                  # the/these ... financial/nancial stmts
                  "the......... ... ........nanci......... statements ... in accordance with",
                  "the......... ... ........nanci......... statements ... in compliance with",
                  "the......... ... ........nanci......... statements ... in conformity with",
                  "the......... ... ........nanci......... statements ... comply ... with",
                  "the......... ... ........nanci......... statements ... according to",
                  "the......... ... ........nanci......... statements ... in agreement with",
                  "the......... ... ........nanci......... statements ... with respect to",

                  # the ... prepares/presents/draws up ... financial/nancial stmts
                  "the ... ...... ... ........nanci......... statements ... in accordance with",
                  "the ... ...... ... ........nanci......... statements ... in compliance with",
                  "the ... ...... ... ........nanci......... statements ... in conformity with",
                  "the ... ...... ... ........nanci......... statements ... comply ... with",
                  "the ... ...... ... ........nanci......... statements ... according to",
                  "the ... ...... ... ........nanci......... statements ... in agreement with",
                  "the ... ...... ... ........nanci......... statements ... with respect to",

                  # prepared/presented/drawn up ... financial/nancial stmts
                  "..... ... ........nanci......... statements ... in accordance with",
                  "..... ... ........nanci......... statements ... in compliance with",
                  "..... ... ........nanci......... statements ... in conformity with",
                  "..... ... ........nanci......... statements ... comply ... with",
                  "..... ... ........nanci......... statements ... according to",
                  "..... ... ........nanci......... statements ... in agreement with",
                  "..... ... ........nanci......... statements ... with respect to",

                  # financial/nancial report ... prepared/presented/drawn up
                  "th.......... ... ........nanci......... report ... ..... ... in accordance with",
                  "th.......... ... ........nanci......... report ... ..... ... in compliance with",
                  "th.......... ... ........nanci......... report ... ..... ... in conformity with",
                  "th.......... ... ........nanci......... report ... ..... ... comply ... with",
                  "th.......... ... ........nanci......... report ... ..... ... according to",
                  "th.......... ... ........nanci......... report ... ..... ... in agreement with",
                  "th.......... ... ........nanci......... report ... ..... ... with respect to",

                    # financial/nancial report ... 
                  "th.......... ... ........nanci......... report ... in accordance with",
                  "th.......... ... ........nanci......... report ... in compliance with",
                  "th.......... ... ........nanci......... report ... in conformity with",
                  "th.......... ... ........nanci......... report ... comply ... with",
                  "th.......... ... ........nanci......... report ... according to",
                  "th.......... ... ........nanci......... report ... in agreement with",
                  "th.......... ... ........nanci......... report ... with respect to",

                  # annual report ... prepared/presented/drawn up
                  "th.......... ... annual report ... ..... ... in accordance with",
                  "th.......... ... annual report ... ..... ... in compliance with",
                  "th.......... ... annual report ... ..... ... in conformity with",
                  "th.......... ... annual report ... ..... ... comply ... with",
                  "th.......... ... annual report ... ..... ... according to",
                  "th.......... ... annual report ... ..... ... in agreement with",
                  "th.......... ... annual report ... ..... ... with respect to",

                  "the ... accounts ... ..... ... in accordance with",
                  "the ... accounts ... ..... ... in compliance with",
                  "the ... accounts ... ..... ... in conformity with",
                  "the ... accounts ... ..... ... comply ... with",
                  "the ... accounts ... ..... ... according to",
                  "the ... accounts ... ..... ... in agreement with",
                  "the ... accounts ... ..... ... with respect to",
             ]

_notes_extr_std = [# the/these ... financial/nancial stmts ... prepared/presented/drawn up
                  "the......... ... ........nanci......... statements ... ..... ... in accordance with",
                  "the......... ... ........nanci......... statements ... ..... ... in compliance with",
                  "the......... ... ........nanci......... statements ... ..... ... in conformity with",
                  "the......... ... ........nanci......... statements ... ..... ... comply ... with",
                  "the......... ... ........nanci......... statements ... ..... ... according to",
                  "the......... ... ........nanci......... statements ... ..... ... in agreement with",
                  "the......... ... ........nanci......... statements ... ..... ... with respect to",
                  "the......... ... ........nanci......... statements ... ..... ... under",

                  # the/these ... financial/nancial stmts
                  "the......... ... ........nanci......... statements ... in accordance with",
                  "the......... ... ........nanci......... statements ... in compliance with",
                  "the......... ... ........nanci......... statements ... in conformity with",
                  "the......... ... ........nanci......... statements ... comply ... with",
                  "the......... ... ........nanci......... statements ... according to",
                  "the......... ... ........nanci......... statements ... in agreement with",
                  "the......... ... ........nanci......... statements ... with respect to",
                  "the......... ... ........nanci......... statements ... under",

                  # the ... prepares/presents/draws up ... financial/nancial stmts
                  "the ... ...... ... ........nanci......... statements ... in accordance with",
                  "the ... ...... ... ........nanci......... statements ... in compliance with",
                  "the ... ...... ... ........nanci......... statements ... in conformity with",
                  "the ... ...... ... ........nanci......... statements ... comply ... with",
                  "the ... ...... ... ........nanci......... statements ... according to",
                  "the ... ...... ... ........nanci......... statements ... in agreement with",
                  "the ... ...... ... ........nanci......... statements ... with respect to",
                  "the ... ...... ... ........nanci......... statements ... under",

                  # prepared/presented/drawn up ... financial/nancial stmts
                  "..... ... ........nanci......... statements ... in accordance with",
                  "..... ... ........nanci......... statements ... in compliance with",
                  "..... ... ........nanci......... statements ... in conformity with",
                  "..... ... ........nanci......... statements ... comply ... with",
                  "..... ... ........nanci......... statements ... according to",
                  "..... ... ........nanci......... statements ... in agreement with",
                  "..... ... ........nanci......... statements ... with respect to",
                  "..... ... ........nanci......... statements ... under",

                  # financial/nancial report ... prepared/presented/drawn up
                  "th.......... ... ........nanci......... report ... ..... ... in accordance with",
                  "th.......... ... ........nanci......... report ... ..... ... in compliance with",
                  "th.......... ... ........nanci......... report ... ..... ... in conformity with",
                  "th.......... ... ........nanci......... report ... ..... ... comply ... with",
                  "th.......... ... ........nanci......... report ... ..... ... according to",
                  "th.......... ... ........nanci......... report ... ..... ... in agreement with",
                  "th.......... ... ........nanci......... report ... ..... ... with respect to",
                  "th.......... ... ........nanci......... report ... ..... ... under",

                    # financial/nancial report ... 
                  "th.......... ... ........nanci......... report ... in accordance with",
                  "th.......... ... ........nanci......... report ... in compliance with",
                  "th.......... ... ........nanci......... report ... in conformity with",
                  "th.......... ... ........nanci......... report ... comply ... with",
                  "th.......... ... ........nanci......... report ... according to",
                  "th.......... ... ........nanci......... report ... in agreement with",
                  "th.......... ... ........nanci......... report ... with respect to",
                  "th.......... ... ........nanci......... report ... under",

                  # annual report ... prepared/presented/drawn up
                  "th.......... ... annual report ... ..... ... in accordance with",
                  "th.......... ... annual report ... ..... ... in compliance with",
                  "th.......... ... annual report ... ..... ... in conformity with",
                  "th.......... ... annual report ... ..... ... comply ... with",
                  "th.......... ... annual report ... ..... ... according to",
                  "th.......... ... annual report ... ..... ... in agreement with",
                  "th.......... ... annual report ... ..... ... with respect to",
                  "th.......... ... annual report ... ..... ... under",

                  "the ... accounts ... ..... ... in accordance with",
                  "the ... accounts ... ..... ... in compliance with",
                  "the ... accounts ... ..... ... in conformity with",
                  "the ... accounts ... ..... ... comply ... with",
                  "the ... accounts ... ..... ... according to",
                  "the ... accounts ... ..... ... in agreement with",
                  "the ... accounts ... ..... ... with respect to",
                  "the ... accounts ... ..... ... under",
    
                  "nanci......... statements ... reported ... in accordance with",
                  "nanci......... statements ... reported ... in compliance with",
                  "nanci......... statements ... reported ... in conformity with",
                  "nanci......... statements ... reported ... comply ... with",
                  "nanci......... statements ... reported ... according to",
                  "nanci......... statements ... reported ... in agreement with",
                  "nanci......... statements ... reported ... with respect to",
                  "nanci......... statements ... reported ... under",
                    
             ]

_notes_sections = [_notes_head, _notes_head2, _notes_all_std, _notes_all_std]# _notes_all_std]
_notes_standards = (_notes_extr_std, )
