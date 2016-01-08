
@auth.requires_membership(role='administrators')
def listing():
    return dict()
