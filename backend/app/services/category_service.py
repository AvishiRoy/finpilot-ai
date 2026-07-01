from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate
from app.models.category import Category


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def get_categories(self, user_id: int) -> list[Category]:
        return self.repository.get_all_for_user(user_id)

    def create_category(self, data: CategoryCreate, user_id: int) -> Category:
        if data.type not in ("income", "expense"):
            raise ValueError("Category type must be 'income' or 'expense'.")
        return self.repository.create(
            name=data.name,
            type=data.type,
            user_id=user_id,
            description=data.description,
        )

    def delete_category(self, category_id: int, user_id: int) -> None:
        category = self.repository.get_by_id(category_id)
        if category is None:
            raise ValueError("Category not found.")
        if category.is_default:
            raise ValueError("System default categories cannot be deleted.")
        if category.user_id != user_id:
            raise PermissionError("You can only delete your own categories.")
        self.repository.delete(category)