class ProductService:
    def get_product(self, product_id):
        return {
            "id": product_id,
            "name": "Demo Product"
        }

def get_product_service():
    return ProductService()