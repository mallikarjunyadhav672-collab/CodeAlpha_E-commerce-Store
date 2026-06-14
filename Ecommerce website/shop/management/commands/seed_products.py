from django.core.management.base import BaseCommand
from shop.models import Product

DATA = [
  { 'name':'Premium Leather Jacket', 'brand':'LUXE Originals','price':4999,'old_price':7999,'img':'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&auto=format&fit=crop','badge':'sale','category':'fashion','rating':4.8,'reviews':124 },
  { 'name':'Wireless Pro Earbuds','brand':'SoundElite','price':2499,'old_price':3999,'img':'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&auto=format&fit=crop','badge':'sale','category':'electronics','rating':4.9,'reviews':256 },
  { 'name':'Minimalist Watch','brand':'Chrono Co.','price':8999,'old_price':None,'img':'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&auto=format&fit=crop','badge':'new','category':'fashion','rating':4.7,'reviews':89 },
  { 'name':'Luxury Sofa Set','brand':'HomeVibe','price':34999,'old_price':49999,'img':'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&auto=format&fit=crop','badge':'sale','category':'home','rating':4.6,'reviews':43 },
  { 'name':'Serum Glow Kit','brand':'BeautyLux','price':1299,'old_price':None,'img':'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&auto=format&fit=crop','badge':'new','category':'beauty','rating':4.8,'reviews':315 },
  { 'name':'Ultra 4K Camera','brand':'PixelPro','price':59999,'old_price':None,'img':'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&auto=format&fit=crop','badge':'new','category':'electronics','rating':5.0,'reviews':67 },
  { 'name':'Designer Sneakers','brand':'StrideLux','price':3499,'old_price':5999,'img':'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&auto=format&fit=crop','badge':'sale','category':'fashion','rating':4.5,'reviews':198 },
  { 'name':'Scented Candle Set','brand':'AromaLife','price':799,'old_price':None,'img':'https://images.unsplash.com/photo-1602781914733-3a99a7a7e0cb?w=400&auto=format&fit=crop','badge':'new','category':'home','rating':4.7,'reviews':432 },
    # additional products
    { 'name':'Cashmere Scarf','brand':'LuxeWeave','price':2599,'old_price':None,'img':'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=400&auto=format&fit=crop','badge':'new','category':'fashion','rating':4.6,'reviews':54 },
    { 'name':'Portable Espresso Maker','brand':'BrewMaster','price':6999,'old_price':8999,'img':'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=400&auto=format&fit=crop','badge':'sale','category':'home','rating':4.4,'reviews':23 },
    { 'name':'Hydrating Night Cream','brand':'GlowWorks','price':1599,'old_price':1999,'img':'https://images.unsplash.com/photo-1585155778353-8b0b5a4f8b6a?w=400&auto=format&fit=crop','badge':'new','category':'beauty','rating':4.9,'reviews':142 },
    { 'name':'Smart Home Hub','brand':'Nestify','price':8999,'old_price':10999,'img':'https://images.unsplash.com/photo-1582719478250-3d2a9b0a1f11?w=400&auto=format&fit=crop','badge':'new','category':'electronics','rating':4.5,'reviews':88 },
]

class Command(BaseCommand):
    help = 'Seed sample products into the database'

    def handle(self, *args, **options):
        created = 0
        for item in DATA:
            obj, _ = Product.objects.get_or_create(
                name=item['name'], defaults={
                    'brand': item['brand'], 'price': item['price'], 'old_price': item['old_price'],
                    'img': item['img'], 'badge': item['badge'], 'category': item['category'],
                    'rating': item['rating'], 'reviews': item['reviews']
                }
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(DATA)} products (or ensured they exist).'))
