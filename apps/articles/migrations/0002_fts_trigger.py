from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE OR REPLACE FUNCTION update_article_search_vector()
                RETURNS trigger AS $$
                BEGIN
                  NEW.search_vector :=
                    to_tsvector('french', coalesce(NEW.title, '')) ||
                    to_tsvector('french', coalesce(NEW.excerpt, '')) ||
                    to_tsvector('french', coalesce(NEW.content, ''));
                  RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER article_search_update
                  BEFORE INSERT OR UPDATE OF title, excerpt, content
                  ON articles_article
                  FOR EACH ROW EXECUTE FUNCTION update_article_search_vector();
            """,
            reverse_sql="""
                DROP TRIGGER IF EXISTS article_search_update ON articles_article;
                DROP FUNCTION IF EXISTS update_article_search_vector();
            """,
        ),
    ]
