from .models import AffiliatedUniversity

class AffiliatedUniversityRepository:
    @staticmethod
    def get_by_affiliation_id(self, affiliation_id):
        """get affiliation university"""
        AffiliatedUniversity.objects.get(id=affiliation_id)

    @staticmethod
    def get_all(self):
        """Retrieve all universities."""
        return AffiliatedUniversity.objects.all()