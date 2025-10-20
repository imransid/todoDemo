from .repositories import AffiliatedUniversityRepository

class AffiliatedUniversityService:
    repository = AffiliatedUniversityRepository()

    def get_all_affiliation_university(self):
        return self.repository.get_all()

    def get_affiliation_university(self, affiliation_id):
        return self.repository.get_by_id(affiliation_id)

    def create_affiliated_university(self, data):
        return self.repository.create(data)

    def update_affiliation_university(self, affiliation_id, data):
        return self.repository.update(affiliation_id, data)

    def remove_affiliation_university(self, affiliation_id):
        return self.repository.delete(affiliation_id)