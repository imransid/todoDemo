from .models import AffiliatedUniversity

class AffiliatedUniversityService:
    @staticmethod
    def create_affiliated_university( affiliation):
        """create affiliated university"""
        affiliation_university = AffiliatedUniversity.objects.create(**affiliation)
        return affiliation_university

    @staticmethod
    def get_all_affiliation_university():
        """get affiliation university"""
        return AffiliatedUniversity.objects.all()

    @staticmethod
    def get_affiliation_university( affiliation_id):
        """get affiliation university"""
        return AffiliatedUniversity.objects.get(id=affiliation_id)

    @staticmethod
    def update_affiliation_university(self, affiliation_id, updated_affiliation_university):
        """update affiliation university"""
        affiliation_university = self.get_affiliation_university(affiliation_id)
        for field, value in updated_affiliation_university.items():
            setattr(affiliation_university, field, value)
        affiliation_university.save()
        return affiliation_university

    @staticmethod
    def remove_affiliation_university(self, affiliation_id):
        """get affiliation university"""
        affiliation_university = self.get_affiliation_university(affiliation_id)
        affiliation_university.delete()
        return affiliation_university