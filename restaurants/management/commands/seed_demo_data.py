from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import connection
from django.utils.text import slugify

from employees.models import Employee, EmployeeReview
from restaurants.models import Perks, Restaurant
from reviews.models import Review


class Command(BaseCommand):
    help = 'Add realistic fictional sample data to the HyperServe content tables.'

    def handle(self, *args, **options):
        perk_names = [
            'Outdoor seating', 'Vegetarian options', 'Vegan options', 'Pet friendly',
            'Free Wi-Fi', 'Parking', 'Private dining', 'Takeaway',
        ]
        perks = {
            name: Perks.objects.get_or_create(name=name, defaults={'is_active': True})[0]
            for name in perk_names
        }

        restaurant_rows = [
            ('The Copper Fig', '21 Shishman Street, Sofia', 'copperfig@hypserve.com',
             'Seasonal Bulgarian cooking, local produce, and a relaxed dining room in the heart of the city.',
             Restaurant.TypeChoices.BU, 'Elena Markova', ['Outdoor seating', 'Vegetarian options', 'Private dining']),
            ('Olive & Ember', '8 Oborishte Street, Sofia', 'oliveember@hypserve.com',
             'Handmade pasta, wood-fired dishes, and a thoughtful wine list inspired by the Italian table.',
             Restaurant.TypeChoices.IT, 'Marta Leone', ['Vegetarian options', 'Vegan options', 'Outdoor seating']),
            ('Little Kyoto', '14 Tsar Ivan Shishman Street, Sofia', 'littlekyoto@hypserve.com',
             'A small Japanese kitchen serving seasonal ramen, carefully prepared sushi, and house-made tea.',
             Restaurant.TypeChoices.JA, 'Aiko Tanaka', ['Takeaway', 'Free Wi-Fi', 'Vegetarian options']),
            ('Cedar House', '6 San Stefano Street, Sofia', 'cedarhouse@hypserve.com',
             'Bright Mediterranean plates, grilled vegetables, and a welcoming terrace for long lunches.',
             Restaurant.TypeChoices.OT, 'Nadia Georgieva', ['Outdoor seating', 'Pet friendly', 'Vegan options']),
            ('Blue Moon Diner', '32 Graf Ignatiev Street, Sofia', 'bluemoon@hypserve.com',
             'A neighborhood American-style diner for generous brunches, classic burgers, and late coffee.',
             Restaurant.TypeChoices.AM, 'Talia Morris', ['Free Wi-Fi', 'Parking', 'Takeaway']),
            ('The Market Table', '10 Solunska Street, Sofia', 'markettable@hypserve.com',
             'A produce-led dining room with a changing menu shaped by the best ingredients at the market.',
             Restaurant.TypeChoices.OT, 'Yana Koleva', ['Vegetarian options', 'Vegan options', 'Private dining']),
        ]
        restaurants = {}
        restaurant_columns = self.table_columns(Restaurant)
        for name, address, email, description, cuisine, owner, restaurant_perks in restaurant_rows:
            restaurant = Restaurant.objects.filter(name=name).first()
            if restaurant is None:
                if 'rating' in restaurant_columns:
                    # The configured database retains a required legacy rating column.
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO restaurants_restaurant '
                            '(name, address, email, description, cuisine_type, owner, slug, rating) '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                            [name, address, email, description, cuisine, owner,
                             slugify(f'{name} {cuisine}'), 0],
                        )
                        restaurant_id = cursor.fetchone()[0]
                    restaurant = Restaurant.objects.get(pk=restaurant_id)
                else:
                    restaurant = Restaurant.objects.create(
                        name=name, address=address, email=email,
                        description=description, cuisine_type=cuisine, owner=owner,
                    )
            restaurant.perks.add(*(perks[perk] for perk in restaurant_perks))
            restaurants[name] = restaurant

        employee_rows = [
            ('Elena', 'Markova', Employee.PositionChoices.CH, 'The Copper Fig', 'elena.markova@hypserve.com', '+359 2 000 1001'),
            ('Petar', 'Dimitrov', Employee.PositionChoices.SO, 'The Copper Fig', 'petar.dimitrov@hypserve.com', '+359 2 000 1002'),
            ('Marta', 'Leone', Employee.PositionChoices.CH, 'Olive & Ember', 'marta.leone@hypserve.com', '+359 2 000 1003'),
            ('Luca', 'Romano', Employee.PositionChoices.SO, 'Olive & Ember', 'luca.romano@hypserve.com', '+359 2 000 1004'),
            ('Aiko', 'Tanaka', Employee.PositionChoices.CH, 'Little Kyoto', 'aiko.tanaka@hypserve.com', '+359 2 000 1005'),
            ('Ren', 'Ito', Employee.PositionChoices.SO, 'Little Kyoto', 'ren.ito@hypserve.com', '+359 2 000 1006'),
            ('Nadia', 'Georgieva', Employee.PositionChoices.CH, 'Cedar House', 'nadia.georgieva@hypserve.com', '+359 2 000 1007'),
            ('Simeon', 'Ivanov', Employee.PositionChoices.SO, 'Cedar House', 'simeon.ivanov@hypserve.com', '+359 2 000 1008'),
            ('Talia', 'Morris', Employee.PositionChoices.CH, 'Blue Moon Diner', 'talia.morris@hypserve.com', '+359 2 000 1009'),
            ('Marcus', 'Reed', Employee.PositionChoices.SO, 'Blue Moon Diner', 'marcus.reed@hypserve.com', '+359 2 000 1010'),
            ('Yana', 'Koleva', Employee.PositionChoices.CH, 'The Market Table', 'yana.koleva@hypserve.com', '+359 2 000 1011'),
            ('Ivan', 'Petrov', Employee.PositionChoices.SO, 'The Market Table', 'ivan.petrov@hypserve.com', '+359 2 000 1012'),
        ]
        employees = {}
        employee_columns = self.table_columns(Employee)
        for first_name, last_name, position, restaurant_name, email, phone in employee_rows:
            employee = Employee.objects.filter(email=email).first()
            if employee is None:
                if 'rating' in employee_columns:
                    # The configured database retains a required legacy employee rating column.
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO employees_employee '
                            '(first_name, last_name, email, phone_number, position, restaurant_id, rating) '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                            [first_name, last_name, email, phone, position,
                             restaurants[restaurant_name].pk, 3],
                        )
                        employee_id = cursor.fetchone()[0]
                    employee = Employee.objects.get(pk=employee_id)
                else:
                    employee = Employee.objects.create(
                        first_name=first_name, last_name=last_name, email=email,
                        phone_number=phone, position=position,
                        restaurant=restaurants[restaurant_name],
                    )
            employees[email] = employee

        staff_review_rows = [
            ('elena.markova@hypserve.com', 'Care in every detail', 'Alex Morgan', 'A thoughtful cook with a calm, precise approach. Every plate felt balanced and carefully prepared.', '4.90'),
            ('elena.markova@hypserve.com', 'A memorable seasonal menu', 'Riley Chen', 'The seasonal dishes were full of character. Elena clearly takes great care with local ingredients.', '4.80'),
            ('petar.dimitrov@hypserve.com', 'A steady hand in the kitchen', 'Jordan Ellis', 'Petar kept the kitchen running smoothly and sent out a consistently excellent meal.', '4.60'),
            ('petar.dimitrov@hypserve.com', 'Excellent preparation', 'Casey Taylor', 'Well prepared dishes and a thoughtful attention to timing made the evening easy to enjoy.', '4.50'),
            ('marta.leone@hypserve.com', 'Beautiful handmade pasta', 'Alex Morgan', 'The pasta was delicate, fresh, and full of flavor. Marta made the meal feel special without fuss.', '4.90'),
            ('marta.leone@hypserve.com', 'A warm welcome', 'Riley Chen', 'A generous host and a talented chef. The menu was clear, seasonal, and delicious.', '4.80'),
            ('luca.romano@hypserve.com', 'The perfect finish', 'Jordan Ellis', 'Luca brought a great deal of care to every course and made excellent recommendations.', '4.60'),
            ('luca.romano@hypserve.com', 'Attentive service', 'Casey Taylor', 'The team was organized and friendly, and the meal arrived at just the right pace.', '4.40'),
            ('aiko.tanaka@hypserve.com', 'Exceptional ramen', 'Alex Morgan', 'A deeply flavorful broth and perfectly cooked noodles. Aiko is clearly dedicated to her craft.', '5.00'),
            ('aiko.tanaka@hypserve.com', 'A lovely Japanese meal', 'Riley Chen', 'Careful preparation and beautifully balanced flavors made this one of my favorite dinners.', '4.90'),
            ('ren.ito@hypserve.com', 'Fresh and beautifully prepared', 'Jordan Ellis', 'The sushi was fresh, neatly prepared, and served with a helpful explanation of the menu.', '4.70'),
            ('ren.ito@hypserve.com', 'Great attention to detail', 'Casey Taylor', 'A smooth service and well prepared dishes from start to finish.', '4.60'),
            ('nadia.georgieva@hypserve.com', 'A bright, fresh menu', 'Alex Morgan', 'Nadia made vegetables the highlight of the meal. Everything tasted fresh and vibrant.', '4.80'),
            ('nadia.georgieva@hypserve.com', 'A beautiful terrace lunch', 'Riley Chen', 'A relaxed lunch with thoughtful dishes and a warm welcome from Nadia and the team.', '4.70'),
            ('simeon.ivanov@hypserve.com', 'Great teamwork', 'Jordan Ellis', 'The kitchen worked seamlessly, and every dish arrived fresh and well presented.', '4.50'),
            ('simeon.ivanov@hypserve.com', 'Consistent and welcoming', 'Casey Taylor', 'A friendly team and a very enjoyable meal. I would happily come back.', '4.40'),
            ('talia.morris@hypserve.com', 'Brunch done right', 'Alex Morgan', 'Talia brought real care to a familiar menu. The brunch was generous, well seasoned, and satisfying.', '4.80'),
            ('talia.morris@hypserve.com', 'A neighborhood favorite', 'Riley Chen', 'Excellent comfort food and a friendly atmosphere. The team made us feel at home.', '4.70'),
            ('marcus.reed@hypserve.com', 'A perfectly cooked burger', 'Jordan Ellis', 'The burger was cooked exactly right, and the kitchen handled a busy evening with ease.', '4.60'),
            ('marcus.reed@hypserve.com', 'Friendly and efficient', 'Casey Taylor', 'Quick, welcoming service and a meal that arrived hot and fresh.', '4.50'),
            ('yana.koleva@hypserve.com', 'Seasonal cooking at its best', 'Alex Morgan', 'Yana built a balanced menu around excellent market ingredients. A polished, memorable meal.', '4.90'),
            ('yana.koleva@hypserve.com', 'A lovely market menu', 'Riley Chen', 'The menu felt fresh and carefully considered. Every course had a clear point of view.', '4.80'),
            ('ivan.petrov@hypserve.com', 'Thoughtful, precise cooking', 'Jordan Ellis', 'A great example of simple ingredients treated with care and confidence.', '4.60'),
            ('ivan.petrov@hypserve.com', 'Wonderful hospitality', 'Casey Taylor', 'The team was attentive and kind, and the meal was beautifully paced.', '4.50'),
        ]
        for email, title, author, content, rating in staff_review_rows:
            EmployeeReview.objects.get_or_create(
                employee=employees[email], title=title, author=author,
                defaults={'content': content, 'rating': Decimal(rating)},
            )

        guest_review_rows = [
            ('The Copper Fig', 'A generous taste of Bulgaria', 'Alex Morgan', 'The grilled vegetables and slow-cooked dishes were excellent. Warm service and a relaxed room made this an easy place to recommend.', '4.80'),
            ('The Copper Fig', 'A lovely neighborhood dinner', 'Riley Chen', 'Seasonal ingredients, thoughtful portions, and a very welcoming team. The outdoor tables are a nice touch.', '4.60'),
            ('The Copper Fig', 'Local flavors, beautifully done', 'Jordan Ellis', 'A well considered menu that celebrates Bulgarian cooking without feeling formal. We will be back.', '4.70'),
            ('Olive & Ember', 'Fresh pasta worth returning for', 'Casey Taylor', 'The handmade pasta was excellent and the staff gave helpful wine suggestions. A relaxed, polished dinner.', '4.90'),
            ('Olive & Ember', 'A warm Italian evening', 'Alex Morgan', 'Great wood-fired vegetables, lovely bread, and a welcoming atmosphere. The menu has something for everyone.', '4.70'),
            ('Olive & Ember', 'Excellent from start to finish', 'Riley Chen', 'The service was attentive without hovering and every dish was well prepared. Save room for dessert.', '4.80'),
            ('Little Kyoto', 'Carefully made ramen', 'Jordan Ellis', 'The broth was rich and balanced, with fresh toppings and perfectly cooked noodles. A small place with a lot of care.', '4.90'),
            ('Little Kyoto', 'A quiet sushi favorite', 'Casey Taylor', 'Fresh sushi, a concise menu, and friendly service. It is a good choice for a relaxed dinner.', '4.80'),
            ('Little Kyoto', 'Thoughtful Japanese cooking', 'Alex Morgan', 'Everything was neatly presented and full of flavor. The staff helped us choose dishes to share.', '4.70'),
            ('Cedar House', 'Fresh Mediterranean flavors', 'Riley Chen', 'A bright menu with excellent grilled vegetables and a pleasant terrace. Great for an unhurried lunch.', '4.70'),
            ('Cedar House', 'A lovely place to gather', 'Jordan Ellis', 'We shared several dishes and enjoyed every one. The staff were kind and the atmosphere was easygoing.', '4.60'),
            ('Cedar House', 'Excellent seasonal plates', 'Casey Taylor', 'Fresh ingredients and generous flavors, with enough vegetarian choices to make the whole group happy.', '4.80'),
            ('Blue Moon Diner', 'Comfort food and friendly service', 'Alex Morgan', 'A satisfying burger, crisp fries, and a cheerful team. A dependable neighborhood stop.', '4.50'),
            ('Blue Moon Diner', 'A relaxed weekend brunch', 'Riley Chen', 'Good coffee, generous portions, and a relaxed pace. The menu has all the diner classics we wanted.', '4.40'),
            ('Blue Moon Diner', 'Classic diner favorites', 'Jordan Ellis', 'The food arrived hot and the service was quick. A comfortable place for a casual meal.', '4.60'),
            ('The Market Table', 'A seasonal menu with character', 'Casey Taylor', 'The ingredients were the star of every course. A thoughtful menu and polished service made for a memorable evening.', '4.90'),
            ('The Market Table', 'A great place for a special dinner', 'Alex Morgan', 'Beautifully balanced dishes, excellent pacing, and a team that made us feel welcome from the moment we arrived.', '4.80'),
            ('The Market Table', 'Fresh, thoughtful, and delicious', 'Riley Chen', 'The menu changes with the market and it shows. Every dish felt fresh, intentional, and full of flavor.', '4.70'),
        ]
        for restaurant_name, title, author, content, rating in guest_review_rows:
            Review.objects.get_or_create(
                restaurant=restaurants[restaurant_name], title=title, author=author,
                defaults={'content': content, 'rating': Decimal(rating)},
            )

        self.stdout.write(self.style.SUCCESS(
            'Sample data ready: '
            f'{Perks.objects.count()} perks, {Restaurant.objects.count()} restaurants, '
            f'{Employee.objects.count()} employees, '
            f'{EmployeeReview.objects.count()} employee reviews, {Review.objects.count()} guest reviews.'
        ))

    @staticmethod
    def table_columns(model):
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(
                cursor, model._meta.db_table
            )
        return {column.name for column in description}
