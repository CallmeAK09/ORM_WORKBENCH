import contextlib

from django.db import models 

@contextlib.contextmanager
def enforce_validation():
    """
    Monkey-patch models.Model.save to call full_clean() before saving.
    This ensures that Django's validation (max_length, blank, etc.) is enforced.
    """

    original_save = models.Model.save

    def save_validated(self, *args, **kwargs):
        # We call full_clean() to trigger Django's field validation.
        # This will raise a ValidationError if constraints are violated.
        self.full_clean()
        return original_save(self, *args, **kwargs)

    models.Model.save = save_validated

    try:
        yield
    finally:
        models.Model.save = original_save