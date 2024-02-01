all: all the relations involving at least one person entity

filtered: all the relations involving at least one person entity except "related-to" and "compare" (which are not
covered by the hierarchy)

hierarchy: all the relations involving at least one person entity except "related-to" and "compare" (which are not
covered by the hierarchy). The fine-grained relation types have been mapped into the hierarchy types.

swapped: all the relations involving at least one person entity except "related-to" and "compare" (which are not
covered by the hierarchy). The fine-grained relation types have been mapped into the hierarchy types. The role 
(position-held) and general-affiliation and part-of (member) are swapped so that the entity person is always in position 1.
