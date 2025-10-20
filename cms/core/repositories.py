from .models import AffiliatedUniversity

class AffiliatedUniversityRepository:
    @staticmethod
    def get_by_id(affiliation_id):
        """Get an affiliated university by ID."""
        try:
            return AffiliatedUniversity.objects.get(id=affiliation_id)
        except AffiliatedUniversity.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        """Retrieve all affiliated universities."""
        return AffiliatedUniversity.objects.all()

    @staticmethod
    def create(data):
        """Create a new affiliated university."""
        return AffiliatedUniversity.objects.create(**data)

    @staticmethod
    def update(affiliation_id, data):
        """Update an existing affiliated university."""
        university = AffiliatedUniversity.objects.get(id=affiliation_id)
        for field, value in data.items():
            setattr(university, field, value)
        university.save()
        return university

    @staticmethod
    def delete(affiliation_id):
        """Delete an affiliated university."""
        try:
            university = AffiliatedUniversity.objects.get(id=affiliation_id)
            university.delete()
            return True
        except AffiliatedUniversity.DoesNotExist:
            return False
