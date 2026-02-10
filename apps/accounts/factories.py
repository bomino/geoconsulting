import factory

from apps.accounts.models import Profile, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        password = extracted or "testpass123"
        obj.set_password(password)
        if create:
            obj.save(update_fields=["password"])


class StaffUserFactory(UserFactory):
    is_staff = True


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
