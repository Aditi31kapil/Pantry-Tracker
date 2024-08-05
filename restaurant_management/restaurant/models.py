from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100,null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=30,null=False)
    last_name =models.CharField(max_length=30)
    dept =models.ForeignKey(Department,on_delete=models.CASCADE)
    salary =models.IntegerField(default=0)
    bonus=models.IntegerField(default=0)
    role=models.ForeignKey(Role, on_delete=models.CASCADE)
    phone=models.IntegerField(default=0)
    hire_date = models.DateField()

    def __str__(self):
        return "%s %s %s" %(self.first_name, self.last_name, self.phone)

class TableBooking(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Number = models.CharField(max_length=20)
    Person = models.PositiveIntegerField()
    Date = models.DateField()

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField('Category',related_name='item')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()

    def __str__(self):
        return f'Table {self.number}'
class OrderOnline(models.Model):
    created_on = models.DateTimeField(auto_now_add= True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I : %M %p" )}'

# class Order(models.Model):
#     table = models.ForeignKey(Table, on_delete=models.CASCADE)
#     items = models.ManyToManyField(MenuItem, through='OrderItem')
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

#     def __str__(self):
#         return f'Order {self.id} at Table {self.table.number}'

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.IntegerField()

#     def __str__(self):
#         return f'{self.quantity} x {self.menu_item.name} for Order {self.order.id}'