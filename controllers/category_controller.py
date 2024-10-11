from models.category_model import CategoryModel

class CategoryController:
    def __init__(self, mysql):
        self.category_model = CategoryModel(mysql)

    def get_all_categories(self):
        return self.category_model.get_all_categories()
