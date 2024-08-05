from django.contrib import admin
from restaurant.models import Category, OrderOnline, TableBooking, MenuItem, InventoryItem, Table,Employee,Role,Department

admin.site.register(TableBooking)
admin.site.register(InventoryItem)
admin.site.register(Table)
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderOnline)
