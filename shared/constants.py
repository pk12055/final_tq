class UserType():
    USERTYPE = (
        ('Consumer', 'Consumer'),
        ('Shop', 'Shop'),
        ('Brand', 'Brand'),
    )

    consumer = USERTYPE[0][0]
    own_shop = USERTYPE[1][0]
    own_brand = USERTYPE[2][0]


class AddressType():
    ADDRESSTYPE = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    )

    home = ADDRESSTYPE[0][0]
    office = ADDRESSTYPE[1][0]
    other = ADDRESSTYPE[2][0]


class StoreType():
    STORETYPE = (
        ('Public', 'Public'),
        ('Private', 'Private'),
    )

    public = STORETYPE[0][0]
    private = STORETYPE[1][0]


class SizeType():
    SIZETYPE = (
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    )

class Followchoice():
    FOLLOWCHOICE = (
        ('FOLLOW', 'FOLLOW'),
        ('UNFOLLOW', 'UNFOLLOW'),
    )


class productFor():
    PRODUCTFOR = (
        ('WOMEN', 'WOMEN'),
        ('MEN', 'MEN'),
        ('BOTH', 'BOTH'),
    )


class Favouritechoice():
    FAVOURITECHOICE = (
        ('FAVOURITE', 'FAVOURITE'),
        ('UNFavourite', 'UNFAVOURITE'),
    )

class QuantityType():
    QUANTITYTYPE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    )


class SaleType():
    SALETYPE = (
        ('Value', 'Value'),
        ('Percentage', 'Percentage'),
    )


class CategoryType():
    CATEGORYTYPE = (
        ('Activewears', 'Activewears'),
        ('Dresses', 'Dresses'),
        ('Jackets And Coats', 'Jackets And Coats'),
        ('Jumpsuits and Playsuits', 'Jumpsuits and Playsuits'),
        ('Knitwear', 'Knitwear'),
        ('Swimwear', 'Swimwear'),
        ('Tops', 'Tops'),
        ('Trouser', 'Trouser'),
        ('Accessories', 'Accessories'),
        ('Clothing', 'Clothing'),
        ('Other', 'Other'),
    )


WHO_WE_ARE_PARA_1 = 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters'

WHO_WE_ARE_PARA_2 = 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters'

WHO_WE_ARE_PARA_3 = 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters'

SHOP_DESCRIPTION = 'It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters'