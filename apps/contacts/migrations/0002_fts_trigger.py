from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE FUNCTION update_contact_search_vector()
                RETURNS trigger AS $$
                BEGIN
                  NEW.search_vector :=
                    to_tsvector('french', coalesce(NEW.name, '')) ||
                    to_tsvector('french', coalesce(NEW.subject, '')) ||
                    to_tsvector('french', coalesce(NEW.message, ''));
                  RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER contact_search_update
                  BEFORE INSERT OR UPDATE OF name, subject, message
                  ON contacts_contact
                  FOR EACH ROW EXECUTE FUNCTION update_contact_search_vector();
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS contact_search_update ON contacts_contact;
                DROP FUNCTION IF EXISTS update_contact_search_vector();
            """,
        ),
    ]
