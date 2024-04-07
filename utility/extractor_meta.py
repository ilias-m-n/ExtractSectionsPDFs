# Auditor Applied Standard Section

_auditor_page_head = ["report of independent auditors",
                      "independent auditors report",
                      "independent audit report",
                      "auditors report",
                      "auditor report",
                      ]

"""
"we have audited the accompanying",
"we have audited the ... prepared by",
"we have audited the ... of",
"""
_auditor_1 = ["we have audited the",
              ]

"""
"management is responsible for the preparation and fair presentation ... in accordance with",
"management is responsible for the preparation of financial statements that give a true and fair view in accordance with",
"management is responsible for the preparation and fair presentation of",
"management is responsible for the preparation and fair presentation of ... in accordance with",
"management is responsible for the preparation and fair presentation of ... in accordance with"

"directors ... are responsible for the preparation ... true and fair ... in accordance with",
"directors are responsible for the preparation and fair presentation of ... in accordance with",
"directors ... are responsible for the preparation and true and fair presentation of ... in accordance with",
"directors are responsible for the preparation of ... give a true and fair view",
"""
_auditor_11 = ["management ... is responsible for the preparation and fair presentation",
               "the preparation of the ... are the responsibility of",
               "responsibilities for preparing the ... in accordance with",
               "these consolidated financial statements are the responsibility of",
                   "is responsible for",
               "directors ... are responsible for the preparation"
               ]

"""
"our responsibility is to express an opinion ... based on our audit",
"our responsibility is to express an opinion ... based on our audits",
"our responsibility is to audit and express an opinion ... in accordance with",


our responsibility is to express and opinion",
"""
_auditor_12 = ["our responsibility is to express an opinion",
               "our responsibility is to audit the",
               "our responsibilities",
               ]

"""
"we conducted our audit in accordance with",
"we conducted our audit of ... in accordance with",
"""
_auditor_2 = ["we conducted our audits in accordance with",
              "we conducted our audit ... in accordance with",
              "we conducted an independent audit in order to express an opinion",
              "our ... audit has been performed in accordance with",
              "our audit was conducted",
              ]

"""
"an audit involves performing procedures to obtain audit evidence about the amounts and disclosures in the financial statments",
"an audit involves performing procedures to obtain audit evidence about the amounts and the disclosures",
"an audit involves performing procedures to obtain audit evidence about the amounts and disclosures",
"an audit involves performing procedures to obtain audit evidence",

"an audit involves performing procedures to obtain",
"an audit includes ... evidence relevant to the amounts and disclosures",

"an audit includes ... evidence relevant to the amounts and disclosures",

"an  ... audit involves performing",
"an audit involves obtaining evidence about the amounts and disclosures in the financial statements",            
"""
_auditor_21 = ["an  ... audit involves ",
               "an ... audit includes",
               ]

"""
"we believe that the audit evidence we have obtained is sufficient and appropriate to provide a basis for our audit opinion",
"we believe that the audit evidence we have obtained is sufficient and appropriate to provide a basis for our opinion",
"we believe that the audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our opinion."
"we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our audit opinion",
"""
_auditor_3 = ["we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our ... opinion",
              "we believe that our audit provides a reasonable basis for our opinion",
              "we believe that our audits provide a reasonable basis for our opinion",
              ]

"""
"in our opinion ... present fairly ... in all material respects ... in accordance with",
"in our opinion ... present fairly ... in all material respects ... in conformity with",
"in our opinion ... is presented fairly ... in all material respects.",
"in our opinion ... give a true and fair view in conformity with",
"in our opinion ... give a true and fair view ... in accordance with",
"in our opinion ... give a true and fair view ... have been properly prepared in accordance with",
"in our opinion based on our findings of our audit ... comply with",


"in our opinion ... is in accordance with ... giving a true and fair view ... complying with",
"in our opinion ... in accordance with ... give a true and fair view",


"in our opinion ... in accordance with ... true and fair view",
"in our opinion ... are properly drawn up in accordance with"

"in our opinion ... give a true and fair view",


"in our opinion ... present fairly in all material respects ... in accordance with"
"""
_auditor_4 = ["in our opinion ... fairly ... in all material respects",
              "in our opinion ... comply with",
              "in our opinion ... true and fair view",
              "in our opinion ... in accordance with"
              ]

_auditor_sections = (_auditor_page_head, _auditor_1, _auditor_11, _auditor_12, _auditor_2, _auditor_21, _auditor_3, _auditor_4)


# Notes Applied Standard Section
"""
"notes to the consolidated financial statements",
"notes to the financial statements",
"""
_notes_head_page = ["accounting policies",
                    "basis of presentation of consolidated financial statements",
                    ]

_notes_head = ["basis of preparation",
               "basis of presentation",
               "basis of accounting",
               "statement of compliance",
               "accounting convention",
               "presentation of accounts"
               ]

_notes_head2 = ["summary of accounting policies",
                "statement of compliance",
                "significant accounting policies",
                "financial reporting standards",
                "basis of reporting"
                ]

"""
"consolidated financial statements have been prepared in compliance with",
"consolidated financial statements of ... have been prepared in accordance with",
"consolidated financial statements ... have been prepared in accordance with",
"consolidated financial statements are prepared in accordance with ... consolidated financial statements are prepared in accordance with",
"consolidated financial statements have been prepared in compliance with",
"consolidated financial statements ... have been prepared in compliance with",
"consolidated financial statements of ... have been prepared in accordance with"
"these consolidated financial statements are prepared in accordance with",

"consolidated financial statements ... prepared in compliance with",
"consolidated financial statements ... prepared in accordance with",

"financial statements have been prepared in accordance with",
"financial statements are prepared ... in accordance with",
"financial statements have been prepared to comply with",
"financial statements ... have been prepared in accordance with",
"financial statements have been drawn up in accordance with",

"financial statements ... prepared in compliance with",
"financial statements ... prepared ... in accordance with",
"financial statements ... prepared ... to comply with",

"the financial report is a general purpose financial report which has been prepared in accordance with",

"financial statements have been drawn up in accordance with",
"financial report ... has been prepared in accordance with",


"has been prepared in accordance with the",
"... are prepared ... in accordance with",
"""
_notes_1 = ["financial statements ... prepared ... with",
            "financial ... in accordance with",
            "prepared ... in accordance with",
            ]


_notes_sections = (_notes_head, _notes_head2, _notes_1)