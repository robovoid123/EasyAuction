from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_shops():
    pass


@router.post('/')
def create_shop():
    pass


@router.put('/{id}')
def update_shop():
    pass


@router.get('/{id}')
def get_shop():
    pass


@router.delete('/{id}')
def delete_shop():
    pass


@router.post('/{id}/products')
def add_product_in_shop():
    pass


@router.get('/{id}/products')
def get_products_in_shop():
    pass


@router.get('/{id}/products/{prod_id}')
def get_product_in_shop():
    pass


@router.delete('/{id}/products/{prod_id}')
def remove_product_from_shop():
    pass
