from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    id: str
    name: str
    category: str
    price: float
    available_qty: int
    description: str
    spice_level: str = "Medium"


INITIAL_MENU: List[Dict] = [
    {
        "id": "butter-chicken",
        "name": "Butter Chicken",
        "category": "Curry",
        "price": 350.0,
        "available_qty": 5,
        "description": "Tender chicken pieces simmered in a velvety tomato and butter gravy.",
        "spice_level": "Medium",
    },
    {
        "id": "paneer-tikka",
        "name": "Paneer Tikka",
        "category": "Starter",
        "price": 250.0,
        "available_qty": 8,
        "description": "Marinated cottage cheese cubes grilled to perfection with bell peppers and onions.",
        "spice_level": "Mild",
    },
    {
        "id": "hyderabadi-biryani",
        "name": "Hyderabadi Biryani",
        "category": "Rice",
        "price": 220.0,
        "available_qty": 10,
        "description": "Fragrant basmati rice layered with aromatic spices and saffron.",
        "spice_level": "Spicy",
    },
    {
        "id": "dal-makhani",
        "name": "Dal Makhani",
        "category": "Curry",
        "price": 180.0,
        "available_qty": 6,
        "description": "Black lentils slow-cooked overnight with fresh cream and butter.",
        "spice_level": "Mild",
    },
    {
        "id": "garlic-naan",
        "name": "Garlic Naan",
        "category": "Bread",
        "price": 60.0,
        "available_qty": 20,
        "description": "Crispy traditional tandoori flatbread infused with roasted garlic and coriander.",
        "spice_level": "Mild",
    },
    {
        "id": "gulab-jamun",
        "name": "Gulab Jamun (2 pcs)",
        "category": "Dessert",
        "price": 90.0,
        "available_qty": 12,
        "description": "Golden fried milk-solid dumplings soaked in rose and cardamom sugar syrup.",
        "spice_level": "Mild",
    },
]


class MenuRepository:
    """Thread-safe in-memory menu repository with inventory management."""

    def __init__(self):
        self._menu: Dict[str, MenuItem] = {}
        self.reset()

    def reset(self) -> None:
        """Reset menu back to initial stock."""
        self._menu = {item["id"]: MenuItem(**item) for item in INITIAL_MENU}

    def get_all(self) -> List[MenuItem]:
        """Return all menu items with current stock."""
        return list(self._menu.values())

    def get_by_id(self, item_id: str) -> Optional[MenuItem]:
        """Get an item by exact ID."""
        return self._menu.get(item_id)

    def find_by_name(self, query: str) -> Optional[MenuItem]:
        """Find a dish by fuzzy, case-insensitive match or alias."""
        if not query:
            return None
        q = query.strip().lower()

        # 1. Exact match on name
        for item in self._menu.values():
            if item.name.lower() == q:
                return item

        # 2. Known aliases / key words
        alias_map = {
            "butter chicken": "butter-chicken",
            "murg makhani": "butter-chicken",
            "paneer tikka": "paneer-tikka",
            "paneer": "paneer-tikka",
            "biryani": "hyderabadi-biryani",
            "hyderabadi biryani": "hyderabadi-biryani",
            "dal makhani": "dal-makhani",
            "dal": "dal-makhani",
            "daal": "dal-makhani",
            "garlic naan": "garlic-naan",
            "naan": "garlic-naan",
            "gulab jamun": "gulab-jamun",
            "jamun": "gulab-jamun",
            "sweet": "gulab-jamun",
        }

        if q in alias_map:
            return self._menu.get(alias_map[q])

        # 3. Substring match
        for item in self._menu.values():
            if q in item.name.lower() or item.name.lower() in q:
                return item

        return None

    def reserve_stock(self, item_id: str, quantity: int) -> bool:
        """Decrement inventory if sufficient stock is available."""
        item = self._menu.get(item_id)
        if not item or item.available_qty < quantity or quantity <= 0:
            return False
        item.available_qty -= quantity
        return True

    def release_stock(self, item_id: str, quantity: int) -> bool:
        """Restore inventory if an order fails or is cancelled."""
        item = self._menu.get(item_id)
        if not item or quantity <= 0:
            return False
        item.available_qty += quantity
        return True


# Singleton instance
menu_repo = MenuRepository()

