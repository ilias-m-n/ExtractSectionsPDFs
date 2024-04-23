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

"we have audited"

"i have audited the consolidated balance sheets of"

"The Office of the Auditor General of Thailand has audited the"
"""
_auditor_1 = ["have audited the",
              "has audited the"
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

"these financial statements are the responsibility of the Company's management"
"""
_auditor_11 = ["management ... is responsible for the preparation and fair presentation",
               "the preparation of the ... are the responsibility of",
               "responsibilities for preparing the ... in accordance with",
               "these consolidated financial statements are the responsibility of",
               "is responsible for",
               "directors ... are responsible for the preparation",
               "are the responsibility of"
               ]


"""
"our responsibility is to express an opinion ... based on our audit",
"our responsibility is to express an opinion ... based on our audits",
"our responsibility is to audit and express an opinion ... in accordance with",


"our responsibility is to express and opinion",

"my responsibility is to express an opinion on these statements based on my audit."
"""
_auditor_12 = ["responsibility is to express an opinion",
               "responsibility is to audit the",
               "our responsibilities",
               'my responsibilities'
               ]


"""
"we conducted our audit in accordance with",
"we conducted our audit of ... in accordance with",

"we conducted an independent audit in order to express an opinion",
"our ... audit has been performed in accordance with",
"our audit was conducted",

"we conducted our audits in accordance with",
"we conducted our audit ... in accordance with",
"we conducted an independent audit in order to express an opinion",
"our ... audit has been performed in accordance with",
"our audit was conducted",

"I conducted my audit in accordance with "
"""
_auditor_2 = ["conducted our audits in accordance with",
              "conducted our audit ... in accordance with",
              "conducted an independent audit in order to express an opinion",
              "audit has been performed in accordance with",
              "audit was conducted",
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
_auditor_21 = ["an ... audit involves ",
               "an ... audit includes",
               ]


"""
"we believe that the audit evidence we have obtained is sufficient and appropriate to provide a basis for our audit opinion",
"we believe that the audit evidence we have obtained is sufficient and appropriate to provide a basis for our opinion",
"we believe that the audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our opinion."
"we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our audit opinion",

"we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our ... opinion",
"we believe that our audit provides a reasonable basis for our opinion",
"we believe that our audits provide a reasonable basis for our opinion",

"believes that the audit evidence"

"""
_auditor_3 = [
    "we believe that the ... audit evidence we have obtained ... is sufficient and appropriate to provide a basis for our ... opinion",
    "we believe that our audit provides a reasonable basis for our opinion",
    "we believe that our audits provide a reasonable basis for our opinion",
    "I believe that the ... audit evidence I have obtained ... is sufficient and appropriate to provide a basis for my ... opinion",
    "I believe that my audit provides a reasonable basis for my opinion",
    "I believe that my audits provide a reasonable basis for my opinion",
    "believes that the audit evidence ... has obtained is sufficient and appropriate to provide a basis"
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

"in our opinion ... in accordance with",

"in our opinion ... fairly ... in all material respects"
"in our opinion ... fairly ... in all material respects"

"in our opinion ... fairly ... in all material",
              "in our opinion ... comply with",
              "in our opinion ... true and fair view",
              "in our opinion ... in accordance with",
              "in our opinion ... in conformity with",
              "our opinion ... in accordance with",
              "in my opinion ... fairly ... in all material",
              "in my opinion ... comply with",
              "in my opinion ... true and fair view",
              "in my opinion ... in accordance with",
              "in my opinion ... in conformity with",
              
_auditor_42 = ["our opinion ... fairly ... in all material",
              "our opinion ... comply with",
              "our opinion ... true and fair view",
              "our opinion ... in accordance with",
              "our opinion ... in conformity with",
              "our opinion ... in accordance with",
              "my opinion ... fairly ... in all material",
              "my opinion ... comply with",
              "my opinion ... true and fair view",
              "my opinion ... in accordance with",
              "my opinion ... in conformity with",
              "in the ... opinion ... in all material respects",
               
               ]
"""
_auditor_4 = [
              "in the ... opinion ... in all material respects",
              "in our opinion ... the ... financial statements ... in conformity with",
              "in our opinion ... the ... financial statements ... in accordance with",
              "in our opinion ... the ... financial statements ... comply with",
              "in our opinion ... these ... financial Statements ... in accordance with",
              "in our opinion ... these ... financial Statements ... in conformity with",
              "in our opinion ... these ... financial Statements ... comply with",
              "in my opinion ... the ... financial statements ... in conformity with",
              "in my opinion ... the ... financial statements ... in accordance with",
              "in my opinion ... the ... financial statements ... comply with",
              "in my opinion ... these ... financial Statements ... in accordance with",
              "in my opinion ... these ... financial Statements ... in conformity with",
              "in my opinion ... these ... financial Statements ... comply with",
              ]

"""
_auditor_std = ["the consolidated financial statements referred to above present fairly, in all material respects ... in conformity with",
                "in our opinion ... the financial report of ... in accordance with ... a true and fair view ... complying with",
                "in our opinion ... the group financial statements give a true and fair view ... in accordance with",
                "the group financial statements have been properly prepared in accordance with",
                "in our opinion, based on our findings of our audit, the consolidated financial statements comply with",
                "in our opinion, the consolidated financial statements present fairly, in all material respects ... in accordance with",
                "in our opinion, the consolidated financial statements of ... in accordance with",
                "in our opinion ... the financial statements give a true and fair view of ... in accordance with",
                "in our opinion, these Financial Statements present fairly, in all material respects, the consolidated and separate financial position of",
                "in our opinion, the consolidated financial statements present fairly, in all material respects ... in accordance with",
                "in our opinion, the financial statements of the Group ... in accordance with"
                "in our opinion, the consolidated financial statements present fairly, in all material respects ... in accordance with",
                "in our opinion ... financial statements give the information required by ... and give a true and fair view in conformity with",
                "in our opinion ... financial statements give a true and fair view of ... in accordance with"]

_auditor_std_simple = ["in conformity with",
                       "in accordance with",
                       "complying with",
                       "comply with",
                       ]

in our opinion ... the consolidated financial statements present fairly, in all material respects ... in accordance with

"in our opinion ... the ... consolidated financial statements give the information required by ... give a true and fair view in conformity with",
"in our opinion ... the consolidated financial statements ... present fairly ... material respects ... in accordance with",
"in our opinion ... these ... financial Statements ... present fairly ... material respects ... in accordance with",
"in our opinion ... the ... consolidated financial statements ... are properly drawn up in accordance with",
"in our opinion ... the ... consolidated financial statements give the information required by ... give a true and fair view in accordance with",
"in our opinion ... the consolidated financial statements ... present fairly ... material respects ... in conformity with",
"in our opinion ... these ... financial Statements ... present fairly ... material respects ... in conformity with",
"in our opinion ... the ... consolidated financial statements ... are properly drawn up in conformity with",
"in our opinion ... the consolidated financial statements comply with"

"in our opinion ... the ... consolidated financial statements ... in conformity with",
"in our opinion ... the ... consolidated financial statements ... in accordance with",
"in our opinion ... the ... consolidated financial statements ... comply with",
"in our opinion ... these ... financial Statements ... in accordance with",
 "in our opinion ... these ... financial Statements ... in conformity with",
 "in our opinion ... these ... financial Statements ... comply with",
 "in my opinion ... the ... consolidated financial statements ... in conformity with",
 "in my opinion ... the ... consolidated financial statements ... in accordance with",
 "in my opinion ... the ... consolidated financial statements ... comply with",
 "in my opinion ... these ... financial Statements ... in accordance with",
 "in my opinion ... these ... financial Statements ... in conformity with",
 "in my opinion ... these ... financial Statements ... comply with",
"""
_auditor_cons_std = ["in our opinion ... the ... financial statements ... in conformity with",
                     "in our opinion ... the ... financial statements ... in accordance with",
                     "in our opinion ... the ... financial statements ... comply with",
                     "in our opinion ... these ... financial Statements ... in accordance with",
                     "in our opinion ... these ... financial Statements ... in conformity with",
                     "in our opinion ... these ... financial Statements ... comply with",
                     "in my opinion ... the ... financial statements ... in conformity with",
                     "in my opinion ... the ... financial statements ... in accordance with",
                     "in my opinion ... the ... financial statements ... comply with",
                     "in my opinion ... these ... financial Statements ... in accordance with",
                     "in my opinion ... these ... financial Statements ... in conformity with",
                     "in my opinion ... these ... financial Statements ... comply with",
                     ]

"""
"""
_auditor_fin_std = ["in our opinion ... the --- financial statements ... in conformity with ",
                    "in our opinion ... the --- financial statements ... in accordance with",
                    "in our opinion ... the financial report ... in accordance with ... complying with"
                    ]


_auditor_sections = (_auditor_1, _auditor_11, _auditor_12, _auditor_2, _auditor_21, _auditor_3, _auditor_4, )
_auditor_standards = (_auditor_cons_std, _auditor_fin_std, )


# Notes Applied Standard Section
"""
"notes to the consolidated financial statements",
"notes to the financial statements",
"""
_notes_head_page = ["accounting policies",
                    "basis of presentation of consolidated financial statements",
                    "accounting standards"
                    ]

_notes_head = ["basis of preparation",
               "basis of presentation",
               "basis of accounting",
               "statement of compliance",
               "accounting convention",
               "presentation of accounts",
               'bases of preparation',
               'accounting policies',
               'accounting principles'
               ]

_notes_head2 = ["summary of accounting policies",
                "statement of compliance",
                "significant accounting policies",
                "financial reporting standards",
                "basis of reporting",
                "presentation of ... financial statements",
                ''
                'applied rules'
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

These Financial Statements have been prepared according to
"""
_notes_1 = ["financial statements ... prepared ... with",
            "financial ... in accordance with",
            "financial ... prepared ... according to",
            "prepared ... in accordance with",
            ]



"""
_notes_std_simple = ["prepared ... with",
              "according to",
              "in accordance with",
              ]

these financial statements have been prepared to comply with
the financial statements have been prepared in accordance with ??? last year ???
the financial  statements  are  prepared  under  the  historical  cost  convention  in  accordance  with
the financial statements of the Group and of the Company have been prepared in accordance with
The financial statements have been drawn up in accordance with
The consolidated Financial Statements and the separate Financial Statements have been prepared in compliance with
The accounts are prepared on a going concern basis (see page 300 of the Report of the directors) and in accordance with
The consolidated financial statements of the Group and the balance sheet and statement of changes in equity of the Company have been prepared in accordance with
The consolidated financial statements have been prepared in compliance with
The consolidated financial statements of Deutsche Telekom have been prepared in accordance with
The financial statements have been prepared in accordance with
The financial report is a general purpose financial report which has been prepared in accordance with
The consolidated financial statements of the Company have been prepared in accordance with
These consolidated financial statements are prepared in accordance with
The separate financial statements have been prepared in compliance with
The consolidated financial statements have been prepared in compliance with

the consolidated financial statements and disclosures have been prepared in accordance with ??? standard mentioned in next sentence 
The accompanying consolidated financial statements are prepared in accordance with Communiqué Serial II, No:14.1, “Principles of Financial Reporting
in Capital Markets” (“the Communiqué”) published in the Official Gazette numbered 28676 on 13 June 2013. According to Article 5 of the Communiqué,
consolidated financial statements are prepared in accordance with the Turkish Accounting Standards issued by Public Oversight Accounting and
Auditing Standards Authority (“POAASA”).


The accompanying consolidated financial statements are prepared in accordance with Communiqué Serial II, No:14.1, “Principles of Financial Reporting
in Capital Markets” (“the Communiqué”) published in the Official Gazette numbered 28676 on 13 June 2013. According to Article 5 of the Communiqué,
consolidated financial statements are prepared in accordance with the Turkish Accounting Standards issued by Public Oversight Accounting and
Auditing Standards Authority (“POAASA”).

"""
_notes_std = ["these ... financial statements ... prepared ... comply with",
              "these ... financial statements ... prepared ... in accordance with",
              "these ... financial statements ... prepared ... in compliance with",
              "these ... financial statements ... presented ... in accordance with",
              "the ... financial statements ... prepared ... in accordance with",
              "the ... financial statements ... presented ... in accordance with",
              "the ... financial statements ... presented ... in compliance with",
              "the ... financial statements ... prepared ... in compliance with",
              "the ... financial statements ... prepared ... comply with",
              "the ... financial statements ... drawn up ... in accordance with",
              "the ... financial statements ... drawn up ... in compliance with",
              "the ... financial statements ... drawn up ... comply with",
              "the accounts ... prepared ... in accordance with",
              "the ... financial report ... prepared ... in accordance with",
              "the ... prepares its financial statements in accordance with",
              "the ... prepares its financial statements in compliance with",
]


_notes_sections = (_notes_head, _notes_head2, _notes_1, )
_notes_standards = (_notes_std, )
