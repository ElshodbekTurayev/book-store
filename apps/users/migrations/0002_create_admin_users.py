from django.db import migrations

def create_admin_users(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    from django.contrib.auth.hashers import make_password
    
    admin_accounts = [
        ('elshodbekturayev005@gmail.com', 'elshodbek', 'admin123'),
        ('admin@bookstore.com', 'admin', 'admin123'),
    ]
    
    for email, username, password in admin_accounts:
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            user = CustomUser(email=email, username=username)
        
        user.password = make_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email_verified = True
        user.role = 'super_admin'
        user.save()

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_users, reverse_func),
    ]
