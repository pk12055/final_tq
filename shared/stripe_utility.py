import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeUtility(object):

    def __init__(self, customer_code=None, subscription_code=None, coupon_code=None, token=None, email=None, name=None):
        self.token = token
        self.customer_code = customer_code
        self.subscription_code = subscription_code
        self.email = email
        self.coupon_code = coupon_code
        self.name = name

    def get_or_create_customer(self):
        """
        Using this function to get or create a customer using by the 'customer_code' or 'token',
        'email' of the customer.
        """

        if self.customer_code:
            customer = stripe.Customer.retrieve(self.customer_code)
        else:
            customer = stripe.Customer.create(
                card=self.token,
                email=self.email
            )
        self.customer_code = customer.id

        return customer

    def get_or_create_subscription(self):
        """
        Using this function to get or create the subscription of the customer by using
        'subscription_code' or 'customer_code', and 'coupon_code'.
        """

        if self.subscription_code:
            subscription = stripe.Subscription.retrieve(self.subscription_code)
            customer = subscription.customer
        else:
            customer = self.get_or_create_customer()
            subscription = stripe.Subscription.create(
                customer=self.customer_code,
                items=[
                    {
                        "price": settings.STRIPE_PLAN_ID
                    }
                ],
                coupon=self.coupon_code
            )
            self.subscription_code = subscription.id

        return subscription, customer

    def cancel_subscription(self):
        """
        Using this function to cancel the subscription by using the 'subscription_code' till the
        period of the subscription ends.
        """

        stripe.Subscription.delete(self.subscription_code)
        return True

    def get_product(self, product_id):
        """
        This function is used to get the product of the subscription.
        """

        product = stripe.Product.retrieve(product_id)
        return product

    def validate_coupon(self):
        """
        This function is used to check if the coupon code entered by the user is valid or not
        """
        try:
            coupon = stripe.Coupon.retrieve(self.coupon_code)
            return coupon['valid']
        except:
            return False
