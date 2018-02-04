DEP_TAG_NOUN_SUBJECT = 'nsubj'
POS_TAG_VERB = 'VERB'

def is_full_sentence(span):
    subject_present = False
    verb_present = False
    for token in span:
        if token.dep_ == DEP_TAG_NOUN_SUBJECT:
            subject_present = True
        if token.pos_ == POS_TAG_VERB:
            verb_present = True
        if subject_present and verb_present:
            return True
    return False
