from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=120)
    price = models.IntegerField()
    old_price = models.IntegerField(null=True, blank=True)
    img = models.URLField(max_length=1000, blank=True)
    badge = models.CharField(max_length=32, blank=True)
    category = models.CharField(max_length=80, blank=True)
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'oldPrice': self.old_price,
            'img': self.img,
            'badge': self.badge,
            'category': self.category,
            'rating': float(self.rating),
            'reviews': int(self.reviews),
        }

    def __str__(self):
        return f"{self.brand} - {self.name}"


class Cart(models.Model):
    # session-scoped cart (anonymous). For logged-in users you could add a ForeignKey to User.
    session_key = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def items_mapping(self):
        return {str(item.product_id): item.qty for item in self.items.all()}

    def __str__(self):
        return f"Cart {self.session_key} ({self.items.count()} items)"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} x{self.qty}"


class NewsletterEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
