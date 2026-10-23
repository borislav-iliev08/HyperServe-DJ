from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils.text import slugify

from employees.models import Employee, EmployeeReview
from restaurants.models import Perks, Restaurant
from reviews.models import Review


class Command(BaseCommand):
    help = 'Create 20 fictional restaurants with perks, staff, and reviews.'

    restaurants = [
        ('Juniper & Rye', '12 Rakovski Street', 'Bulgarian', 'Mila Stoyanova', 'A seasonal neighborhood kitchen pairing slow-roasted meats with herbs, local grains, and bright pickles.', ['Outdoor seating', 'Vegetarian options', 'Private dining'], 'roast lamb with juniper jus'),
        ('Saffron Courtyard', '37 Angel Kanchev Street', 'Indonesian', 'Rina Santoso', 'An intimate Indonesian dining room serving fragrant rice plates, charcoal satay, and house-made sambals.', ['Outdoor seating', 'Vegan options', 'Takeaway'], 'charcoal chicken satay and coconut rice'),
        ('Casa del Sol', '5 William Gladstone Street', 'Spanish', 'Lucia Alvarez', 'A lively Spanish table for tapas, seasonal seafood, and long dinners shared over a thoughtful list of wines.', ['Outdoor seating', 'Private dining', 'Vegetarian options'], 'garlic prawns and smoked paprika potatoes'),
        ('Miso & Maple', '19 Iskar Street', 'Japanese', 'Hana Mori', 'A modern Japanese counter focused on careful broths, crisp tempura, and small plates made with local produce.', ['Takeaway', 'Free Wi-Fi', 'Vegetarian options'], 'miso-glazed aubergine and slow-simmered broth'),
        ('Pasta Verde', '28 Hristo Belchev Street', 'Italian', 'Giorgio Bianchi', 'Fresh pasta is rolled each morning and served with seasonal sauces, market vegetables, and regional Italian wines.', ['Vegetarian options', 'Vegan options', 'Private dining'], 'hand-cut tagliatelle with wild mushrooms'),
        ('Danube Hearth', '41 Tsar Samuil Street', 'Bulgarian', 'Georgi Iliev', 'A welcoming dining room celebrating Bulgarian comfort food with a wood-fired oven and ingredients from nearby farms.', ['Parking', 'Outdoor seating', 'Pet friendly'], 'wood-fired banitsa and slow-cooked beans'),
        ('Firebird Smokehouse', '16 Knyaz Boris I Street', 'American', 'Marcus Bennett', 'Low-and-slow barbecue, house pickles, and generous sides served in a relaxed smokehouse built for groups.', ['Parking', 'Takeaway', 'Free Wi-Fi'], 'smoked brisket with applewood and house pickles'),
        ('Lemon Grove Kitchen', '9 Solunska Street', 'Other', 'Nadia Petrova', 'A bright Mediterranean-inspired menu of grilled fish, citrus salads, and vegetable dishes in a leafy courtyard.', ['Outdoor seating', 'Vegan options', 'Pet friendly'], 'charred sea bass with lemon and fennel'),
        ('Basilica Trattoria', '22 Oborishte Street', 'Italian', 'Francesca Conti', 'A neighborhood trattoria with handmade ravioli, slow braises, and a short menu that changes with the season.', ['Private dining', 'Vegetarian options', 'Parking'], 'ricotta ravioli with sage butter'),
        ('Kumo Sushi Bar', '3 Shipka Street', 'Japanese', 'Kenji Sato', 'A small sushi bar serving carefully cut nigiri, seasonal sashimi, and warm rice bowls in a calm setting.', ['Takeaway', 'Free Wi-Fi', 'Parking'], 'salmon nigiri and seasonal sashimi'),
        ('Spice Route Sofia', '44 Vitosha Boulevard', 'Indonesian', 'Dewi Putri', 'Indonesian recipes meet a contemporary Sofia dining room, with aromatic curries, grilled seafood, and vegan plates.', ['Vegan options', 'Outdoor seating', 'Takeaway'], 'slow-cooked beef rendang and turmeric rice'),
        ('La Mesa Roja', '11 Graf Ignatiev Street', 'Spanish', 'Mateo Ruiz', 'An easygoing tapas bar with crisp croquetas, grilled vegetables, and paella made to share at the table.', ['Outdoor seating', 'Private dining', 'Free Wi-Fi'], 'saffron seafood paella and crisp croquetas'),
        ('Golden Apron', '7 Shishman Street', 'Bulgarian', 'Ivana Dimitrova', 'Modern Bulgarian cooking brings garden vegetables, mountain herbs, and traditional recipes together in polished plates.', ['Vegetarian options', 'Private dining', 'Parking'], 'grilled peppers with sirene and garden herbs'),
        ('North Star Brunch', '30 Gurko Street', 'American', 'Sophie Carter', 'A friendly all-day cafe serving careful coffee, buttermilk pancakes, and savory brunch favorites with local eggs.', ['Free Wi-Fi', 'Pet friendly', 'Takeaway'], 'buttermilk pancakes with seasonal fruit'),
        ('Olive Orchard', '25 Angel Kanchev Street', 'Other', 'Yasmin Haddad', 'Levantine and Mediterranean sharing plates bring warm flatbread, bright salads, and slow-roasted vegetables to the table.', ['Vegan options', 'Outdoor seating', 'Private dining'], 'zaatar flatbread with whipped labneh'),
        ('Tamarind House', '2 Pirotska Street', 'Indonesian', 'Arif Wibowo', 'A relaxed Indonesian kitchen built around fragrant broths, grilled skewers, and family recipes from across the islands.', ['Takeaway', 'Parking', 'Vegetarian options'], 'grilled beef skewers with peanut sauce'),
        ('Calle Ocho Tapas', '18 Lege Street', 'Spanish', 'Elena Garcia', 'Small plates, Spanish cheeses, and carefully prepared seafood make this a lively stop for an evening with friends.', ['Outdoor seating', 'Free Wi-Fi', 'Private dining'], 'patatas bravas with house-made aioli'),
        ('Riverstone Grill', '33 Opalchenska Street', 'American', 'Daniel Brooks', 'An open-fire grill serving responsibly sourced steaks, seasonal sides, and a concise menu of American classics.', ['Parking', 'Takeaway', 'Private dining'], 'ribeye steak with rosemary potatoes'),
        ('Nori & Noodles', '15 Aksakov Street', 'Japanese', 'Yuki Nakamura', 'A casual Japanese noodle house with rich ramen, crisp vegetable tempura, and quick lunches made from scratch.', ['Takeaway', 'Free Wi-Fi', 'Vegan options'], 'tonkotsu ramen with slow-braised pork'),
        ('The Sunday Table', '6 Benkovski Street', 'Bulgarian', 'Petya Nikolova', 'A warm, family-style restaurant serving seasonal Bulgarian dishes, fresh bread, and generous Sunday roasts every day.', ['Pet friendly', 'Outdoor seating', 'Vegetarian options'], 'slow-roasted pork with seasonal sides'),
    ]

    staff = [
        ('Mihail', 'Kostov', 'Radoslav', 'Marinov'), ('Ayu', 'Pratama', 'Bima', 'Hidayat'),
        ('Isabel', 'Moreno', 'Diego', 'Santos'), ('Emi', 'Kobayashi', 'Taro', 'Fujita'),
        ('Alessandro', 'Greco', 'Paolo', 'Moretti'), ('Kalin', 'Vasilev', 'Nikolay', 'Todorov'),
        ('Andre', 'Collins', 'Darius', 'Walker'), ('Mariya', 'Hristova', 'Stefan', 'Dobrev'),
        ('Chiara', 'Romano', 'Lorenzo', 'Ricci'), ('Sora', 'Yamamoto', 'Daichi', 'Kato'),
        ('Putri', 'Wijaya', 'Fajar', 'Nugroho'), ('Carlos', 'Navarro', 'Pablo', 'Vega'),
        ('Desislava', 'Petkova', 'Martin', 'Angelov'), ('Grace', 'Wilson', 'Ethan', 'Miller'),
        ('Samir', 'Khalil', 'Omar', 'Farah'), ('Intan', 'Permata', 'Dimas', 'Saputra'),
        ('Javier', 'Ortega', 'Sergio', 'Mendez'), ('Anthony', 'Price', 'Caleb', 'James'),
        ('Ami', 'Suzuki', 'Riku', 'Endo'), ('Viktoria', 'Taneva', 'Borislav', 'Nedev'),
    ]

    perks_available = [
        'Outdoor seating', 'Vegetarian options', 'Vegan options', 'Pet friendly',
        'Free Wi-Fi', 'Parking', 'Private dining', 'Takeaway',
        "Children's entertainer", "Kids' playground", 'High chairs',
        "Children's menu", 'Baby changing station', 'Live music',
        'Heated outdoor seating', 'Board games',
    ]
    extra_perks = {
        'North Star Brunch': ["Children's entertainer", "Kids' playground", 'High chairs', "Children's menu", 'Baby changing station', 'Board games'],
        'The Sunday Table': ["Children's entertainer", "Kids' playground", 'High chairs', "Children's menu", 'Baby changing station'],
        'Casa del Sol': ['Live music'],
        'La Mesa Roja': ['Live music'],
        'Juniper & Rye': ['Heated outdoor seating'],
    }

    @transaction.atomic
    def handle(self, *args, **options):
        perks = {
            name: Perks.objects.get_or_create(name=name, defaults={'is_active': True})[0]
            for name in self.perks_available
        }
        restaurant_columns = self.table_columns(Restaurant)
        employee_columns = self.table_columns(Employee)
        created_restaurants = created_employees = 0

        for index, row in enumerate(self.restaurants):
            name, street, cuisine, owner, description, perk_names, signature = row
            email_slug = slugify(name).replace('-', '')
            defaults = {
                'address': f'{street}, Sofia',
                'email': f'{email_slug}@hypserve.com',
                'description': description,
                'cuisine_type': cuisine,
                'owner': owner,
            }
            restaurant = Restaurant.objects.filter(name=name).first()
            if restaurant is None:
                restaurant = self.create_restaurant(name, defaults, restaurant_columns)
                created_restaurants += 1
            else:
                for field, value in defaults.items():
                    setattr(restaurant, field, value)
                restaurant.save()
            restaurant.perks.add(*(perks[perk] for perk in perk_names))
            restaurant.perks.add(*(perks[perk] for perk in self.extra_perks.get(name, [])))

            chef_first, chef_last, sous_first, sous_last = self.staff[index]
            employees = []
            for position, first, last, rating, author, role in (
                (Employee.PositionChoices.CH, chef_first, chef_last, Decimal('4.85'), 'Alex Morgan', 'chef'),
                (Employee.PositionChoices.SO, sous_first, sous_last, Decimal('4.65'), 'Riley Chen', 'sous chef'),
            ):
                employee_email = f'{slugify(first + "-" + last)}@hypserve.com'
                is_new_employee = not Employee.objects.filter(email=employee_email).exists()
                phone_slot = index * 2 + (1 if position == Employee.PositionChoices.SO else 0)
                employee = self.create_employee(
                    first, last, position, restaurant, phone_slot, employee_columns,
                )
                if is_new_employee:
                    created_employees += 1
                employees.append(employee)
                EmployeeReview.objects.get_or_create(
                    employee=employee,
                    title=f'Kitchen craft at {name}',
                    author=author,
                    defaults={
                        'content': f'The {role} brought care and consistency to the kitchen. The {signature} was thoughtfully prepared, and the team worked with excellent timing.',
                        'rating': rating,
                    },
                )

            guest_reviews = [
                ('A memorable meal', 'Jordan Ellis', Decimal('4.80'), f'The {signature} was a highlight, and the menu felt carefully connected to the season. The service was warm and the atmosphere made it easy to linger.'),
                ('A place worth returning to', 'Casey Taylor', Decimal('4.60'), f'We enjoyed the {signature} and appreciated the thoughtful options across the menu. A welcoming team and a relaxed room made this a very enjoyable visit.'),
            ]
            for title, author, rating, content in guest_reviews:
                Review.objects.get_or_create(
                    restaurant=restaurant, title=title, author=author,
                    defaults={'content': content, 'rating': rating},
                )

        self.stdout.write(self.style.SUCCESS(
            f'Restaurant directory ready: {Restaurant.objects.count()} restaurants; '
            f'added {created_restaurants} restaurants and {created_employees} new employees. '
            f'Now {Employee.objects.count()} employees, '
            f'{Review.objects.count()} restaurant reviews, '
            f'{EmployeeReview.objects.count()} employee reviews.'
        ))

    @staticmethod
    def create_restaurant(name, defaults, columns):
        if 'rating' in columns:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO restaurants_restaurant '
                    '(name, address, email, description, cuisine_type, owner, slug, rating) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                    [name, defaults['address'], defaults['email'], defaults['description'],
                     defaults['cuisine_type'], defaults['owner'],
                     slugify(f"{name} {defaults['cuisine_type']}"), 0],
                )
                return Restaurant.objects.get(pk=cursor.fetchone()[0])
        return Restaurant.objects.create(name=name, **defaults)

    @staticmethod
    def create_employee(first, last, position, restaurant, index, columns):
        email = f'{slugify(first + "-" + last)}@hypserve.com'
        phone = f'+359 2 001 {index + 2000:04d}'
        employee = Employee.objects.filter(email=email).first()
        if employee is not None:
            employee.restaurant = restaurant
            employee.position = position
            employee.save(update_fields=['restaurant', 'position'])
            return employee
        if 'rating' in columns:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO employees_employee '
                    '(first_name, last_name, email, phone_number, position, restaurant_id, rating) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                    [first, last, email, phone, position, restaurant.pk, 3],
                )
                return Employee.objects.get(pk=cursor.fetchone()[0])
        return Employee.objects.create(
            first_name=first, last_name=last, email=email, phone_number=phone,
            position=position, restaurant=restaurant,
        )

    @staticmethod
    def table_columns(model):
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        return {column.name for column in description}