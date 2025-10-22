"""
Management command para poblar la base de datos con datos de prueba
Uso: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from frontend.models import Page
from orders.models import Order, OrderItem
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🌱 Iniciando seed de datos...'))

        # 1. Crear usuarios de prueba
        self.create_users()

        # 2. Crear categorías
        self.create_categories()

        # 3. Crear productos
        self.create_products()

        # 4. Crear páginas de contenido
        self.create_pages()

        # 5. Crear pedidos de ejemplo
        self.create_orders()

        self.stdout.write(self.style.SUCCESS('\n✅ Seed completado exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\n📋 Resumen:'))
        self.stdout.write(f'   - Usuarios: {User.objects.count()}')
        self.stdout.write(f'   - Categorías: {Category.objects.count()}')
        self.stdout.write(f'   - Productos: {Product.objects.count()}')
        self.stdout.write(f'   - Páginas: {Page.objects.count()}')
        self.stdout.write(f'   - Pedidos: {Order.objects.count()}')

    def create_users(self):
        self.stdout.write('\n👥 Creando usuarios...')

        # Usuario admin (si no existe)
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@admin.com',
                'full_name': 'Administrador',
                'is_admin': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write(self.style.SUCCESS('   ✅ Admin creado'))
        else:
            self.stdout.write('   ⏭️  Admin ya existe')

        # Clientes de prueba
        clientes = [
            {
                'username': 'cliente1',
                'email': 'cliente1@test.com',
                'full_name': 'María García',
                'password': 'test123'
            },
            {
                'username': 'cliente2',
                'email': 'cliente2@test.com',
                'full_name': 'Carlos Rodríguez',
                'password': 'test123'
            },
            {
                'username': 'cliente3',
                'email': 'cliente3@test.com',
                'full_name': 'Ana Martínez',
                'password': 'test123'
            },
        ]

        for cliente_data in clientes:
            password = cliente_data.pop('password')
            cliente, created = User.objects.get_or_create(
                username=cliente_data['username'],
                defaults=cliente_data
            )
            if created:
                cliente.set_password(password)
                cliente.save()
                self.stdout.write(self.style.SUCCESS(f'   ✅ Cliente {cliente.username} creado'))

    def create_categories(self):
        self.stdout.write('\n📁 Creando categorías...')

        categorias = [
            {'name': 'Anillos', 'slug': 'anillos', 'description': 'Anillos de oro de alta calidad'},
            {'name': 'Collares', 'slug': 'collares', 'description': 'Collares elegantes y sofisticados'},
            {'name': 'Pulseras', 'slug': 'pulseras', 'description': 'Pulseras finas y delicadas'},
            {'name': 'Aretes', 'slug': 'aretes', 'description': 'Aretes brillantes y modernos'},
            {'name': 'Relojes', 'slug': 'relojes', 'description': 'Relojes de lujo premium'},
        ]

        for cat_data in categorias:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✅ {cat.name} creada'))
            else:
                self.stdout.write(f'   ⏭️  {cat.name} ya existe')

    def create_products(self):
        self.stdout.write('\n🛍️  Creando productos...')

        # Obtener categorías
        anillos = Category.objects.get(slug='anillos')
        collares = Category.objects.get(slug='collares')
        pulseras = Category.objects.get(slug='pulseras')
        aretes = Category.objects.get(slug='aretes')
        relojes = Category.objects.get(slug='relojes')

        productos = [
            # Anillos
            {'name': 'Anillo Minimal', 'category': anillos, 'price': '150000', 'stock': 15, 'material': 'Oro 14k', 'size': 'Ajustable'},
            {'name': 'Anillo Royal', 'category': anillos, 'price': '180000', 'stock': 12, 'material': 'Oro 18k', 'size': '6-8'},
            {'name': 'Anillo Aurora Brillante', 'category': anillos, 'price': '220000', 'stock': 8, 'material': 'Oro blanco 18k', 'size': 'Personalizable'},
            {'name': 'Anillo Eterno Compromiso', 'category': anillos, 'price': '350000', 'stock': 5, 'material': 'Platino con diamante', 'size': '5-9'},

            # Collares
            {'name': 'Collar Minimal Glow', 'category': collares, 'price': '210000', 'stock': 20, 'material': 'Oro 14k', 'size': '45cm'},
            {'name': 'Collar Brillo Infinito', 'category': collares, 'price': '250000', 'stock': 15, 'material': 'Oro 18k', 'size': '50cm'},
            {'name': 'Collar Romance Puro', 'category': collares, 'price': '290000', 'stock': 10, 'material': 'Oro rosado 18k', 'size': '40cm'},
            {'name': 'Collar Lágrima Celestial', 'category': collares, 'price': '420000', 'stock': 6, 'material': 'Oro blanco con zafiro', 'size': '45cm'},

            # Pulseras
            {'name': 'Pulsera Romance Clásico', 'category': pulseras, 'price': '170000', 'stock': 18, 'material': 'Oro 14k', 'size': 'Ajustable'},
            {'name': 'Pulsera Vanguardia', 'category': pulseras, 'price': '200000', 'stock': 14, 'material': 'Oro 18k', 'size': '18cm'},
            {'name': 'Pulsera Encanto Natural', 'category': pulseras, 'price': '190000', 'stock': 16, 'material': 'Oro amarillo 14k', 'size': '17cm'},
            {'name': 'Pulsera Tenis Diamante', 'category': pulseras, 'price': '580000', 'stock': 4, 'material': 'Oro blanco con diamantes', 'size': '19cm'},

            # Aretes
            {'name': 'Aretes Brillo Estelar', 'category': aretes, 'price': '160000', 'stock': 22, 'material': 'Oro 14k', 'size': 'Pequeño'},
            {'name': 'Aretes Luz de Luna', 'category': aretes, 'price': '180000', 'stock': 19, 'material': 'Oro blanco 18k', 'size': 'Mediano'},
            {'name': 'Aretes Flor Dorada', 'category': aretes, 'price': '195000', 'stock': 17, 'material': 'Oro rosado 14k', 'size': 'Grande'},
            {'name': 'Aretes Solitario Premium', 'category': aretes, 'price': '450000', 'stock': 7, 'material': 'Platino con diamante', 'size': 'Mediano'},

            # Relojes
            {'name': 'Reloj Deportivo Lux', 'category': relojes, 'price': '450000', 'stock': 10, 'material': 'Acero inoxidable con oro', 'size': 'Unisex'},
            {'name': 'Reloj Clásico Dorado', 'category': relojes, 'price': '520000', 'stock': 8, 'material': 'Oro 18k', 'size': 'Hombre'},
            {'name': 'Reloj Royal Cronógrafo', 'category': relojes, 'price': '600000', 'stock': 5, 'material': 'Oro y cerámica', 'size': 'Hombre'},
            {'name': 'Reloj Dama Elegance', 'category': relojes, 'price': '380000', 'stock': 12, 'material': 'Oro rosado y cristal', 'size': 'Mujer'},
        ]

        for prod_data in productos:
            prod, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': prod_data['category'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'material': prod_data['material'],
                    'size': prod_data['size'],
                    'description': f"Hermoso {prod_data['name']} elaborado en {prod_data['material']}. Pieza única de alta calidad.",
                    'weight': '5.5',
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✅ {prod.name} creado'))

    def create_pages(self):
        self.stdout.write('\n📄 Creando páginas...')

        paginas = [
            {
                'title': 'Sobre Nosotros',
                'slug': 'sobre-nosotros',
                'content': '''
                    <h1>Alma de Oro</h1>
                    <p>Somos una joyería de lujo con más de 20 años de experiencia en la creación de piezas únicas.</p>
                    <h2>Nuestra Misión</h2>
                    <p>Crear joyas que cuenten historias y se conviertan en tesoros familiares.</p>
                    <h2>Nuestros Valores</h2>
                    <ul>
                        <li>Calidad excepcional</li>
                        <li>Diseño único</li>
                        <li>Atención personalizada</li>
                        <li>Compromiso con la excelencia</li>
                    </ul>
                ''',
                'meta_description': 'Conoce la historia de Alma de Oro, joyería de lujo con más de 20 años de experiencia',
            },
            {
                'title': 'Política de Envíos',
                'slug': 'politica-envios',
                'content': '''
                    <h1>Política de Envíos</h1>
                    <h2>Tiempos de Entrega</h2>
                    <p>Los envíos se realizan en un plazo de 3 a 5 días hábiles.</p>
                    <h2>Costos</h2>
                    <p>Envío gratis en compras superiores a $500.000</p>
                    <h2>Cobertura</h2>
                    <p>Realizamos envíos a toda Colombia</p>
                ''',
                'meta_description': 'Conoce nuestra política de envíos y tiempos de entrega',
            },
            {
                'title': 'Términos y Condiciones',
                'slug': 'terminos-condiciones',
                'content': '''
                    <h1>Términos y Condiciones</h1>
                    <h2>1. Uso del Sitio</h2>
                    <p>Al acceder y usar este sitio web, aceptas estos términos y condiciones.</p>
                    <h2>2. Productos</h2>
                    <p>Todos los productos están sujetos a disponibilidad.</p>
                    <h2>3. Garantía</h2>
                    <p>Todos nuestros productos cuentan con garantía de 1 año.</p>
                ''',
                'meta_description': 'Términos y condiciones de uso de Alma de Oro',
            },
        ]

        for page_data in paginas:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✅ Página "{page.title}" creada'))
            else:
                self.stdout.write(f'   ⏭️  Página "{page.title}" ya existe')

    def create_orders(self):
        self.stdout.write('\n📦 Creando pedidos de ejemplo...')

        # Obtener clientes y productos
        try:
            cliente1 = User.objects.get(username='cliente1')
            cliente2 = User.objects.get(username='cliente2')

            producto1 = Product.objects.filter(name__icontains='Anillo').first()
            producto2 = Product.objects.filter(name__icontains='Collar').first()
            producto3 = Product.objects.filter(name__icontains='Pulsera').first()

            if not all([cliente1, cliente2, producto1, producto2, producto3]):
                self.stdout.write(self.style.WARNING('   ⚠️  Faltan datos para crear pedidos'))
                return

            # Pedido 1 - Completado
            order1, created = Order.objects.get_or_create(
                user=cliente1,
                status='completed',
                defaults={
                    'total_cents': int(float(producto1.price) + float(producto2.price)),
                    'nombre': cliente1.full_name,
                    'direccion': 'Calle 123 # 45-67, Bogotá',
                    'telefono': '3001234567',
                }
            )
            if created:
                OrderItem.objects.create(order=order1, product=producto1, quantity=1, price_cents=int(float(producto1.price)))
                OrderItem.objects.create(order=order1, product=producto2, quantity=1, price_cents=int(float(producto2.price)))
                self.stdout.write(self.style.SUCCESS(f'   ✅ Pedido #{order1.id} creado'))

            # Pedido 2 - Pendiente
            order2, created = Order.objects.get_or_create(
                user=cliente2,
                status='pending',
                defaults={
                    'total_cents': int(float(producto3.price) * 2),
                    'nombre': cliente2.full_name,
                    'direccion': 'Carrera 15 # 89-12, Medellín',
                    'telefono': '3109876543',
                }
            )
            if created:
                OrderItem.objects.create(order=order2, product=producto3, quantity=2, price_cents=int(float(producto3.price)))
                self.stdout.write(self.style.SUCCESS(f'   ✅ Pedido #{order2.id} creado'))

        except Exception as e:
            self.stdout.write(self.style.WARNING(f'   ⚠️  Error creando pedidos: {str(e)}'))
