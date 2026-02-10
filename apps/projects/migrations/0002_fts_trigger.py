from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE FUNCTION update_project_search_vector()
                RETURNS trigger AS $$
                BEGIN
                  NEW.search_vector :=
                    to_tsvector('french', coalesce(NEW.title, '')) ||
                    to_tsvector('french', coalesce(NEW.description, '')) ||
                    to_tsvector('french', coalesce(NEW.location, ''));
                  RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER project_search_update
                  BEFORE INSERT OR UPDATE OF title, description, location
                  ON projects_project
                  FOR EACH ROW EXECUTE FUNCTION update_project_search_vector();
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS project_search_update ON projects_project;
                DROP FUNCTION IF EXISTS update_project_search_vector();
            """,
        ),
    ]
